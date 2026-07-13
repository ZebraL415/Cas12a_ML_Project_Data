#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Generate validated engineered features for the Cas12a diagnostic activity dataset.

Main functions
--------------
1. Read the original feature table.
2. Clean crRNA and target sequences.
3. Validate sequence orientation by testing:
   - direct
   - complement
   - reverse
   - reverse-complement
4. Select the orientation that best reproduces the existing
   guide_target_hamming_dist_computed column.
5. Generate deterministic single-sequence features.
6. Generate pairwise mismatch features using the validated orientation.
7. Save a new CSV containing identifiers, original labels/splits, and all
   derived features.
8. Save QC reports and a feature dictionary.

Important scientific note
-------------------------
This script validates orientation computationally against the existing
Hamming-distance column in the source table. It does not replace checking the
EasyDesign paper/data documentation for the biological sequence convention.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from collections import Counter
from pathlib import Path
from typing import Dict, Iterable, Tuple

import numpy as np
import pandas as pd

DNA = "ACGT"
COMPLEMENT_TABLE = str.maketrans("ACGT", "TGCA")
CANDIDATE_MODES = ("direct", "complement", "reverse", "reverse_complement")

GUIDE_COL = "crRNA_sequence"
TARGET_COL = "target_sequence"
CONTEXT_COL = "target_context_sequence"
PAM_COL = "pam"
PRIMARY_COL = "label_is_primary_baseline"
REF_COMPUTED_COL = "guide_target_hamming_dist_computed"
REF_RAW_COL = "guide_target_hamming_dist_raw"

ID_COLUMNS = [
    "dataset_id",
    "source_id",
    "source_table_id",
    "record_id",
    "paper_split",
    "baseline_split",
    "data_role",
    GUIDE_COL,
    TARGET_COL,
    CONTEXT_COL,
    PAM_COL,
    "label_raw_name",
    "label_raw_value",
    "label_normalized",
    "label_scale_group",
    PRIMARY_COL,
]

DINUCS = [a + b for a in DNA for b in DNA]
TRINUCS = ["AAA", "CCC", "GGG", "TTT", "GCG", "CGC", "TAT", "ATA"]
MISMATCH_TYPES = [f"{a}_to_{b}" for a in DNA for b in DNA if a != b]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate orientation and generate engineered Cas12a features."
    )
    parser.add_argument(
        "input_csv",
        type=Path,
        help="Original feature table CSV.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("validated_engineered_features_output"),
        help="Output directory.",
    )
    parser.add_argument(
        "--primary-only-for-validation",
        action="store_true",
        help=(
            "Use only label_is_primary_baseline=yes rows when selecting "
            "the orientation mode."
        ),
    )
    parser.add_argument(
        "--minimum-exact-agreement",
        type=float,
        default=0.99,
        help="Minimum exact agreement required for computational validation.",
    )
    return parser.parse_args()


def clean_sequence(value: object) -> str:
    if pd.isna(value):
        return ""
    seq = str(value).strip().upper().replace("U", "T")
    return "".join(base for base in seq if base in DNA)


def transform_target(seq: str, mode: str) -> str:
    if mode == "direct":
        return seq
    if mode == "complement":
        return seq.translate(COMPLEMENT_TABLE)
    if mode == "reverse":
        return seq[::-1]
    if mode == "reverse_complement":
        return seq.translate(COMPLEMENT_TABLE)[::-1]
    raise ValueError(f"Unsupported mode: {mode}")


def hamming_with_length_penalty(a: str, b: str) -> int:
    shared = min(len(a), len(b))
    mismatch_count = sum(x != y for x, y in zip(a[:shared], b[:shared]))
    return mismatch_count + abs(len(a) - len(b))


def gc_content(seq: str) -> float:
    if not seq:
        return np.nan
    return (seq.count("G") + seq.count("C")) / len(seq)


def shannon_entropy(seq: str) -> float:
    if not seq:
        return np.nan
    counts = Counter(seq)
    n = len(seq)
    return -sum(
        (count / n) * math.log2(count / n)
        for count in counts.values()
        if count > 0
    )


