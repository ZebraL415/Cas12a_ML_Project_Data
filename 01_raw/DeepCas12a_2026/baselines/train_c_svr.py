import argparse
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import joblib
import numpy as np
import pandas as pd
import tensorflow as tf
from scipy.stats import pearsonr, spearmanr
from sklearn.metrics import average_precision_score, precision_recall_curve, roc_auc_score, roc_curve
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVR
from tensorflow import keras
from tensorflow.keras import Sequential
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.layers import Conv1D, Dense, Dropout, Flatten, MaxPooling1D


def set_seed(seed):
    random.seed(seed)
    np.random.seed(seed)
    tf.random.set_seed(seed)


def load_data(path):
    df = pd.read_csv(path, sep=r"\s+", header=None)
    return df.iloc[:, 0].astype(str).to_numpy(), df.iloc[:, -1].astype(int).to_numpy()


def one_hot_encode(sequences):
    mapping = {"A": [1, 0, 0, 0], "T": [0, 1, 0, 0], "G": [0, 0, 1, 0], "C": [0, 0, 0, 1]}
    return np.array([[mapping.get(nt, [0, 0, 0, 0]) for nt in seq] for seq in sequences])


def build_cnn():
    model = Sequential(
        [
            Conv1D(filters=128, kernel_size=7, activation="relu", input_shape=(34, 4)),
            MaxPooling1D(pool_size=2),
            Conv1D(filters=64, kernel_size=7, activation="relu"),
            MaxPooling1D(pool_size=2),
            Flatten(),
            Dense(64, activation="relu"),
            Dense(40, activation="relu"),
            Dense(40, activation="relu"),
            Dense(28, activation="relu"),
            Dropout(0.15),
            Dense(1, activation="sigmoid"),
        ]
    )
    model.compile(optimizer=keras.optimizers.Adam(learning_rate=5e-4), loss="binary_crossentropy", metrics=["accuracy"])
    return model


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
    parser = argparse.ArgumentParser(description="Train the C-SVR reproduction baseline.")
    parser.add_argument("--train-data", default="Dataset/train_HT1-1_plus_HEK_in_situ.txt")
    parser.add_argument("--test-data", default="Dataset/HT1-2_test.txt")
    parser.add_argument("--output-dir", type=Path, default=Path("results/baselines/c_svr"))
    parser.add_argument("--epochs", type=int, default=50)
    parser.add_argument("--batch-size", type=int, default=16)
    parser.add_argument("--validation-size", type=float, default=0.2)
    parser.add_argument("--seed", type=int, default=42)
    return parser.parse_args()


def main():
    args = parse_args()
    set_seed(args.seed)
    args.output_dir.mkdir(parents=True, exist_ok=True)

    train_sequences, train_labels = load_data(args.train_data)
    test_sequences, test_labels = load_data(args.test_data)
    x_train_full = one_hot_encode(train_sequences)
    x_test = one_hot_encode(test_sequences)

    x_train, x_val, y_train, y_val = train_test_split(
        x_train_full,
        train_labels,
        test_size=args.validation_size,
        random_state=args.seed,
        stratify=train_labels,
    )
    cnn = build_cnn()
    early_stopping = EarlyStopping(monitor="val_loss", patience=5, restore_best_weights=True)
    cnn.fit(
        x_train,
        y_train,
        epochs=args.epochs,
        batch_size=args.batch_size,
        validation_data=(x_val, y_val),
        callbacks=[early_stopping],
        verbose=1,
    )
    cnn.save(args.output_dir / "cnn_model.keras")

    extractor = keras.Model(inputs=cnn.inputs, outputs=cnn.layers[-3].output)
    train_features = extractor.predict(x_train, verbose=0)
    test_features = extractor.predict(x_test, verbose=0)
    scaler = StandardScaler()
    train_features = scaler.fit_transform(train_features)
    test_features = scaler.transform(test_features)

    svr = SVR(C=1.0, gamma="scale", epsilon=0.1)
    svr.fit(train_features, y_train)
    scores = svr.predict(test_features)

    joblib.dump(scaler, args.output_dir / "scaler.joblib")
    joblib.dump(svr, args.output_dir / "svr_model.joblib")
    pd.DataFrame({"label": test_labels, "score": scores}).to_csv(args.output_dir / "predictions.csv", index=False)
    print(evaluate(test_labels, scores, args.output_dir))


if __name__ == "__main__":
    main()
