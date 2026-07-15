#!/usr/bin/env python3
"""Build the model-agnostic EasyDesign diagnostic activity feature table v2."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
from pathlib import Path
from typing import Any

import pandas as pd


V0_REL = Path("04_candidate_ml_dataset/diagnostic_activity_easydesign/EasyDesign_2024_diagnostic_activity_feature_table_v0.csv")
ALIGNMENT_REL = Path("03_cleaned_minimal/easydesign_mismatch/EasyDesign_2024_guide_target_alignment_v2.csv")
SOURCE_MAP_REL = Path("03_cleaned_minimal/easydesign_mismatch/EasyDesign_2024_source_mapping_v1.csv")
OUTPUT_REL = Path("04_candidate_ml_dataset/diagnostic_activity_easydesign/EasyDesign_2024_diagnostic_activity_feature_table_v2.csv")
FEATURE_DIR_REL = Path("04_candidate_ml_dataset/diagnostic_activity_easydesign/feature_engineering_v2")


def clean_sequence(value: Any, keep_gap: bool = False) -> str:
    text = "" if pd.isna(value) else str(value).upper()
    allowed = r"[^ACGTRYSWKMBDHVN-]" if keep_gap else r"[^ACGTRYSWKMBDHVN]"
    return re.sub(allowed, "", text)


def stable_pair_id(guide: str, target_aligned: str) -> str:
    token = hashlib.sha1(f"{guide}|{target_aligned}".encode("utf-8")).hexdigest()[:16]
    return f"EasyDesign_2024_pair_{token}"


def safe_float(value: Any) -> float | None:
    try:
        if pd.isna(value):
            return None
        return float(value)
    except (TypeError, ValueError):
        return None


def entropy(seq: str) -> float | None:
    seq = "".join(base for base in seq if base in "ACGT")
    if not seq:
        return None
    value = 0.0
    for base in "ACGT":
        fraction = seq.count(base) / len(seq)
        if fraction:
            value -= fraction * math.log2(fraction)
    return round(value, 6)


def longest_homopolymer(seq: str) -> int:
    seq = "".join(base for base in seq if base in "ACGT")
    if not seq:
        return 0
    longest = current = 1
    for previous, current_base in zip(seq, seq[1:]):
        current = current + 1 if current_base == previous else 1
        longest = max(longest, current)
    return longest


def longest_run(values: list[bool]) -> int:
    longest = current = 0
    for value in values:
        current = current + 1 if value else 0
        longest = max(longest, current)
    return longest


def base_features(prefix: str, seq: str) -> dict[str, Any]:
    acgt = "".join(base for base in seq if base in "ACGT")
    result: dict[str, Any] = {
        f"{prefix}_length_acgt": len(acgt),
        f"{prefix}_gc_content": round((acgt.count("G") + acgt.count("C")) / len(acgt), 6) if acgt else None,
        f"{prefix}_shannon_entropy": entropy(acgt),
        f"{prefix}_longest_homopolymer": longest_homopolymer(acgt),
    }
    for base in "ACGT":
        result[f"{prefix}_{base.lower()}_fraction"] = round(acgt.count(base) / len(acgt), 6) if acgt else None
    return result


def pair_features(guide: str, target_aligned: str) -> dict[str, Any]:
    events: list[str] = []
    substitutions: dict[str, int] = {f"sub_{a}_to_{b}_count": 0 for a in "ACGT" for b in "ACGT" if a != b}
    result: dict[str, Any] = {}
    for index in range(25):
        guide_base = guide[index] if index < len(guide) else ""
        target_base = target_aligned[index] if index < len(target_aligned) else ""
        if not guide_base or not target_base:
            event = "unresolved"
        elif guide_base == "-" and target_base != "-":
            event = "gap_in_guide"
        elif target_base == "-" and guide_base != "-":
            event = "gap_in_target"
        elif guide_base not in "ACGT" or target_base not in "ACGT":
            event = "unresolved"
        elif guide_base == target_base:
            event = "match"
        else:
            event = "substitution"
            substitutions[f"sub_{guide_base}_to_{target_base}_count"] += 1
        events.append(event)
        result[f"difference_pos_{index + 1:02d}"] = int(event in {"substitution", "gap_in_target", "gap_in_guide"})
        result[f"substitution_pos_{index + 1:02d}"] = int(event == "substitution")
        result[f"target_gap_pos_{index + 1:02d}"] = int(event == "gap_in_target")

    differences = [event in {"substitution", "gap_in_target", "gap_in_guide"} for event in events]
    positions = [index + 1 for index, value in enumerate(differences) if value]
    result.update(substitutions)
    result.update(
        {
            "aligned_difference_count": sum(differences),
            "substitution_count": events.count("substitution"),
            "gap_count_target": events.count("gap_in_target"),
            "gap_count_guide": events.count("gap_in_guide"),
            "unresolved_alignment_position_count": events.count("unresolved"),
            "pam_difference_count": sum(differences[:4]),
            "spacer_difference_count": sum(differences[4:]),
            "first_difference_position_1based": min(positions) if positions else None,
            "last_difference_position_1based": max(positions) if positions else None,
            "longest_match_run": longest_run([event == "match" for event in events]),
            "longest_substitution_run": longest_run([event == "substitution" for event in events]),
            "longest_target_gap_run": longest_run([event == "gap_in_target" for event in events]),
            "position_event_string": ";".join(f"{i + 1}:{event}" for i, event in enumerate(events) if event != "match"),
        }
    )
    return result


def feature_dictionary() -> pd.DataFrame:
    rows: list[dict[str, str]] = []

    def add(name: str, category: str, inputs: str, formula: str, gap_behavior: str, role: str, notes: str = "") -> None:
        rows.append(
            {
                "feature_name": name,
                "category": category,
                "input_fields": inputs,
                "formula_or_definition": formula,
                "gap_behavior": gap_behavior,
                "default_model_role": role,
                "leakage_risk": "none_known" if role == "candidate_input" else "exclude_or_metadata",
                "notes": notes,
            }
        )

    for name in (
        "target_aligned_25",
        "target_ungapped",
        "alignment_has_gap",
        "alignment_event_status",
        "alignment_qc_status",
        "default_training_eligibility",
    ):
        add(name, "alignment_or_qc", "guide_seq; target_at_guide", "See build script and source-preserving alignment rules.", "preserved", "metadata_only")
    for name in (
        "aligned_difference_count",
        "substitution_count",
        "gap_count_target",
        "gap_count_guide",
        "pam_difference_count",
        "spacer_difference_count",
        "first_difference_position_1based",
        "last_difference_position_1based",
        "longest_match_run",
        "longest_substitution_run",
        "longest_target_gap_run",
    ):
        add(name, "pair_alignment", "crRNA_sequence; target_aligned_25", "Direct 25-position guide-to-target comparison.", "gap is a separate event", "candidate_input")
    for position in range(1, 26):
        add(f"difference_pos_{position:02d}", "pair_position", "crRNA_sequence; target_aligned_25", f"1 if aligned position {position} is substitution or gap, else 0.", "gap contributes 1", "candidate_input")
        add(f"substitution_pos_{position:02d}", "pair_position", "crRNA_sequence; target_aligned_25", f"1 if aligned position {position} is an A/C/G/T substitution.", "gap contributes 0", "candidate_input")
        add(f"target_gap_pos_{position:02d}", "pair_position", "target_aligned_25", f"1 if aligned target position {position} is '-'.", "explicit target-channel gap", "candidate_input")
    for guide_base in "ACGT":
        for target_base in "ACGT":
            if guide_base != target_base:
                add(
                    f"sub_{guide_base}_to_{target_base}_count",
                    "substitution_type",
                    "crRNA_sequence; target_aligned_25",
                    f"Count of direct-orientation {guide_base}-to-{target_base} substitutions.",
                    "gaps excluded",
                    "candidate_input",
                )
    for prefix, source in (
        ("guide", "crRNA_sequence"),
        ("target_ungapped", "target_ungapped"),
        ("guide_spacer", "crRNA_sequence positions 5-25"),
        ("target_spacer_ungapped", "target_aligned_25 positions 5-25 with gaps removed"),
    ):
        for suffix in ("length_acgt", "gc_content", "shannon_entropy", "longest_homopolymer", "a_fraction", "c_fraction", "g_fraction", "t_fraction"):
            add(f"{prefix}_{suffix}", "sequence_composition", source, suffix.replace("_", " "), "computed after removing gaps", "candidate_input")
    for name in (
        "mapping_status",
        "mapping_confidence",
        "mapping_template_count",
        "mapping_group_count",
        "mapping_candidate_template_nos",
        "mapping_candidate_group_ids",
    ):
        add(name, "source_mapping", "Table S2 exact/IUPAC-compatible windows", "Audit metadata from source mapping.", "uses target_ungapped only for lookup", "metadata_only", "Do not use as a default numeric feature; may encode source or pathogen group.")
    add("guide_target_hamming_dist_computed_v0_legacy", "legacy_qc", "v0 target_sequence", "Legacy value retained only for comparison.", "v0 removed gaps before comparison", "exclude")
    add("guide_target_hamming_dist_raw", "source_qc", "Table S3 source column", "Unmodified source value.", "source semantics unresolved", "exclude")
    add("label_raw_value", "label", "Table S3 30 min or Table S5 true value", "Measured activity label.", "not applicable", "label_only")
    return pd.DataFrame(rows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--run-dir", type=Path)
    args = parser.parse_args()
    root = args.root.resolve()

    v0 = pd.read_csv(root / V0_REL)
    alignment = pd.read_csv(root / ALIGNMENT_REL).set_index("record_id", drop=False)
    source_map = pd.read_csv(root / SOURCE_MAP_REL).set_index("record_id", drop=False)
    output_rows: list[dict[str, Any]] = []

    for _, source in v0.iterrows():
        row = source.to_dict()
        record_id = str(row["record_id"])
        guide = clean_sequence(row["crRNA_sequence"], keep_gap=True)
        is_table_s3 = record_id in alignment.index
        if is_table_s3:
            aligned = alignment.loc[record_id]
            target_aligned = str(aligned["target_aligned_25"])
            target_ungapped = str(aligned["target_ungapped"])
            alignment_qc = str(aligned["alignment_qc_status"])
            alignment_event_status = str(aligned["alignment_event_status"])
            guide_target_pair_id = str(aligned["guide_target_pair_id"])
            mapping = source_map.loc[record_id]
            mapping_fields = {
                key: mapping[key]
                for key in (
                    "mapping_status",
                    "mapping_confidence",
                    "mapping_hit_count",
                    "mapping_template_count",
                    "mapping_group_count",
                    "mapping_orientation_count",
                    "mapping_candidate_template_nos",
                    "mapping_candidate_group_ids",
                    "mapping_candidate_orientations",
                    "mapping_match_modes",
                )
            }
            eligibility = "eligible_core_v2" if alignment_qc == "pass_no_gap" else "conditional_gap_aware_v2"
        else:
            target_aligned = clean_sequence(row["target_sequence"], keep_gap=True)
            target_ungapped = target_aligned.replace("-", "")
            guide_target_pair_id = stable_pair_id(guide, target_aligned)
            alignment_qc = "pass_external_no_gap" if len(guide) == len(target_aligned) == 25 and "-" not in target_aligned else "review_external_alignment"
            alignment_event_status = "substitution_or_match_only" if "-" not in target_aligned else "gap_preserved"
            mapping_fields = {
                "mapping_status": "not_applicable_table_s5",
                "mapping_confidence": "not_applicable",
                "mapping_hit_count": 0,
                "mapping_template_count": 0,
                "mapping_group_count": 0,
                "mapping_orientation_count": 0,
                "mapping_candidate_template_nos": "",
                "mapping_candidate_group_ids": "",
                "mapping_candidate_orientations": "",
                "mapping_match_modes": "",
            }
            eligibility = "external_test_only_scale_unconfirmed"

        pair = pair_features(guide, target_aligned)
        guide_spacer = guide[4:]
        target_spacer_ungapped = target_aligned[4:].replace("-", "")
        legacy_hamming = safe_float(row.get("guide_target_hamming_dist_computed"))
        row.update(
            {
                "dataset_id": "EasyDesign_2024_diagnostic_activity_feature_v2",
                "feature_table_version": "v2_gap_aware",
                "guide_target_pair_id": guide_target_pair_id,
                "target_sequence": target_ungapped,
                "target_sequence_representation": "ungapped_legacy_compatibility",
                "target_aligned_25": target_aligned,
                "target_ungapped": target_ungapped,
                "target_alignment_length": len(target_aligned),
                "target_ungapped_length": len(target_ungapped),
                "alignment_has_gap": "yes" if "-" in guide or "-" in target_aligned else "no",
                "alignment_event_status": alignment_event_status,
                "alignment_qc_status": alignment_qc,
                "pam_sequence_guide": guide[:4],
                "pam_sequence_target_aligned": target_aligned[:4],
                "spacer_sequence_guide": guide_spacer,
                "spacer_sequence_target_aligned": target_aligned[4:],
                "spacer_sequence_target_ungapped_by_alignment": target_spacer_ungapped,
                "guide_target_hamming_dist_computed_v0_legacy": legacy_hamming,
                "guide_target_hamming_dist_computed": pair["aligned_difference_count"],
                "default_training_eligibility": eligibility,
                "default_model_input_profile": "gap_aware_pair_plus_sequence_composition_excluding_source_mapping",
                **pair,
                **base_features("guide", guide),
                **base_features("target_ungapped", target_ungapped),
                **base_features("guide_spacer", guide_spacer),
                **base_features("target_spacer_ungapped", target_spacer_ungapped),
                **mapping_fields,
            }
        )
        output_rows.append(row)

    output = pd.DataFrame(output_rows)
    output_path = root / OUTPUT_REL
    feature_dir = root / FEATURE_DIR_REL
    output_path.parent.mkdir(parents=True, exist_ok=True)
    feature_dir.mkdir(parents=True, exist_ok=True)
    output.to_csv(output_path, index=False)
    dictionary = feature_dictionary()
    dictionary.to_csv(feature_dir / "EasyDesign_2024_feature_dictionary_v2.csv", index=False)

    table_s3 = output[output["source_table_id"].astype(str).str.contains("TableS3")]
    table_s5 = output[output["source_table_id"].astype(str).str.contains("TableS5")]
    v0_labels = v0.set_index("record_id")["label_raw_value"].astype(float)
    v2_labels = output.set_index("record_id")["label_raw_value"].astype(float)
    v0_splits = v0.set_index("record_id")["baseline_split"].astype(str)
    v2_splits = output.set_index("record_id")["baseline_split"].astype(str)
    internal = table_s3[table_s3["baseline_split"].isin(["baseline_train", "baseline_validation"])]
    split_leakage_pairs = int((internal.groupby("guide_target_pair_id")["baseline_split"].nunique() > 1).sum())
    no_gap = table_s3[table_s3["alignment_has_gap"] == "no"]
    gap = table_s3[table_s3["alignment_has_gap"] == "yes"]
    qc = {
        "v0_rows": int(len(v0)),
        "v2_rows": int(len(output)),
        "record_id_unique": bool(output["record_id"].is_unique),
        "labels_unchanged": bool(v0_labels.equals(v2_labels)),
        "baseline_split_unchanged": bool(v0_splits.equals(v2_splits)),
        "table_s3_rows": int(len(table_s3)),
        "table_s5_rows": int(len(table_s5)),
        "table_s3_no_gap_rows": int(len(no_gap)),
        "table_s3_gap_rows": int(len(gap)),
        "eligible_core_v2_rows": int((output["default_training_eligibility"] == "eligible_core_v2").sum()),
        "conditional_gap_aware_v2_rows": int((output["default_training_eligibility"] == "conditional_gap_aware_v2").sum()),
        "external_test_rows": int((output["default_training_eligibility"] == "external_test_only_scale_unconfirmed").sum()),
        "no_gap_new_vs_legacy_hamming_agreement_rows": int(
            (no_gap["guide_target_hamming_dist_computed"] == no_gap["guide_target_hamming_dist_computed_v0_legacy"]).sum()
        ),
        "gap_new_vs_legacy_hamming_agreement_rows": int(
            (gap["guide_target_hamming_dist_computed"] == gap["guide_target_hamming_dist_computed_v0_legacy"]).sum()
        ),
        "pair_split_leakage_count": split_leakage_pairs,
        "feature_dictionary_rows": int(len(dictionary)),
        "output_columns": int(output.shape[1]),
        "mapping_confidence_counts_table_s3": table_s3["mapping_confidence"].value_counts().to_dict(),
    }
    qc_path = feature_dir / "EasyDesign_2024_feature_qc_v2.json"
    qc_path.write_text(json.dumps(qc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if args.run_dir:
        args.run_dir.mkdir(parents=True, exist_ok=True)
        (args.run_dir / "feature_table_qc.json").write_text(json.dumps(qc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(qc, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
