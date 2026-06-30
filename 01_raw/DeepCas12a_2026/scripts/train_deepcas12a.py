import argparse
import json
import random
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import torch
import torch.nn as nn
from scipy.stats import pearsonr, spearmanr
from sklearn.metrics import average_precision_score, roc_auc_score
from torch.utils.data import DataLoader, TensorDataset
from tqdm import tqdm

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from DeepCas12a import Episgt, VisionTransformer


def set_seed(seed):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)


def load_dataset(path):
    data = Episgt(path, num_epi_features=2, with_y=True)
    x, y = data.get_dataset()
    x = torch.tensor(x, dtype=torch.float32).unsqueeze(1)
    y = torch.tensor(y, dtype=torch.long)
    return x, y


def load_fold_indices(partitions_csv, fold):
    partitions = pd.read_csv(partitions_csv)
    fold_df = partitions[partitions["fold"] == fold]
    train_idx = fold_df.loc[fold_df["partition"] == "train", "training_index"].to_numpy()
    val_idx = fold_df.loc[fold_df["partition"] == "validation", "training_index"].to_numpy()
    return train_idx, val_idx


def make_loader(x, y, indices, batch_size, shuffle):
    dataset = TensorDataset(x[indices], y[indices])
    return DataLoader(dataset, batch_size=batch_size, shuffle=shuffle)


def train_one_fold(args, fold, x, y, device):
    train_idx, val_idx = load_fold_indices(args.partitions_csv, fold)
    train_loader = make_loader(x, y, train_idx, args.batch_size, True)
    val_loader = make_loader(x, y, val_idx, args.batch_size, False)

    model = VisionTransformer(
        embed_dim=args.embed_dim,
        depth=args.depth,
        num_heads=args.num_heads,
        mlp_ratio=args.mlp_ratio,
        dropout=args.dropout,
        attention_drop=args.attention_dropout,
    ).to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=args.learning_rate, weight_decay=args.weight_decay)

    best_acc = -1.0
    patience_counter = 0
    fold_dir = args.output_dir / f"fold{fold}"
    fold_dir.mkdir(parents=True, exist_ok=True)
    checkpoint_path = fold_dir / "model.pth"

    for epoch in range(1, args.epochs + 1):
        model.train()
        for batch_x, batch_y in tqdm(train_loader, desc=f"fold {fold} epoch {epoch}", leave=False):
            batch_x = batch_x.to(device)
            batch_y = batch_y.to(device)
            optimizer.zero_grad()
            loss = criterion(model.forward_logits(batch_x), batch_y)
            loss.backward()
            optimizer.step()

        val_acc = evaluate_accuracy(model, val_loader, device)
        if val_acc > best_acc + args.min_delta:
            best_acc = val_acc
            patience_counter = 0
            torch.save(model.state_dict(), checkpoint_path)
        else:
            patience_counter += 1
        if patience_counter >= args.patience:
            break

    return {"fold": fold, "best_val_accuracy": best_acc, "checkpoint": str(checkpoint_path)}


def evaluate_accuracy(model, loader, device):
    model.eval()
    correct = 0
    total = 0
    with torch.no_grad():
        for batch_x, batch_y in loader:
            logits = model.forward_logits(batch_x.to(device))
            preds = logits.argmax(dim=1).cpu()
            correct += (preds == batch_y).sum().item()
            total += len(batch_y)
    return correct / total


def predict_proba(model, loader, device):
    model.eval()
    probs = []
    labels = []
    with torch.no_grad():
        for batch_x, batch_y in loader:
            logits = model.forward_logits(batch_x.to(device))
            probs.append(torch.softmax(logits, dim=1)[:, 1].cpu().numpy())
            labels.append(batch_y.numpy())
    return np.concatenate(probs), np.concatenate(labels)


def evaluate_ensemble(args, device):
    x_test, y_test = load_dataset(args.test_data)
    test_loader = DataLoader(TensorDataset(x_test, y_test), batch_size=args.batch_size, shuffle=False)
    fold_probs = []
    for fold in range(1, args.n_splits + 1):
        checkpoint = args.output_dir / f"fold{fold}" / "model.pth"
        model = VisionTransformer(
            embed_dim=args.embed_dim,
            depth=args.depth,
            num_heads=args.num_heads,
            mlp_ratio=args.mlp_ratio,
            dropout=args.dropout,
            attention_drop=args.attention_dropout,
        ).to(device)
        model.load_state_dict(torch.load(checkpoint, map_location=device))
        probs, labels = predict_proba(model, test_loader, device)
        fold_probs.append(probs)
    ensemble_probs = np.mean(fold_probs, axis=0)
    metrics = {
        "spearman": float(spearmanr(labels, ensemble_probs).statistic),
        "pearson": float(pearsonr(labels, ensemble_probs).statistic),
        "roc_auc": float(roc_auc_score(labels, ensemble_probs)),
        "average_precision": float(average_precision_score(labels, ensemble_probs)),
    }
    pd.DataFrame({"label": labels, "score": ensemble_probs}).to_csv(args.output_dir / "ensemble_predictions.csv", index=False)
    pd.DataFrame([metrics]).to_csv(args.output_dir / "ensemble_metrics.csv", index=False)
    return metrics


def parse_args():
    parser = argparse.ArgumentParser(description="Train DeepCas12a with fixed k-fold validation partitions.")
    parser.add_argument("--train-data", default="Dataset/train_HT1-1_plus_HEK_in_situ.txt")
    parser.add_argument("--test-data", default="Dataset/HT1-2_test.txt")
    parser.add_argument("--partitions-csv", default="splits/deepcas12a_9fold_partitions.csv")
    parser.add_argument("--output-dir", type=Path, default=Path("results/deepcas12a"))
    parser.add_argument("--n-splits", type=int, default=9)
    parser.add_argument("--epochs", type=int, default=70)
    parser.add_argument("--batch-size", type=int, default=256)
    parser.add_argument("--learning-rate", type=float, default=2.001718570896886e-4)
    parser.add_argument("--weight-decay", type=float, default=1e-4)
    parser.add_argument("--patience", type=int, default=10)
    parser.add_argument("--min-delta", type=float, default=0.0)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--embed-dim", type=int, default=256)
    parser.add_argument("--depth", type=int, default=10)
    parser.add_argument("--num-heads", type=int, default=12)
    parser.add_argument("--mlp-ratio", type=float, default=2.4453125)
    parser.add_argument("--dropout", type=float, default=0.3070070756414809)
    parser.add_argument("--attention-dropout", type=float, default=0.27131834758785345)
    return parser.parse_args()


def main():
    args = parse_args()
    set_seed(args.seed)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    x, y = load_dataset(args.train_data)
    fold_results = [train_one_fold(args, fold, x, y, device) for fold in range(1, args.n_splits + 1)]
    metrics = evaluate_ensemble(args, device)
    (args.output_dir / "run_config.json").write_text(json.dumps(vars(args), indent=2, default=str) + "\n")
    pd.DataFrame(fold_results).to_csv(args.output_dir / "fold_results.csv", index=False)
    print(json.dumps(metrics, indent=2))


if __name__ == "__main__":
    main()
