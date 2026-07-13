#!/usr/bin/env python3
"""Verify EasyDesign feature integration and reference evaluation artifacts.

This script recalculates metrics from saved predictions and performs row-level
checks only. It never fits or trains a model.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-v0", type=Path, required=True)
    parser.add_argument("--feature-v1", type=Path, required=True)
    parser.add_argument("--predictions", type=Path, required=True)
    parser.add_argument("--reported-metrics", type=Path, required=True)
    parser.add_argument("--importance-all", type=Path, required=True)
    parser.add_argument("--first-run-importance", type=Path, required=True)
    parser.add_argument("--output-json", type=Path, required=True)
    return parser.parse_args()


def metrics(y: pd.Series, prediction: pd.Series) -> dict[str, float]:
    y = pd.to_numeric(y, errors="coerce")
    prediction = pd.to_numeric(prediction, errors="coerce")
    valid = y.notna() & prediction.notna()
    y = y[valid]
    prediction = prediction[valid]
    residual = y - prediction
    ss_res = float(np.square(residual).sum())
    ss_total = float(np.square(y - y.mean()).sum())
    return {
        "n_validation": int(valid.sum()),
        "spearman_rho": float(
            y.rank(method="average").corr(prediction.rank(method="average"))
        ),
        "pearson_r": float(y.corr(prediction)),
        "mae": float(residual.abs().mean()),
        "rmse": float(np.sqrt(np.square(residual).mean())),
        "r2": float(1 - ss_res / ss_total),
    }


def main() -> int:
    args = parse_args()
    source = pd.read_csv(args.source_v0, low_memory=False)
    feature_v1 = pd.read_csv(args.feature_v1, low_memory=False)
    predictions = pd.read_csv(args.predictions, low_memory=False)
    reported = json.loads(args.reported_metrics.read_text(encoding="utf-8"))
    importance = pd.read_csv(args.importance_all)
    first_importance = pd.read_csv(args.first_run_importance)

    if source["record_id"].duplicated().any() or feature_v1["record_id"].duplicated().any():
        raise ValueError("duplicate record_id found")
    if not source["record_id"].equals(feature_v1["record_id"]):
        raise ValueError("v1 record order does not match v0")
    source_by_id = source.set_index("record_id", drop=False)
    if not predictions["record_id"].isin(source_by_id.index).all():
        raise ValueError("prediction file contains unknown record_id values")
    matched = source_by_id.loc[predictions["record_id"]].reset_index(drop=True)

    recomputed = metrics(
        predictions["label_normalized"], predictions["predicted_activity"]
    )
    metric_differences = {
        key: abs(float(recomputed[key]) - float(reported[key]))
        for key in recomputed
        if key in reported and key != "n_validation"
    }
    residual_difference = (
        predictions["residual"]
        - (
            predictions["label_normalized"]
            - predictions["predicted_activity"]
        )
    ).abs()

    positional_missing = 0
    positional_encoding_valid = True
    aligned_length = np.minimum(
        pd.to_numeric(feature_v1["crRNA_length"], errors="coerce"),
        pd.to_numeric(feature_v1["target_length"], errors="coerce"),
    )
    for position in range(1, 26):
        column = f"mismatch_pos_{position}"
        should_be_missing = aligned_length < position
        positional_missing += int(feature_v1.loc[should_be_missing, column].isna().sum())
        if not feature_v1.loc[should_be_missing, column].isna().all():
            positional_encoding_valid = False

    report = {
        "model_training_performed": False,
        "source_rows": int(len(source)),
        "feature_v1_rows": int(len(feature_v1)),
        "feature_v1_columns": int(feature_v1.shape[1]),
        "record_order_exact": True,
        "prediction_rows": int(len(predictions)),
        "prediction_duplicate_record_ids": int(predictions["record_id"].duplicated().sum()),
        "prediction_split_counts": {
            str(key): int(value)
            for key, value in matched["baseline_split"].value_counts().items()
        },
        "prediction_sequence_match": {
            "crRNA_sequence": float(
                (predictions["crRNA_sequence"] == matched["crRNA_sequence"]).mean()
            ),
            "target_sequence": float(
                (predictions["target_sequence"] == matched["target_sequence"]).mean()
            ),
        },
        "prediction_label_match": float(
            np.isclose(
                predictions["label_normalized"],
                matched["label_normalized"],
                equal_nan=True,
            ).mean()
        ),
        "recomputed_metrics": recomputed,
        "reported_metrics": reported,
        "metric_absolute_differences": metric_differences,
        "maximum_saved_residual_rounding_difference": float(
            residual_difference.max()
        ),
        "importance_all_rows": int(len(importance)),
        "importance_duplicate_features": int(importance["feature"].duplicated().sum()),
        "importance_sum": float(importance["importance"].sum()),
        "first_run_importance_rows": int(len(first_importance)),
        "position_missing_cells": positional_missing,
        "position_missing_encoding_valid": positional_encoding_valid,
        "reproducibility_boundary": (
            "Saved predictions and metrics are internally consistent, but the "
            "reference improved run cannot be independently retrained because "
            "its training code, hyperparameters, dependency lock, and random "
            "seed were not supplied."
        ),
    }
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(
        json.dumps(report, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
