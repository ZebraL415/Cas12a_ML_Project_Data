import argparse
import sys
import warnings
from itertools import product
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import joblib
import numpy as np
import pandas as pd
from scipy.stats import pearsonr, spearmanr
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import average_precision_score, precision_recall_curve, roc_auc_score, roc_curve
from sklearn.svm import SVC
from tqdm import tqdm

try:
    import RNA
except ImportError:
    RNA = None

try:
    from Bio.Seq import Seq
    from Bio.SeqUtils import MeltingTemp as mt
except ImportError:
    Seq = None
    mt = None


def load_data(path):
    df = pd.read_csv(path, sep=r"\s+", header=None)
    return df.iloc[:, 0].astype(str).to_numpy(), df.iloc[:, -1].astype(int).to_numpy()


def position_specific_encoding(seq):
    mapping = {"A": [1, 0, 0, 0], "C": [0, 1, 0, 0], "G": [0, 0, 1, 0], "T": [0, 0, 0, 1]}
    one_hot = np.array([mapping[nuc] for nuc in seq]).flatten()
    dinucs = {a + b: i for i, (a, b) in enumerate(product("ACGT", repeat=2))}
    di_features = np.zeros((len(seq) - 1) * 16)
    for i in range(len(seq) - 1):
        di_features[i * 16 + dinucs[seq[i : i + 2]]] = 1
    return np.concatenate([one_hot, di_features])


def position_non_specific_encoding(seq):
    features = []
    for k in range(1, 5):
        kmers = [seq[i : i + k] for i in range(len(seq) - k + 1)]
        for kmer in ("".join(item) for item in product("ACGT", repeat=k)):
            features.append(kmers.count(kmer))
    return np.array(features)


def repetitive_base_features(seq):
    patterns = ["AAAA", "CCCC", "GGGG", "TTTT"]
    repeat_counts = [1 if pattern in seq else 0 for pattern in patterns]
    return np.array(repeat_counts + [1 if any(repeat_counts) else 0])


def seed_region_uuu(seq):
    return np.array([1 if "TTT" in seq[:6] else 0])


def gc_content_features(seq):
    seed_gc = (seq[:6].count("G") + seq[:6].count("C")) / 6
    non_seed_gc = (seq[6:].count("G") + seq[6:].count("C")) / (len(seq) - 6)
    full_gc = (seq.count("G") + seq.count("C")) / len(seq)
    normal_gc = 1 if 0.3 <= full_gc <= 0.7 else 0
    return np.array([seed_gc, non_seed_gc, full_gc, normal_gc])


def calculate_mfe(seq):
    if RNA is None:
        return np.array([0.0])
    _, mfe = RNA.fold(seq)
    return np.array([mfe])


def melting_temperature(seq):
    if Seq is None or mt is None:
        return np.array([0.0, 0.0, 0.0])
    seq_obj = Seq(seq)
    return np.array([mt.Tm_NN(seq_obj), mt.Tm_NN(seq_obj[:6]), mt.Tm_NN(seq_obj[6:])])


def extract_features(seq):
    return np.concatenate(
        [
            position_specific_encoding(seq),
            position_non_specific_encoding(seq),
            repetitive_base_features(seq),
            seed_region_uuu(seq),
            gc_content_features(seq),
            calculate_mfe(seq),
            melting_temperature(seq),
        ]
    )


def evaluate(labels, scores, output_dir):
    fpr, tpr, _ = roc_curve(labels, scores)
    precision, recall, _ = precision_recall_curve(labels, scores)
    metrics = {
        "spearman": float(spearmanr(labels, scores).statistic),
        "pearson": float(pearsonr(labels, scores).statistic),
        "roc_auc": float(roc_auc_score(labels, scores)),
        "average_precision": float(average_precision_score(labels, scores)),
    }
    pd.DataFrame({"fpr": fpr, "tpr": tpr}).to_csv(output_dir / "roc_curve.csv", index=False)
    pd.DataFrame({"precision": precision, "recall": recall}).to_csv(output_dir / "pr_curve.csv", index=False)
    pd.DataFrame([metrics]).to_csv(output_dir / "metrics.csv", index=False)
    return metrics


def parse_args():
    parser = argparse.ArgumentParser(description="Train the CRISPR-DT reproduction baseline.")
    parser.add_argument("--train-data", default="Dataset/train_HT1-1_plus_HEK_in_situ.txt")
    parser.add_argument("--test-data", default="Dataset/HT1-2_test.txt")
    parser.add_argument("--output-dir", type=Path, default=Path("results/baselines/crispr_dt"))
    parser.add_argument("--top-features", type=int, default=150)
    parser.add_argument("--seed", type=int, default=42)
    return parser.parse_args()


def main():
    args = parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    if RNA is None:
        warnings.warn("ViennaRNA Python bindings are not installed; MFE is set to 0.0.")
    if Seq is None or mt is None:
        warnings.warn("Biopython is not installed; melting-temperature features are set to 0.0.")

    train_sequences, train_labels = load_data(args.train_data)
    test_sequences, test_labels = load_data(args.test_data)
    x_train = np.array([extract_features(seq) for seq in tqdm(train_sequences, desc="train features")])
    x_test = np.array([extract_features(seq) for seq in tqdm(test_sequences, desc="test features")])

    selector = RandomForestClassifier(n_estimators=100, random_state=args.seed)
    selector.fit(x_train, train_labels)
    top_idx = np.argsort(selector.feature_importances_)[::-1][: args.top_features]
    model = SVC(kernel="rbf", probability=True, random_state=args.seed)
    model.fit(x_train[:, top_idx], train_labels)
    scores = model.predict_proba(x_test[:, top_idx])[:, 1]

    joblib.dump(selector, args.output_dir / "random_forest_selector.joblib")
    joblib.dump(top_idx, args.output_dir / "top_features_idx.joblib")
    joblib.dump(model, args.output_dir / "svm_model.joblib")
    pd.DataFrame({"label": test_labels, "score": scores}).to_csv(args.output_dir / "predictions.csv", index=False)
    print(evaluate(test_labels, scores, args.output_dir))


if __name__ == "__main__":
    main()
