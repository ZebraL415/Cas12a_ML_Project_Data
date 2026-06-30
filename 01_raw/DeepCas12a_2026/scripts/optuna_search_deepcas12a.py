import argparse
import json
import sys
from pathlib import Path

import optuna
import pandas as pd
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, TensorDataset

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from DeepCas12a import Episgt, VisionTransformer
from scripts.train_deepcas12a import evaluate_accuracy, load_fold_indices, set_seed


def load_dataset(path):
    data = Episgt(path, num_epi_features=2, with_y=True)
    x, y = data.get_dataset()
    return torch.tensor(x, dtype=torch.float32).unsqueeze(1), torch.tensor(y, dtype=torch.long)


def suggest_params(trial):
    embed_dim = trial.suggest_categorical("embed_dim", [64, 128, 256, 512])
    num_heads = trial.suggest_categorical("num_heads", [4, 8, 12, 16])
    if embed_dim % num_heads != 0:
        raise optuna.TrialPruned()
    return {
        "learning_rate": trial.suggest_float("learning_rate", 1e-5, 1e-3, log=True),
        "attention_dropout": trial.suggest_float("attention_dropout", 0.1, 0.5),
        "dropout": trial.suggest_float("dropout", 0.1, 0.5),
        "depth": trial.suggest_int("depth", 4, 12),
        "embed_dim": embed_dim,
        "mlp_ratio": trial.suggest_float("mlp_ratio", 1.0, 4.0),
        "num_heads": num_heads,
    }


def objective(trial, args, x, y, device):
    params = suggest_params(trial)
    train_idx, val_idx = load_fold_indices(args.partitions_csv, args.fold)
    train_loader = DataLoader(TensorDataset(x[train_idx], y[train_idx]), batch_size=args.batch_size, shuffle=True)
    val_loader = DataLoader(TensorDataset(x[val_idx], y[val_idx]), batch_size=args.batch_size, shuffle=False)

    model = VisionTransformer(
        embed_dim=params["embed_dim"],
        depth=params["depth"],
        num_heads=params["num_heads"],
        mlp_ratio=params["mlp_ratio"],
        dropout=params["dropout"],
        attention_drop=params["attention_dropout"],
    ).to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=params["learning_rate"], weight_decay=args.weight_decay)

    best_acc = 0.0
    patience_counter = 0
    for epoch in range(1, args.epochs + 1):
        model.train()
        for batch_x, batch_y in train_loader:
            batch_x = batch_x.to(device)
            batch_y = batch_y.to(device)
            optimizer.zero_grad()
            loss = criterion(model.forward_logits(batch_x), batch_y)
            loss.backward()
            optimizer.step()
        val_acc = evaluate_accuracy(model, val_loader, device)
        trial.report(val_acc, epoch)
        if trial.should_prune():
            raise optuna.TrialPruned()
        if val_acc > best_acc:
            best_acc = val_acc
            patience_counter = 0
        else:
            patience_counter += 1
        if patience_counter >= args.patience:
            break
    return best_acc


def parse_args():
    parser = argparse.ArgumentParser(description="Run the Optuna TPE hyperparameter search procedure for DeepCas12a.")
    parser.add_argument("--train-data", default="Dataset/train_HT1-1_plus_HEK_in_situ.txt")
    parser.add_argument("--partitions-csv", default="splits/deepcas12a_9fold_partitions.csv")
    parser.add_argument("--output-dir", type=Path, default=Path("results/optuna"))
    parser.add_argument("--study-name", default="deepcas12a_tpe")
    parser.add_argument("--n-trials", type=int, default=50)
    parser.add_argument("--epochs", type=int, default=30)
    parser.add_argument("--batch-size", type=int, default=256)
    parser.add_argument("--weight-decay", type=float, default=1e-4)
    parser.add_argument("--patience", type=int, default=10)
    parser.add_argument("--fold", type=int, default=1)
    parser.add_argument("--seed", type=int, default=42)
    return parser.parse_args()


def main():
    args = parse_args()
    set_seed(args.seed)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    x, y = load_dataset(args.train_data)
    sampler = optuna.samplers.TPESampler(seed=args.seed)
    study = optuna.create_study(direction="maximize", sampler=sampler, study_name=args.study_name)
    study.optimize(lambda trial: objective(trial, args, x, y, device), n_trials=args.n_trials)
    study.trials_dataframe().to_csv(args.output_dir / "optuna_trials.csv", index=False)
    (args.output_dir / "best_params.json").write_text(json.dumps(study.best_params, indent=2) + "\n")
    pd.DataFrame([{"best_value": study.best_value, **study.best_params}]).to_csv(args.output_dir / "best_params.csv", index=False)


if __name__ == "__main__":
    main()