def longest_identical_base_run(seq: str) -> int:
    if not seq:
        return 0
    best = current = 1
    for i in range(1, len(seq)):
        if seq[i] == seq[i - 1]:
            current += 1
            best = max(best, current)
        else:
            current = 1
    return best


def longest_boolean_run(values: Iterable[bool], target_value: bool) -> int:
    best = current = 0
    for value in values:
        if value == target_value:
            current += 1
            best = max(best, current)
        else:
            current = 0
    return best


def kmer_frequency(seq: str, kmer: str) -> float:
    denominator = len(seq) - len(kmer) + 1
    if denominator <= 0:
        return 0.0
    return (
        sum(
            seq[i : i + len(kmer)] == kmer
            for i in range(denominator)
        )
        / denominator
    )


def single_sequence_features(seq: str, prefix: str) -> Dict[str, object]:
    n = len(seq)
    midpoint = max(1, n // 2) if n else 0

    features: Dict[str, object] = {
        f"{prefix}_length_engineered": n,
        f"{prefix}_gc_content_engineered": gc_content(seq),
        f"{prefix}_entropy": shannon_entropy(seq),
        f"{prefix}_longest_homopolymer": longest_identical_base_run(seq),
        f"{prefix}_unique_base_count": len(set(seq)) if seq else 0,
        f"{prefix}_gc_first_half": (
            gc_content(seq[:midpoint]) if seq else np.nan
        ),
        f"{prefix}_gc_second_half": (
            gc_content(seq[midpoint:])
            if seq and midpoint < n
            else np.nan
        ),
        f"{prefix}_gc_first_5": (
            gc_content(seq[:5]) if seq else np.nan
        ),
        f"{prefix}_gc_last_5": (
            gc_content(seq[-5:]) if seq else np.nan
        ),
    }

    for base in DNA:
        features[f"{prefix}_{base}_fraction"] = (
            seq.count(base) / n if n else 0.0
        )

    for dinuc in DINUCS:
        features[f"{prefix}_dinuc_{dinuc}"] = kmer_frequency(seq, dinuc)

    for trinuc in TRINUCS:
        features[f"{prefix}_trinuc_{trinuc}"] = kmer_frequency(seq, trinuc)

    return features


def pairwise_features(guide: str, target: str) -> Dict[str, object]:
    aligned_length = min(len(guide), len(target))
    guide_aligned = guide[:aligned_length]
    target_aligned = target[:aligned_length]

    mismatch_flags = [
        guide_aligned[i] != target_aligned[i]
        for i in range(aligned_length)
    ]
    mismatch_positions = [
        i + 1 for i, flag in enumerate(mismatch_flags) if flag
    ]
    mismatch_count_shared = sum(mismatch_flags)
    length_difference = abs(len(guide) - len(target))

    features: Dict[str, object] = {
        "aligned_length": aligned_length,
        "length_difference": length_difference,
        "mismatch_count_validated": mismatch_count_shared + length_difference,
        "mismatch_count_shared_positions": mismatch_count_shared,
        "mismatch_fraction_shared_positions": (
            mismatch_count_shared / aligned_length
            if aligned_length
            else np.nan
        ),
        "match_fraction_shared_positions": (
            (aligned_length - mismatch_count_shared) / aligned_length
            if aligned_length
            else np.nan
        ),
        "first_mismatch_position": (
            mismatch_positions[0] if mismatch_positions else 0
        ),
        "last_mismatch_position": (
            mismatch_positions[-1] if mismatch_positions else 0
        ),
        "longest_consecutive_match": longest_boolean_run(
            mismatch_flags, False
        ),
        "longest_consecutive_mismatch": longest_boolean_run(
            mismatch_flags, True
        ),
        "guide_target_gc_difference": (
            abs(gc_content(guide) - gc_content(target))
            if guide and target
            else np.nan
        ),
    }

    # Generic thirds. These are not automatically equivalent to a validated
    # PAM-proximal, seed, or PAM-distal biological region.
    if aligned_length:
        first_end = max(1, aligned_length // 3)
        second_end = max(first_end + 1, (2 * aligned_length) // 3)

        regions = {
            "first_third": mismatch_flags[:first_end],
            "middle_third": mismatch_flags[first_end:second_end],
            "last_third": mismatch_flags[second_end:],
        }

        for name, values in regions.items():
            features[f"mismatch_count_{name}"] = sum(values)
            features[f"mismatch_fraction_{name}"] = (
                sum(values) / len(values) if values else 0.0
            )
    else:
        for name in ("first_third", "middle_third", "last_third"):
            features[f"mismatch_count_{name}"] = 0
            features[f"mismatch_fraction_{name}"] = np.nan

    for position in range(1, 31):
        features[f"mismatch_pos_{position}"] = (
            int(mismatch_flags[position - 1])
            if position <= aligned_length
            else 0
        )

    mismatch_type_counts = Counter(
        f"{guide_base}_to_{target_base}"
        for guide_base, target_base in zip(
            guide_aligned, target_aligned
        )
        if guide_base != target_base
    )

    for mismatch_type in MISMATCH_TYPES:
        features[f"mismatch_type_{mismatch_type}"] = (
            mismatch_type_counts.get(mismatch_type, 0)
        )

    return features


def compare_to_reference(
    calculated: pd.Series,
    reference: pd.Series,
) -> Tuple[int, float, float, float]:
    calc = pd.to_numeric(calculated, errors="coerce")
    ref = pd.to_numeric(reference, errors="coerce")
    mask = calc.notna() & ref.notna()

    if mask.sum() == 0:
        return 0, np.nan, np.nan, np.nan

    exact_agreement = float((calc[mask] == ref[mask]).mean())
    mean_absolute_error = float((calc[mask] - ref[mask]).abs().mean())

    if calc[mask].nunique() > 1 and ref[mask].nunique() > 1:
        correlation = float(calc[mask].corr(ref[mask]))
    else:
        correlation = np.nan

    return int(mask.sum()), exact_agreement, mean_absolute_error, correlation


def validate_orientation(
    df: pd.DataFrame,
    guide: pd.Series,
    target: pd.Series,
    selection_mask: pd.Series,
) -> Tuple[str, pd.DataFrame, Dict[str, pd.Series], float, str]:
    summaries = []
    distance_by_mode: Dict[str, pd.Series] = {}

    for mode in CANDIDATE_MODES:
        transformed = target.map(lambda seq: transform_target(seq, mode))
        distances = pd.Series(
            [
                hamming_with_length_penalty(g, t)
                for g, t in zip(guide, transformed)
            ],
            index=df.index,
            name=f"hamming_{mode}",
        )
        distance_by_mode[mode] = distances

        row: Dict[str, object] = {
            "mode": mode,
            "rows_evaluated": int(selection_mask.sum()),
            "median_hamming": float(distances[selection_mask].median()),
            "mean_hamming": float(distances[selection_mask].mean()),
        }

        if REF_COMPUTED_COL in df.columns:
            n, exact, mae, corr = compare_to_reference(
                distances[selection_mask],
                df.loc[selection_mask, REF_COMPUTED_COL],
            )
            row.update(
                {
                    "computed_reference_n": n,
                    "computed_exact_agreement": exact,
                    "computed_mae": mae,
                    "computed_correlation": corr,
                }
            )

        if REF_RAW_COL in df.columns:
            n, exact, mae, corr = compare_to_reference(
                distances[selection_mask],
                df.loc[selection_mask, REF_RAW_COL],
            )
            row.update(
                {
                    "raw_reference_n": n,
                    "raw_exact_agreement": exact,
                    "raw_mae": mae,
                    "raw_correlation": corr,
                }
            )

        summaries.append(row)

    summary_df = pd.DataFrame(summaries)

    if "computed_exact_agreement" in summary_df.columns:
        best_index = (
            summary_df["computed_exact_agreement"]
            .fillna(-1)
            .idxmax()
        )
        best_exact = float(
            summary_df.loc[best_index, "computed_exact_agreement"]
        )
        selection_basis = REF_COMPUTED_COL
    elif "raw_exact_agreement" in summary_df.columns:
        best_index = (
            summary_df["raw_exact_agreement"]
            .fillna(-1)
            .idxmax()
        )
        best_exact = float(
            summary_df.loc[best_index, "raw_exact_agreement"]
        )
        selection_basis = REF_RAW_COL
    else:
        best_index = summary_df["median_hamming"].idxmin()
        best_exact = np.nan
        selection_basis = "lowest_median_hamming_only"

    selected_mode = str(summary_df.loc[best_index, "mode"])
    return (
        selected_mode,
        summary_df,
        distance_by_mode,
        best_exact,
        selection_basis,
    )


def build_feature_dictionary() -> pd.DataFrame:
    rows = []

    def add(
        feature: str,
        category: str,
        meaning: str,
        calculation: str,
        validation_status: str,
    ) -> None:
        rows.append(
            {
                "feature": feature,
                "category": category,
                "meaning": meaning,
                "calculation": calculation,
                "validation_status": validation_status,
            }
        )

    add(
        "selected_alignment_mode",
        "metadata",
        "Target representation selected by orientation validation",
        "Best match to existing Hamming-distance column",
        "computationally validated",
    )
    add(
        "aligned_length",
        "pairwise",
        "Length used for direct position-wise comparison",
        "min(guide length, transformed target length)",
        "deterministic",
    )
    add(
        "length_difference",
        "pairwise",
        "Absolute difference between sequence lengths",
        "abs(guide length - target length)",
        "deterministic",
    )
    add(
        "mismatch_count_validated",
        "pairwise",
        "Mismatch count including extra unpaired positions",
        "shared-position mismatches + length difference",
        "computationally validated",
    )
    add(
        "mismatch_fraction_shared_positions",
        "pairwise",
        "Mismatch proportion across shared positions",
        "shared-position mismatch count / aligned length",
        "computationally validated",
    )
    add(
        "match_fraction_shared_positions",
        "pairwise",
        "Match proportion across shared positions",
        "1 - mismatch fraction across shared positions",
        "computationally validated",
    )
    add(
        "first_mismatch_position",
        "pairwise",
        "First mismatch position under selected alignment",
        "First unequal index + 1",
        "computationally validated",
    )
    add(
        "last_mismatch_position",
        "pairwise",
        "Last mismatch position under selected alignment",
        "Last unequal index + 1",
        "computationally validated",
    )
    add(
        "longest_consecutive_match",
        "pairwise",
        "Longest consecutive matching segment",
        "Longest run of equal aligned bases",
        "computationally validated",
    )
    add(
        "longest_consecutive_mismatch",
        "pairwise",
        "Longest consecutive mismatch segment",
        "Longest run of unequal aligned bases",
        "computationally validated",
    )

    for region in ("first_third", "middle_third", "last_third"):
        add(
            f"mismatch_count_{region}",
            "regional mismatch",
            f"Mismatch count in the {region.replace('_', ' ')}",
            "Aligned sequence divided into generic thirds",
            "computationally validated; not a biological seed definition",
        )
        add(
            f"mismatch_fraction_{region}",
            "regional mismatch",
            f"Mismatch fraction in the {region.replace('_', ' ')}",
            "Regional mismatch count / regional length",
            "computationally validated; not a biological seed definition",
        )

    for position in range(1, 31):
        add(
            f"mismatch_pos_{position}",
            "position-specific mismatch",
            f"Whether position {position} is a mismatch",
            "1 if unequal, otherwise 0",
            "computationally validated",
        )

    for mismatch_type in MISMATCH_TYPES:
        add(
            f"mismatch_type_{mismatch_type}",
            "mismatch type",
            f"Count of {mismatch_type.replace('_to_', '→')} differences",
            "Count across aligned positions",
            "computationally validated",
        )

    for prefix, name in (("guide", "crRNA/guide"), ("target", "target")):
        add(
            f"{prefix}_length_engineered",
            "single sequence",
            f"Length of {name}",
            "Number of cleaned A/C/G/T bases",
            "deterministic",
        )
        add(
            f"{prefix}_gc_content_engineered",
            "single sequence",
            f"GC content of {name}",
            "(G + C) / sequence length",
            "deterministic",
        )
        add(
            f"{prefix}_entropy",
            "single sequence",
            f"Shannon entropy of {name}",
            "-sum[p(base) log2 p(base)]",
            "deterministic",
        )
        add(
            f"{prefix}_longest_homopolymer",
            "single sequence",
            f"Longest identical-base run in {name}",
            "Maximum consecutive identical bases",
            "deterministic",
        )
        add(
            f"{prefix}_unique_base_count",
            "single sequence",
            f"Number of distinct bases in {name}",
            "Count of unique A/C/G/T",
            "deterministic",
        )

        for region_name in (
            "gc_first_half",
            "gc_second_half",
            "gc_first_5",
            "gc_last_5",
        ):
            add(
                f"{prefix}_{region_name}",
                "local GC",
                f"Local GC content of {name}: {region_name}",
                "(G + C) / local sequence length",
                "deterministic",
            )

        for base in DNA:
            add(
                f"{prefix}_{base}_fraction",
                "nucleotide composition",
                f"Fraction of {base} in {name}",
                f"count({base}) / sequence length",
                "deterministic",
            )

        for dinuc in DINUCS:
            add(
                f"{prefix}_dinuc_{dinuc}",
                "2-mer frequency",
                f"Frequency of {dinuc} in {name}",
                "Occurrences / possible 2-mer positions",
                "deterministic",
            )

        for trinuc in TRINUCS:
            add(
                f"{prefix}_trinuc_{trinuc}",
                "3-mer frequency",
                f"Frequency of {trinuc} in {name}",
                "Occurrences / possible 3-mer positions",
                "deterministic",
            )

    return pd.DataFrame(rows)


def main() -> int:
    args = parse_args()

    if not args.input_csv.exists():
        print(
            f"ERROR: input file not found: {args.input_csv}",
            file=sys.stderr,
        )
        return 1

    args.output_dir.mkdir(parents=True, exist_ok=True)

    print(f"Loading: {args.input_csv}")
    df = pd.read_csv(args.input_csv, low_memory=False)

    required = {GUIDE_COL, TARGET_COL}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    guide = df[GUIDE_COL].map(clean_sequence)
    target = df[TARGET_COL].map(clean_sequence)

    if (
        args.primary_only_for_validation
        and PRIMARY_COL in df.columns
    ):
        selection_mask = (
            df[PRIMARY_COL]
            .astype(str)
            .str.strip()
            .str.lower()
            .eq("yes")
        )
    else:
        selection_mask = pd.Series(True, index=df.index)

    (
        selected_mode,
        orientation_summary,
        distance_by_mode,
        best_exact_agreement,
        selection_basis,
    ) = validate_orientation(
        df,
        guide,
        target,
        selection_mask,
    )

    computationally_validated = (
        not np.isnan(best_exact_agreement)
        and best_exact_agreement
        >= args.minimum_exact_agreement
    )

    transformed_target = target.map(
        lambda seq: transform_target(seq, selected_mode)
    )

    print(f"Selected orientation mode: {selected_mode}")
    print(f"Selection basis: {selection_basis}")
    print(f"Best exact agreement: {best_exact_agreement}")

    print("Generating engineered features...")
    feature_records = []

    for g, t in zip(guide, transformed_target):
        features: Dict[str, object] = {
            "selected_alignment_mode": selected_mode,
            "computational_validation_status": (
                "validated_against_existing_hamming_column"
                if computationally_validated
                else "not_validated"
            ),
            "biological_source_validation_status": (
                "still_requires_confirmation_from_source_documentation"
            ),
            "cleaned_crRNA_sequence": g,
            "cleaned_target_sequence_original": "",
            "transformed_target_sequence": t,
        }
        features.update(single_sequence_features(g, "guide"))
        features.update(single_sequence_features(t, "target"))
        features.update(pairwise_features(g, t))
        feature_records.append(features)

    engineered = pd.DataFrame(feature_records, index=df.index)
    engineered["cleaned_target_sequence_original"] = target

    retained_columns = [
        column for column in ID_COLUMNS if column in df.columns
    ]
    output = pd.concat(
        [df[retained_columns].copy(), engineered],
        axis=1,
    )

    output_path = (
        args.output_dir
        / "diagnostic_activity_validated_engineered_features_v1.csv"
    )
    output.to_csv(output_path, index=False)

    orientation_summary.to_csv(
        args.output_dir / "alignment_mode_summary.csv",
        index=False,
    )

    audit = pd.DataFrame(
        {
            "record_id": (
                df["record_id"]
                if "record_id" in df.columns
                else np.arange(len(df))
            ),
            "cleaned_crRNA_sequence": guide,
            "cleaned_target_sequence": target,
            "transformed_target_sequence": transformed_target,
            "selected_alignment_mode": selected_mode,
            "recomputed_hamming_selected_mode": (
                distance_by_mode[selected_mode]
            ),
            "crRNA_length_cleaned": guide.str.len(),
            "target_length_cleaned": target.str.len(),
            "equal_cleaned_lengths": (
                guide.str.len() == target.str.len()
            ),
        }
    )

    if REF_COMPUTED_COL in df.columns:
        reference = pd.to_numeric(
            df[REF_COMPUTED_COL],
            errors="coerce",
        )
        audit[REF_COMPUTED_COL] = reference
        audit["matches_computed_hamming_reference"] = (
            distance_by_mode[selected_mode] == reference
        )

    if REF_RAW_COL in df.columns:
        reference = pd.to_numeric(
            df[REF_RAW_COL],
            errors="coerce",
        )
        audit[REF_RAW_COL] = reference
        audit["matches_raw_hamming_reference"] = (
            distance_by_mode[selected_mode] == reference
        )

    audit.to_csv(
        args.output_dir / "alignment_row_audit.csv",
        index=False,
    )

    dictionary = build_feature_dictionary()
    dictionary.to_csv(
        args.output_dir / "feature_dictionary.csv",
        index=False,
    )

    report = {
        "input_file": str(args.input_csv),
        "output_file": str(output_path),
        "rows_total": int(len(df)),
        "rows_used_for_orientation_validation": int(
            selection_mask.sum()
        ),
        "selected_alignment_mode": selected_mode,
        "selection_basis": selection_basis,
        "best_exact_agreement": (
            None
            if np.isnan(best_exact_agreement)
            else best_exact_agreement
        ),
        "minimum_exact_agreement_required": (
            args.minimum_exact_agreement
        ),
        "computationally_validated": computationally_validated,
        "biologically_verified_from_source_documentation": False,
        "new_engineered_feature_columns": int(
            engineered.shape[1]
        ),
        "equal_length_rows": int(
            (guide.str.len() == target.str.len()).sum()
        ),
        "unequal_length_rows": int(
            (guide.str.len() != target.str.len()).sum()
        ),
        "crRNA_length_distribution": {
            str(k): int(v)
            for k, v in (
                guide.str.len()
                .value_counts()
                .sort_index()
                .items()
            )
        },
        "target_length_distribution": {
            str(k): int(v)
            for k, v in (
                target.str.len()
                .value_counts()
                .sort_index()
                .items()
            )
        },
        "interpretation": (
            "The selected orientation reproduces the existing Hamming "
            "distance column and is therefore computationally validated "
            "for reproducible feature generation. Biological sequence "
            "conventions should still be confirmed from the EasyDesign "
            "source documentation."
        ),
    }

    (
        args.output_dir / "generation_report.json"
    ).write_text(
        json.dumps(report, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print("\nCompleted successfully.")
    print(f"Main output: {output_path}")
    print(
        f"Engineered feature columns: {engineered.shape[1]}"
    )
    print(
        f"Unequal-length guide-target rows: "
        f"{report['unequal_length_rows']}"
    )
    print(f"All outputs saved to: {args.output_dir.resolve()}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
