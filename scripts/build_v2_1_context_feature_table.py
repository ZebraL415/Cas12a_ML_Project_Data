#!/usr/bin/env python3
"""Build the versioned EasyDesign v2.1 sequence-context feature table.

The script never writes to or modifies the v2 source table. Positional mismatch
and gap features are preserved from v2; new features use only crRNA_sequence
and target_ungapped.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd


DINUCLEOTIDES = [a + b for a in "ACGT" for b in "ACGT"]
TRINUCLEOTIDES = ["AAA", "CCC", "GGG", "TTT", "GCG", "CGC", "TAT", "ATA"]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def write_json(path: Path, value: object) -> None:
    path.write_text(
        json.dumps(value, indent=2, ensure_ascii=False, allow_nan=False) + "\n",
        encoding="utf-8",
    )


def strict_dna(value: object, field: str, record_id: str) -> str:
    if pd.isna(value):
        raise ValueError(f"Missing {field} for record_id={record_id}")
    sequence = str(value).strip().upper().replace("U", "T")
    invalid = sorted(set(sequence) - set("ACGT"))
    if not sequence or invalid:
        raise ValueError(
            f"Invalid {field} for record_id={record_id}: length={len(sequence)}, invalid={invalid}"
        )
    return sequence


def fraction(sequence: str, bases: str) -> float:
    return sum(base in bases for base in sequence) / len(sequence)


def kmer_frequency(sequence: str, kmer: str) -> float:
    denominator = len(sequence) - len(kmer) + 1
    if denominator <= 0:
        return 0.0
    return sum(
        sequence[index : index + len(kmer)] == kmer for index in range(denominator)
    ) / denominator


def context_row(sequence: str, prefix: str) -> dict[str, float | int]:
    midpoint = max(1, len(sequence) // 2)
    row: dict[str, float | int] = {
        f"{prefix}_context_unique_base_count": len(set(sequence)),
        f"{prefix}_context_gc_first_half": fraction(sequence[:midpoint], "GC"),
        f"{prefix}_context_gc_second_half": fraction(sequence[midpoint:], "GC"),
        f"{prefix}_context_gc_first_5nt": fraction(sequence[:5], "GC"),
        f"{prefix}_context_gc_last_5nt": fraction(sequence[-5:], "GC"),
    }
    for kmer in DINUCLEOTIDES:
        row[f"{prefix}_context_dinuc_{kmer}_frequency"] = kmer_frequency(sequence, kmer)
    for kmer in TRINUCLEOTIDES:
        row[f"{prefix}_context_trinuc_{kmer}_frequency"] = kmer_frequency(sequence, kmer)
    return row


def dictionary_rows(prefix: str, input_field: str) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    gap_behavior = (
        "Guide must be strict A/C/G/T; no alignment or gap operation."
        if prefix == "guide"
        else "Computed from target_ungapped; alignment gaps are excluded from composition."
    )

    def add(name: str, definition: str) -> None:
        rows.append(
            {
                "feature_name": name,
                "category": "sequence_context",
                "input_fields": input_field,
                "formula_or_definition": definition,
                "gap_behavior": gap_behavior,
                "default_model_role": "candidate_input",
                "leakage_risk": "none_label_independent",
                "notes": (
                    "Promoted after training-only target-grouped CV; mismatch/gap positions "
                    "remain derived from target_aligned_25."
                ),
            }
        )

    add(f"{prefix}_context_unique_base_count", "Number of distinct A/C/G/T bases in the sequence.")
    add(f"{prefix}_context_gc_first_half", "GC fraction in sequence[0:floor(L/2)].")
    add(f"{prefix}_context_gc_second_half", "GC fraction in sequence[floor(L/2):L].")
    add(f"{prefix}_context_gc_first_5nt", "GC fraction in the first min(5,L) nucleotides.")
    add(f"{prefix}_context_gc_last_5nt", "GC fraction in the last min(5,L) nucleotides.")
    for kmer in DINUCLEOTIDES:
        add(
            f"{prefix}_context_dinuc_{kmer}_frequency",
            f"Overlapping count of {kmer} divided by L-2+1; 0 only when L<2.",
        )
    for kmer in TRINUCLEOTIDES:
        add(
            f"{prefix}_context_trinuc_{kmer}_frequency",
            f"Overlapping count of {kmer} divided by L-3+1; 0 only when L<3.",
        )
    return rows


def verify_context(features: pd.DataFrame, guides: list[str], targets: list[str]) -> dict[str, object]:
    checks: dict[str, bool] = {}
    checks["expected_58_context_features"] = features.shape[1] == 58
    checks["no_missing_context_values"] = not features.isna().any().any()
    values = features.to_numpy(dtype=float)
    checks["all_context_values_finite"] = bool(np.isfinite(values).all())
    frequency_columns = [
        column
        for column in features
        if "_frequency" in column or "_context_gc_" in column
    ]
    checks["frequency_and_gc_values_in_0_1"] = bool(
        ((features[frequency_columns] >= 0) & (features[frequency_columns] <= 1)).all().all()
    )
    unique_columns = [column for column in features if column.endswith("unique_base_count")]
    checks["unique_base_count_in_1_4"] = bool(
        ((features[unique_columns] >= 1) & (features[unique_columns] <= 4)).all().all()
    )
    dinuc_checks = []
    for prefix, sequences in (("guide", guides), ("target", targets)):
        columns = [f"{prefix}_context_dinuc_{kmer}_frequency" for kmer in DINUCLEOTIDES]
        sums = features[columns].sum(axis=1).to_numpy()
        expected = np.array([1.0 if len(sequence) >= 2 else 0.0 for sequence in sequences])
        dinuc_checks.append(np.allclose(sums, expected, atol=1e-12, rtol=0))
    checks["dinucleotide_frequencies_sum_to_one"] = bool(all(dinuc_checks))
    checks["target_ungapped_contains_no_gap"] = all("-" not in sequence for sequence in targets)
    return {"checks": checks, "all_passed": all(checks.values())}


def reports(output_dir: Path, summary: dict[str, object]) -> None:
    checks = summary["qc"]["checks"]
    check_lines_zh = "\n".join(f"- {'通过' if passed else '失败'}：`{name}`" for name, passed in checks.items())
    check_lines_en = "\n".join(f"- {'PASS' if passed else 'FAIL'}: `{name}`" for name, passed in checks.items())
    zh = f"""# EasyDesign v2.1 上下文特征表构建报告

