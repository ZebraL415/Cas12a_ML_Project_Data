#!/usr/bin/env python3
"""Independently verify a built EasyDesign v2.1 context feature table."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--parent", type=Path, required=True)
    parser.add_argument("--candidate", type=Path, required=True)
    parser.add_argument("--dictionary", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    parent = pd.read_csv(args.parent, low_memory=False)
    candidate = pd.read_csv(args.candidate, low_memory=False)
    dictionary = pd.read_csv(args.dictionary)
    context_names = dictionary.loc[
        dictionary["category"].eq("sequence_context"), "feature_name"
    ].tolist()
    checks = {
        "shape_11992_by_246": candidate.shape == (11992, 246),
        "parent_shape_11992_by_188": parent.shape == (11992, 188),
        "record_id_unique": bool(candidate["record_id"].is_unique),
        "row_order_unchanged": candidate["record_id"].equals(parent["record_id"]),
        "parent_columns_preserved": candidate.columns[: len(parent.columns)].tolist() == parent.columns.tolist(),
        "all_parent_values_exact": candidate[parent.columns].equals(parent),
        "58_context_dictionary_rows": len(context_names) == 58,
        "58_context_table_columns": len(set(context_names).intersection(candidate.columns)) == 58,
        "188_candidate_inputs": int(dictionary["default_model_role"].eq("candidate_input").sum()) == 188,
        "context_no_missing": not candidate[context_names].isna().any().any(),
        "context_all_finite": bool(np.isfinite(candidate[context_names].to_numpy(float)).all()),
        "target_ungapped_has_no_gap": not candidate["target_ungapped"].astype(str).str.contains("-", regex=False).any(),
        "target_aligned_25_unchanged": candidate["target_aligned_25"].equals(parent["target_aligned_25"]),
        "label_unchanged": candidate["label_normalized"].equals(parent["label_normalized"]),
        "split_unchanged": candidate["baseline_split"].equals(parent["baseline_split"]),
        "no_duplicate_columns": not candidate.columns.duplicated().any(),
    }
    result = {
        "all_passed": all(checks.values()),
        "checks": checks,
        "parent_sha256": sha256(args.parent),
        "candidate_sha256": sha256(args.candidate),
        "dictionary_sha256": sha256(args.dictionary),
    }
    args.output.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    if not result["all_passed"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
