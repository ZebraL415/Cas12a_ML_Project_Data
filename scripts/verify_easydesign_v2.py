#!/usr/bin/env python3
"""Verify EasyDesign v2 row, alignment, label, split, and mapping invariants."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd


def check(name: str, passed: bool, detail: object) -> dict[str, object]:
    return {"check": name, "passed": bool(passed), "detail": detail}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--run-dir", type=Path)
    args = parser.parse_args()
    root = args.root.resolve()

    alignment = pd.read_csv(root / "03_cleaned_minimal/easydesign_mismatch/EasyDesign_2024_guide_target_alignment_v2.csv")
    source_map = pd.read_csv(root / "03_cleaned_minimal/easydesign_mismatch/EasyDesign_2024_source_mapping_v1.csv")
    v0 = pd.read_csv(root / "04_candidate_ml_dataset/diagnostic_activity_easydesign/EasyDesign_2024_diagnostic_activity_feature_table_v0.csv")
    v2 = pd.read_csv(
        root / "04_candidate_ml_dataset/diagnostic_activity_easydesign/EasyDesign_2024_diagnostic_activity_feature_table_v2.csv",
        low_memory=False,
    )
    dictionary = pd.read_csv(root / "04_candidate_ml_dataset/diagnostic_activity_easydesign/feature_engineering_v2/EasyDesign_2024_feature_dictionary_v2.csv")

    event_sum = alignment["substitution_count"] + alignment["gap_count_target"] + alignment["gap_count_guide"]
    positional_sum = alignment[[f"difference_pos_{position:02d}" for position in range(1, 26)]].sum(axis=1)
    table_s3_v2 = v2[v2["source_table_id"].astype(str).str.contains("TableS3")]
    table_s5_v2 = v2[v2["source_table_id"].astype(str).str.contains("TableS5")]
    no_gap = table_s3_v2[table_s3_v2["alignment_has_gap"] == "no"]
    gap = table_s3_v2[table_s3_v2["alignment_has_gap"] == "yes"]
    internal = table_s3_v2[table_s3_v2["baseline_split"].isin(["baseline_train", "baseline_validation"])]

    v0_index = v0.set_index("record_id")
    v2_index = v2.set_index("record_id")
    same_labels = v0_index["label_raw_value"].astype(float).equals(v2_index["label_raw_value"].astype(float))
    same_splits = v0_index["baseline_split"].astype(str).equals(v2_index["baseline_split"].astype(str))
    same_sources = v0_index["source_table_id"].astype(str).equals(v2_index["source_table_id"].astype(str))

    results = [
        check("alignment_row_count", len(alignment) == 10634, len(alignment)),
        check("alignment_record_id_unique", alignment["record_id"].is_unique, alignment["record_id"].nunique()),
        check("alignment_lengths_25", bool((alignment["target_alignment_length"] == 25).all()), alignment["target_alignment_length"].value_counts().to_dict()),
        check("guide_lengths_25", bool((alignment["guide_length"] == 25).all()), alignment["guide_length"].value_counts().to_dict()),
        check("gap_row_count", int((alignment["alignment_has_gap"] == "yes").sum()) == 740, int((alignment["alignment_has_gap"] == "yes").sum())),
        check("no_gap_row_count", int((alignment["alignment_has_gap"] == "no").sum()) == 9894, int((alignment["alignment_has_gap"] == "no").sum())),
        check("gap_ungapped_length_distribution", alignment[alignment["alignment_has_gap"] == "yes"]["target_ungapped_length"].value_counts().sort_index().to_dict() == {17: 4, 18: 2, 23: 47, 24: 687}, alignment[alignment["alignment_has_gap"] == "yes"]["target_ungapped_length"].value_counts().sort_index().to_dict()),
        check("event_count_invariant", bool((event_sum == alignment["aligned_difference_count"]).all()), int((event_sum != alignment["aligned_difference_count"]).sum())),
        check("position_count_invariant", bool((positional_sum == alignment["aligned_difference_count"]).all()), int((positional_sum != alignment["aligned_difference_count"]).sum())),
        check("raw_hamming_disagreement_count", int((alignment["raw_hamming_agreement"] == "no").sum()) == 188, int((alignment["raw_hamming_agreement"] == "no").sum())),
        check("source_map_one_row_per_record", len(source_map) == 10634 and source_map["record_id"].is_unique, {"rows": len(source_map), "unique": source_map["record_id"].nunique()}),
        check("source_map_hit_coverage", int((source_map["mapping_hit_count"] > 0).sum()) >= 10617, int((source_map["mapping_hit_count"] > 0).sum())),
        check("v2_row_count_matches_v0", len(v2) == len(v0) == 11992, {"v0": len(v0), "v2": len(v2)}),
        check("v2_record_id_unique", v2["record_id"].is_unique, v2["record_id"].nunique()),
        check("v2_table_s3_count", len(table_s3_v2) == 10634, len(table_s3_v2)),
        check("v2_table_s5_count", len(table_s5_v2) == 1358, len(table_s5_v2)),
        check("labels_unchanged", same_labels, same_labels),
        check("splits_unchanged", same_splits, same_splits),
        check("source_tables_unchanged", same_sources, same_sources),
        check("core_eligibility_count", int((v2["default_training_eligibility"] == "eligible_core_v2").sum()) == 9894, int((v2["default_training_eligibility"] == "eligible_core_v2").sum())),
        check("conditional_gap_count", int((v2["default_training_eligibility"] == "conditional_gap_aware_v2").sum()) == 740, int((v2["default_training_eligibility"] == "conditional_gap_aware_v2").sum())),
        check("external_test_count", int((v2["default_training_eligibility"] == "external_test_only_scale_unconfirmed").sum()) == 1358, int((v2["default_training_eligibility"] == "external_test_only_scale_unconfirmed").sum())),
        check("no_gap_legacy_hamming_agreement", bool((no_gap["guide_target_hamming_dist_computed"] == no_gap["guide_target_hamming_dist_computed_v0_legacy"]).all()), int((no_gap["guide_target_hamming_dist_computed"] != no_gap["guide_target_hamming_dist_computed_v0_legacy"]).sum())),
        check("gap_alignment_preserved", bool(gap["target_aligned_25"].astype(str).str.contains("-", regex=False).all()), int(gap["target_aligned_25"].astype(str).str.contains("-", regex=False).sum())),
        check("pair_split_no_leakage", int((internal.groupby("guide_target_pair_id")["baseline_split"].nunique() > 1).sum()) == 0, int((internal.groupby("guide_target_pair_id")["baseline_split"].nunique() > 1).sum())),
        check("feature_dictionary_names_unique", dictionary["feature_name"].is_unique, dictionary["feature_name"].nunique()),
    ]
    failed = [item for item in results if not item["passed"]]
    report = {"status": "pass" if not failed else "fail", "checks": results, "failed_check_count": len(failed)}
    if args.run_dir:
        args.run_dir.mkdir(parents=True, exist_ok=True)
        (args.run_dir / "verification_results.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