## 范围

本层以只读 V2 gap-aware core 为父表，逐行从 `crRNA_sequence` 和 `target_ungapped` 重算 58 个序列上下文特征。未重算或覆盖 `target_aligned_25` 及其 mismatch/gap 位置特征，标签、split、来源字段与记录顺序均保持不变。

## 结果

- 父表：`{summary['source_table']}`
- 输出表：`{summary['output_table']}`
- 行数：{summary['n_rows']:,}
- 父表列数：{summary['n_parent_columns']}
- 新增上下文列数：{summary['n_context_features']}
- 输出总列数：{summary['n_output_columns']}
- 候选模型输入：{summary['n_candidate_inputs']} 个
- 输出 SHA-256：`{summary['output_sha256']}`

## 质量控制

{check_lines_zh}

## 使用边界

该表是 V2 的版本化候选扩展，不替代或覆盖 V2。`sequence_context` 已通过单 seed 的训练集内部 grouped CV，仍须在 V2-1 中完成多 seed 与整块消融后，才能决定其正式模型输入地位。
"""
    en = f"""# EasyDesign v2.1 Context Feature Table Build Report

## Scope

This layer treats the V2 gap-aware core table as read-only and recomputes 58 sequence-context features row by row from `crRNA_sequence` and `target_ungapped`. It neither recomputes nor overwrites `target_aligned_25` or its mismatch/gap positional features. Labels, splits, provenance fields, and row order are unchanged.

## Results

- Parent table: `{summary['source_table']}`
- Output table: `{summary['output_table']}`
- Rows: {summary['n_rows']:,}
- Parent columns: {summary['n_parent_columns']}
- Added context columns: {summary['n_context_features']}
- Total output columns: {summary['n_output_columns']}
- Candidate model inputs: {summary['n_candidate_inputs']}
- Output SHA-256: `{summary['output_sha256']}`

## Quality Control

{check_lines_en}

## Usage Boundary

