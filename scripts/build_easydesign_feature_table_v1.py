#!/usr/bin/env python3
"""Build the audited EasyDesign feature table v1 from v0 and Xu's output.

The script preserves every v0 provenance/label column, verifies row-level
identity against the full engineered table, and appends a compact set of
model-agnostic features. It does not train a model or mix label systems.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd


POSITION_FEATURES = [f"mismatch_pos_{position}" for position in range(1, 26)]
MISMATCH_TYPE_FEATURES = [
    f"mismatch_type_{guide}_to_{target}"
    for guide in "ACGT"
    for target in "ACGT"
    if guide != target
]

CORE_PAIRWISE_FEATURES = [
    "mismatch_count_shared_positions",
    "mismatch_fraction_shared_positions",
    "first_mismatch_position",
    "last_mismatch_position",
    "longest_consecutive_match",
    "longest_consecutive_mismatch",
    "guide_target_gc_difference",
]

SELECTED_SEQUENCE_FEATURES = [
    "guide_entropy",
    "target_entropy",
    "guide_longest_homopolymer",
    "target_longest_homopolymer",
    "guide_gc_first_5",
    "guide_gc_first_half",
    "guide_gc_second_half",
    "target_gc_first_5",
    "target_gc_first_half",
    "target_gc_second_half",
    "guide_trinuc_TTT",
    "target_trinuc_TTT",
    "guide_trinuc_AAA",
    "guide_dinuc_GA",
    "guide_dinuc_GT",
    "guide_dinuc_AG",
]

SELECTED_FEATURES = (
    CORE_PAIRWISE_FEATURES
    + POSITION_FEATURES
    + MISMATCH_TYPE_FEATURES
    + SELECTED_SEQUENCE_FEATURES
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-v0", type=Path, required=True)
    parser.add_argument("--engineered-full", type=Path, required=True)
    parser.add_argument("--feature-dictionary", type=Path, required=True)
    parser.add_argument("--importance-all", type=Path, required=True)
    parser.add_argument("--output-table", type=Path, required=True)
    parser.add_argument("--output-manifest", type=Path, required=True)
    parser.add_argument("--output-qc", type=Path, required=True)
    return parser.parse_args()


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def require_columns(df: pd.DataFrame, columns: list[str], table: str) -> None:
    missing = sorted(set(columns) - set(df.columns))
    if missing:
        raise ValueError(f"{table} is missing required columns: {missing}")


def importance_name_map() -> dict[str, str]:
    mapping = {
        "eng_mismatch_count": "mismatch_count_validated",
        "eng_match_fraction": "match_fraction_shared_positions",
        "eng_mismatch_fraction": "mismatch_fraction_shared_positions",
        "eng_first_mismatch_pos": "first_mismatch_position",
        "eng_last_mismatch_pos": "last_mismatch_position",
        "eng_longest_match": "longest_consecutive_match",
        "eng_longest_mismatch": "longest_consecutive_mismatch",
        "eng_gc_difference": "guide_target_gc_difference",
        "eng_aligned_length": "aligned_length",
        "eng_length_difference": "length_difference",
        "target_len_eng": "target_length_engineered",
        "guide_gc_eng": "guide_gc_content_engineered",
        "target_gc_eng": "target_gc_content_engineered",
        # These names are used only for reference-result reconciliation. The
        # supplied generator calls them generic thirds, not biological zones.
        "eng_mismatch_count_proximal": "mismatch_count_first_third",
        "eng_mismatch_fraction_proximal": "mismatch_fraction_first_third",
        "eng_mismatch_count_middle": "mismatch_count_middle_third",
        "eng_mismatch_fraction_middle": "mismatch_fraction_middle_third",
        "eng_mismatch_count_distal": "mismatch_count_last_third",
        "eng_mismatch_fraction_distal": "mismatch_fraction_last_third",
    }
    for position in range(1, 31):
        mapping[f"eng_mismatch_pos_{position}"] = f"mismatch_pos_{position}"
    for guide in "ACGT":
        for target in "ACGT":
            if guide != target:
                mapping[
                    f"eng_mismatch_type_{guide}_to_{target}"
                ] = f"mismatch_type_{guide}_to_{target}"
    return mapping


def exclusion_reason(feature: str) -> tuple[str, str]:
    if feature in {
        "selected_alignment_mode",
        "computational_validation_status",
        "biological_source_validation_status",
    }:
        return (
            "常量或审计元数据，不作为模型特征。",
            "Constant or audit metadata; not a model feature.",
        )
    if feature.startswith("cleaned_") or feature == "transformed_target_sequence":
        return (
            "与 v0 中已保留的序列字段重复，仅用于审计。",
            "Duplicates sequence fields retained in v0 and is audit-only.",
        )
    if feature == "mismatch_count_validated":
        return (
            "与现有 guide_target_hamming_dist_computed 完全相同。",
            "Exactly duplicates guide_target_hamming_dist_computed.",
        )
    if feature == "match_fraction_shared_positions":
        return (
            "与 mismatch_fraction_shared_positions 互为 1 的补数。",
            "Equals 1 minus mismatch_fraction_shared_positions.",
        )
    if feature in {
        "aligned_length",
        "length_difference",
        "guide_length_engineered",
        "target_length_engineered",
        "guide_gc_content_engineered",
        "target_gc_content_engineered",
    }:
        return (
            "与 v0 的长度或 GC 字段重复或可由其精确推出。",
            "Duplicates or is exactly derivable from a length or GC field already present in v0.",
        )
    if "_third" in feature:
        return (
            "脚本仅按三等分计算；尚不能解释为 PAM proximal/seed/distal。",
            "Computed as generic thirds and not yet interpretable as PAM-proximal, seed, or distal biology.",
        )
    if feature.startswith("mismatch_pos_"):
        return (
            "位置超过本数据集 25 nt 最大对齐长度。",
            "Position exceeds this dataset's maximum 25-nt alignment.",
        )
    if "dinuc" in feature or "trinuc" in feature:
        return (
            "为保持 v1 紧凑，本轮仅保留参考重要性支持的少量 k-mer。",
            "Excluded to keep v1 compact; only a small importance-supported k-mer subset is retained.",
        )
    return (
        "可复算但本轮缺少足够的独立重要性或解释性证据。",
        "Recomputable but lacks sufficient independent importance or interpretability evidence for this compact v1.",
    )


def main() -> int:
    args = parse_args()
    source = pd.read_csv(args.source_v0, low_memory=False)
    engineered = pd.read_csv(args.engineered_full, low_memory=False)
    dictionary = pd.read_csv(args.feature_dictionary, low_memory=False)
    importance = pd.read_csv(args.importance_all, low_memory=False)

    require_columns(
        source,
        [
            "record_id",
            "baseline_split",
            "crRNA_sequence",
            "target_sequence",
            "label_normalized",
        ],
        "source v0",
    )
    require_columns(
        engineered,
        [
            "record_id",
            "crRNA_sequence",
            "target_sequence",
            "label_normalized",
            *SELECTED_FEATURES,
        ],
        "engineered table",
    )
    require_columns(importance, ["feature", "importance"], "importance table")

    if source["record_id"].duplicated().any():
        raise ValueError("source v0 contains duplicate record_id values")
    if engineered["record_id"].duplicated().any():
        raise ValueError("engineered table contains duplicate record_id values")
    if len(source) != len(engineered):
        raise ValueError("source and engineered row counts differ")
    if not source["record_id"].equals(engineered["record_id"]):
        raise ValueError("record_id order differs between source and engineered tables")

    for column in [
        "crRNA_sequence",
        "target_sequence",
        "label_normalized",
        "baseline_split",
    ]:
        left = source[column].fillna("").astype(str)
        right = engineered[column].fillna("").astype(str)
        if not left.equals(right):
            raise ValueError(f"row-level mismatch in {column}")

    curated = engineered[SELECTED_FEATURES].copy()
    aligned_length = pd.to_numeric(
        engineered["aligned_length"], errors="coerce"
    )
    corrected_unaligned_cells = 0
    for position in range(1, 26):
        column = f"mismatch_pos_{position}"
        unaligned = aligned_length < position
        corrected_unaligned_cells += int(unaligned.sum())
        curated.loc[unaligned, column] = pd.NA
        curated[column] = curated[column].astype("Int64")

    output_df = source.copy()
    output_df.insert(1, "feature_table_version", "EasyDesign_2024_feature_table_v1")
    for column in SELECTED_FEATURES:
        output_df[column] = curated[column]

    mapping = importance_name_map()
    importance = importance.copy()
    importance["generator_feature"] = importance["feature"].map(mapping).fillna(
        importance["feature"]
    )
    importance["reference_rank"] = np.arange(1, len(importance) + 1)
    importance_lookup = (
        importance.sort_values("reference_rank")
        .drop_duplicates("generator_feature")
        .set_index("generator_feature")
    )

    dictionary_lookup = (
        dictionary.drop_duplicates("feature").set_index("feature")
        if "feature" in dictionary.columns
        else pd.DataFrame()
    )
    identifier_columns = {
        "dataset_id",
        "source_id",
        "source_table_id",
        "record_id",
        "paper_split",
        "baseline_split",
        "data_role",
        "crRNA_sequence",
        "target_sequence",
        "target_context_sequence",
        "pam",
        "label_raw_name",
        "label_raw_value",
        "label_normalized",
        "label_scale_group",
        "label_is_primary_baseline",
    }
    engineered_feature_columns = [
        column for column in engineered.columns if column not in identifier_columns
    ]
    manifest_rows = []
    for feature in engineered_feature_columns:
        included = feature in SELECTED_FEATURES
        if included:
            reason_zh = "通过复算；具有可解释性，并由参考重要性结果或特征家族完整性支持。"
            reason_en = "Recomputed successfully; interpretable and supported by reference importance or feature-family completeness."
        else:
            reason_zh, reason_en = exclusion_reason(feature)

        reference_name = ""
        reference_importance = ""
        reference_rank = ""
        if feature in importance_lookup.index:
            row = importance_lookup.loc[feature]
            reference_name = row["feature"]
            reference_importance = float(row["importance"])
            reference_rank = int(row["reference_rank"])

        dictionary_row = (
            dictionary_lookup.loc[feature]
            if not dictionary_lookup.empty and feature in dictionary_lookup.index
            else None
        )
        manifest_rows.append(
            {
                "feature": feature,
                "included_in_feature_table_v1": "yes" if included else "no",
                "category": "" if dictionary_row is None else dictionary_row.get("category", ""),
                "meaning": "" if dictionary_row is None else dictionary_row.get("meaning", ""),
                "calculation": "" if dictionary_row is None else dictionary_row.get("calculation", ""),
                "generator_validation_status": "" if dictionary_row is None else dictionary_row.get("validation_status", ""),
                "reference_feature_name": reference_name,
                "reference_importance": reference_importance,
                "reference_rank": reference_rank,
                "selection_reason_zh": reason_zh,
                "selection_reason_en": reason_en,
            }
        )

    manifest = pd.DataFrame(manifest_rows)
    args.output_table.parent.mkdir(parents=True, exist_ok=True)
    args.output_manifest.parent.mkdir(parents=True, exist_ok=True)
    args.output_qc.parent.mkdir(parents=True, exist_ok=True)
    output_df.to_csv(args.output_table, index=False, encoding="utf-8-sig")
    manifest.to_csv(args.output_manifest, index=False, encoding="utf-8-sig")

    hamming_match = np.isclose(
        pd.to_numeric(source["guide_target_hamming_dist_computed"], errors="coerce"),
        pd.to_numeric(engineered["mismatch_count_validated"], errors="coerce"),
        equal_nan=True,
    )
    qc = {
        "source_v0": str(args.source_v0),
        "engineered_full": str(args.engineered_full),
        "output_table": str(args.output_table),
        "source_v0_sha256": sha256(args.source_v0),
        "engineered_full_sha256": sha256(args.engineered_full),
        "rows": int(len(output_df)),
        "columns": int(output_df.shape[1]),
        "selected_engineered_features": len(SELECTED_FEATURES),
        "duplicate_record_ids": int(output_df["record_id"].duplicated().sum()),
        "split_counts": {
            str(key): int(value)
            for key, value in output_df["baseline_split"].value_counts(dropna=False).items()
        },
        "record_order_exact": True,
        "hamming_exact_agreement": float(hamming_match.mean()),
        "unaligned_position_cells_changed_from_zero_to_missing": corrected_unaligned_cells,
        "label_system": "diagnostic_activity",
        "model_training_performed": False,
    }
    args.output_qc.write_text(
        json.dumps(qc, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(json.dumps(qc, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