This table is a versioned candidate extension of V2 and does not replace or overwrite it. `sequence_context` passed a single-seed training-only grouped CV, but its formal model-input status still depends on the V2-1 multi-seed block-ablation layer.
"""
    (output_dir / "v2_1_context_build_report_zh.md").write_text(zh, encoding="utf-8")
    (output_dir / "v2_1_context_build_report_en.md").write_text(en, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    config = json.loads(args.config.read_text(encoding="utf-8"))
    output_dir = args.output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=False)

    source_path = Path(config["source_table"])
    dictionary_path = Path(config["core_dictionary"])
    parent = pd.read_csv(source_path, low_memory=False)
    if parent.shape != tuple(config["expected_parent_shape"]):
        raise ValueError(f"Unexpected parent shape: {parent.shape}")
    if not parent["record_id"].is_unique:
        raise ValueError("record_id is not unique in the parent table")

    guides: list[str] = []
    targets: list[str] = []
    context_rows = []
    for record_id, guide_value, target_value in parent[
        ["record_id", "crRNA_sequence", "target_ungapped"]
    ].itertuples(index=False, name=None):
        guide = strict_dna(guide_value, "crRNA_sequence", str(record_id))
        target = strict_dna(target_value, "target_ungapped", str(record_id))
        guides.append(guide)
        targets.append(target)
        row = context_row(guide, "guide")
        row.update(context_row(target, "target"))
        context_rows.append(row)
    context = pd.DataFrame(context_rows, index=parent.index)

    duplicate_names = sorted(set(parent.columns).intersection(context.columns))
    if duplicate_names:
        raise ValueError(f"Context columns already exist in parent: {duplicate_names}")
    qc = verify_context(context, guides, targets)
    output = pd.concat([parent, context], axis=1)
    if output.columns.duplicated().any():
        raise ValueError("Duplicate columns in output table")
    pd.testing.assert_frame_equal(
        output.loc[:, parent.columns], parent, check_dtype=True, check_exact=True
    )

    core_dictionary = pd.read_csv(dictionary_path)
    context_dictionary = pd.DataFrame(
        dictionary_rows("guide", "crRNA_sequence")
        + dictionary_rows("target", "target_ungapped")
    )
    dictionary = pd.concat([core_dictionary, context_dictionary], ignore_index=True)
    if dictionary["feature_name"].duplicated().any():
        raise ValueError("Duplicate feature names in combined dictionary")
    candidate_features = dictionary.loc[
        dictionary["default_model_role"].eq("candidate_input"), "feature_name"
    ].tolist()
    missing_candidate_features = sorted(set(candidate_features) - set(output.columns))
    if missing_candidate_features:
        raise ValueError(f"Dictionary candidates missing from table: {missing_candidate_features}")

    table_name = config["output_table_name"]
    dictionary_name = config["output_dictionary_name"]
    output_path = output_dir / table_name
    dictionary_output = output_dir / dictionary_name
    context_output = output_dir / "EasyDesign_2024_sequence_context_feature_dictionary_v2_1.csv"
    output.to_csv(output_path, index=False)
    dictionary.to_csv(dictionary_output, index=False)
    context_dictionary.to_csv(context_output, index=False)

    reloaded = pd.read_csv(output_path, low_memory=False)
    pd.testing.assert_frame_equal(
        reloaded.loc[:, parent.columns], parent, check_dtype=False, check_exact=True
    )
    qc["checks"].update(
        {
            "record_id_unique": bool(reloaded["record_id"].is_unique),
            "record_id_and_order_unchanged": reloaded["record_id"].equals(parent["record_id"]),
            "parent_columns_value_exact_after_roundtrip": True,
            "no_duplicate_output_columns": not reloaded.columns.duplicated().any(),
            "expected_output_shape": reloaded.shape == tuple(config["expected_output_shape"]),
            "candidate_input_count_188": len(candidate_features) == 188,
            "label_unchanged": reloaded["label_normalized"].equals(parent["label_normalized"]),
            "split_unchanged": reloaded["baseline_split"].equals(parent["baseline_split"]),
            "source_table_id_unchanged": reloaded["source_table_id"].equals(parent["source_table_id"]),
        }
    )
    qc["all_passed"] = all(qc["checks"].values())
    if not qc["all_passed"]:
        raise ValueError(f"QC failed: {qc['checks']}")

    summary = {
        "build_id": config["build_id"],
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "source_table": str(source_path),
        "source_table_sha256": sha256(source_path),
        "source_dictionary": str(dictionary_path),
        "source_dictionary_sha256": sha256(dictionary_path),
        "output_table": str(output_path),
        "output_sha256": sha256(output_path),
        "output_dictionary": str(dictionary_output),
        "output_dictionary_sha256": sha256(dictionary_output),
        "n_rows": int(output.shape[0]),
        "n_parent_columns": int(parent.shape[1]),
        "n_context_features": int(context.shape[1]),
        "n_output_columns": int(output.shape[1]),
        "n_candidate_inputs": len(candidate_features),
        "feature_blocks": dictionary.loc[
            dictionary["default_model_role"].eq("candidate_input"), "category"
        ].value_counts().sort_index().to_dict(),
        "positional_alignment_source": "target_aligned_25 (preserved from V2; not recomputed)",
        "context_inputs": ["crRNA_sequence", "target_ungapped"],
        "qc": qc,
    }
    write_json(output_dir / "v2_1_context_build_manifest.json", summary)
    write_json(output_dir / "v2_1_context_build_qc.json", qc)
    reports(output_dir, summary)
    print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
