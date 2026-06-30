#!/usr/bin/env python3
"""Audit and organize DeepCas12a_2026 data.

This script is intentionally conservative:
- it never writes to 01_raw;
- it treats DeepCas12a as editing_activity, not diagnostic_activity;
- it preserves the binary AsCas12a editing activity label as a thresholded
  label derived from measured indel activity, not as fluorescence/RFU.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Iterable

import pandas as pd

try:
    import pdfplumber
except Exception:  # pragma: no cover - dependency availability is environment-specific.
    pdfplumber = None


SOURCE_ID = "DeepCas12a_2026"
PAPER_SHORT = "DeepCas12a"
YEAR = "2026"
FULL_TITLE = (
    "DeepCas12a: a hybrid deep learning framework for accurate AsCas12a "
    "efficiency prediction from sequence and epigenetic information"
)
COMMIT_TITLE = "Audit DeepCas12a 2026 editing activity data"
RUN_SLUG = "audit_deepcas12a_2026_editing_activity_data"


@dataclass(frozen=True)
class DatasetSpec:
    file_name: str
    role: str
    split: str
    preprocessing: str
    candidate_use: bool
    priority: str


DATASET_SPECS = [
    DatasetSpec("HT1-1_train.txt", "HT1-1 training split", "component_train", "standardized_ht", False, "high"),
    DatasetSpec("HT1-2_test.txt", "HT1-2 holdout test split", "holdout_test_HT1-2", "standardized_ht", True, "high"),
    DatasetSpec("HT2_test.txt", "independent HT2 test set", "independent_test_HT2", "standardized_ht", True, "high"),
    DatasetSpec("HT3_test.txt", "independent HT3 test set", "independent_test_HT3", "standardized_ht", True, "high"),
    DatasetSpec("HEKplasmid_in_situ.txt", "HEK plasmid in situ training component", "component_train", "retained_in_situ", False, "medium"),
    DatasetSpec("HEK_lenti_in_situ.txt", "HEK lenti in situ training component", "component_train", "retained_in_situ", False, "medium"),
    DatasetSpec(
        "train_HT1-1_plus_HEK_in_situ.txt",
        "recommended final training set",
        "baseline_train",
        "mixed_standardized_ht_and_retained_in_situ",
        True,
        "high",
    ),
]


CATALOG_COLUMNS = [
    "source_id",
    "paper_short",
    "year",
    "full_title",
    "path_type",
    "source_type",
    "raw_path",
    "file_names",
    "data_access_status",
    "record_unit",
    "label_type",
    "label_status",
    "sample_size_estimated",
    "sequence_fields_detected",
    "usable_for_training",
    "usable_for_extension",
    "priority",
    "main_risk",
    "notes",
]

SHEET_INDEX_COLUMNS = [
    "source_id",
    "file_name",
    "file_path",
    "sheet_name",
    "n_rows",
    "n_cols",
    "first_columns",
    "example_values",
    "guessed_content",
    "record_unit_guess",
    "has_crRNA_sequence",
    "has_target_sequence",
    "has_PAM",
    "has_label",
    "label_raw_candidates",
    "label_status_guess",
    "path_type_guess",
    "priority",
    "recommended_action",
    "extracted_csv_path",
    "notes",
]

LABEL_COLUMNS = [
    "label_raw_name",
    "normalized_label",
    "path_type",
    "biological_meaning_cn",
    "biological_meaning_en",
    "assay_readout",
    "label_status",
    "trainable_as_primary_label",
    "standard_unit",
    "transform_needed",
    "notes",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Audit DeepCas12a_2026 source data.")
    parser.add_argument("--project-root", default=".", help="Project root directory.")
    parser.add_argument(
        "--paper-pdf",
        default="/Users/linzibo/Downloads/s12864-026-13003-3_reference.pdf",
        help="DeepCas12a paper PDF used for evidence extraction.",
    )
    parser.add_argument("--run-id", default=None, help="Run directory timestamp, e.g. 20260630_153000.")
    return parser.parse_args()


def safe_slug(text: str) -> str:
    return re.sub(r"[^A-Za-z0-9]+", "_", text).strip("_")


def rel(path: Path, root: Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


def ensure_dirs(paths: Iterable[Path]) -> None:
    for path in paths:
        path.mkdir(parents=True, exist_ok=True)


def backup_file(path: Path, run_id: str, root: Path) -> str:
    if not path.exists():
        return ""
    if "99_notes" in path.parts:
        backup_dir = path.parent / "archived_backups"
    else:
        backup_dir = path.parent / "_archive" / "backups"
    backup_dir.mkdir(parents=True, exist_ok=True)
    backup_path = backup_dir / f"{path.stem}_{run_id}_backup{path.suffix}"
    shutil.copy2(path, backup_path)
    return rel(backup_path, root)


def read_text(path: Path, max_chars: int = 30000) -> str:
    if not path.exists():
        return ""
    text = path.read_text(encoding="utf-8", errors="replace")
    return text[:max_chars]


def file_inventory(raw_dir: Path, root: Path) -> pd.DataFrame:
    rows = []
    for path in sorted(raw_dir.rglob("*")):
        if not path.is_file():
            continue
        suffix = path.suffix.lower()
        if suffix == ".txt":
            ftype = "text table or text documentation"
        elif suffix == ".csv":
            ftype = "csv table"
        elif suffix == ".md":
            ftype = "markdown documentation"
        elif suffix == ".py":
            ftype = "python source"
        elif suffix == ".pth":
            ftype = "trained PyTorch checkpoint"
        elif suffix == ".png":
            ftype = "image"
        elif suffix == ".ds_store":
            ftype = "macOS metadata"
        else:
            ftype = suffix.lstrip(".") or "file"
        if "Dataset" in path.parts and suffix in {".txt", ".tsv", ".csv"}:
            usage = "DeepCas12a data table or manifest."
        elif "splits" in path.parts and suffix == ".csv":
            usage = "Split or cross-validation metadata."
        elif "trained_model" in path.parts:
            usage = "Pretrained model checkpoint; not a raw label source."
        elif suffix in {".md", ".txt"}:
            usage = "Source documentation."
        else:
            usage = "Repository artifact."
        rows.append(
            {
                "file_path": rel(path, root),
                "file_type": ftype,
                "file_size_bytes": path.stat().st_size,
                "possible_usage": usage,
            }
        )
    return pd.DataFrame(rows)


def load_dataset(path: Path) -> pd.DataFrame:
    df = pd.read_csv(
        path,
        sep=r"\s+",
        header=None,
        names=["sequence", "methylation_status", "dnase_signal_status", "label"],
        dtype=str,
        engine="python",
    )
    df["source_row"] = range(len(df))
    df["label"] = df["label"].astype(int)
    return df


def annotate_sequence_fields(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["target_context_sequence"] = out["sequence"]
    out["upstream_4bp"] = out["sequence"].str.slice(0, 4)
    out["pam_sequence"] = out["sequence"].str.slice(4, 8)
    out["protospacer_sequence"] = out["sequence"].str.slice(8, 31)
    out["downstream_3bp"] = out["sequence"].str.slice(31, 34)
    out["sequence_length"] = out["sequence"].str.len()
    out["protospacer_length"] = out["protospacer_sequence"].str.len()
    out["target_context_gc_content"] = out["sequence"].map(gc_fraction)
    out["protospacer_gc_content"] = out["protospacer_sequence"].map(gc_fraction)
    out["has_valid_dna_alphabet"] = out["sequence"].str.fullmatch(r"[ACGT]+").map(bool)
    out["pam_matches_TTTV"] = out["pam_sequence"].str.fullmatch(r"TTT[ACG]").map(bool)
    out["methylation_length"] = out["methylation_status"].str.len()
    out["dnase_length"] = out["dnase_signal_status"].str.len()
    out["methylation_valid_AN"] = out["methylation_status"].str.fullmatch(r"[AN]+").map(bool)
    out["dnase_valid_AN"] = out["dnase_signal_status"].str.fullmatch(r"[AN]+").map(bool)
    out["methylation_A_count"] = out["methylation_status"].str.count("A")
    out["dnase_A_count"] = out["dnase_signal_status"].str.count("A")
    return out


def gc_fraction(seq: str) -> float | None:
    if not isinstance(seq, str) or not seq:
        return None
    return round((seq.count("G") + seq.count("C")) / len(seq), 6)


def component_for_combined(source_file: str, source_row: int) -> tuple[str, str]:
    if source_file != "train_HT1-1_plus_HEK_in_situ.txt":
        if source_file.startswith("HT"):
            return source_file.replace(".txt", ""), "standardized_ht"
        return source_file.replace(".txt", ""), "retained_in_situ"
    if source_row < 15000:
        return "HT1-1_train", "standardized_ht"
    if source_row < 15055:
        return "HEKplasmid_in_situ", "retained_in_situ"
    return "HEK_lenti_in_situ", "retained_in_situ"


def extract_pdf_evidence(pdf_path: Path) -> list[dict]:
    targets = [
        ("title", "DeepCas12a: a hybrid deep learning framework"),
        ("data_preparation", "CRISPR-AsCas12a on-target cleavage efficiency data were retrieved"),
        ("binary_label", "For binary classification, labels were assigned"),
        ("input_sequence", "Target sequences (34 bp)"),
        ("input_tensor", "Input sequences were encoded as 6-channel tensors"),
        ("data_availability", "The datasets analyzed during the current study are available"),
    ]
    evidence = []
    if pdfplumber is None or not pdf_path.exists():
        return evidence
    with pdfplumber.open(pdf_path) as pdf:
        for page_no, page in enumerate(pdf.pages, start=1):
            compact = re.sub(r"\s+", " ", page.extract_text() or "")
            for key, needle in targets:
                if needle.lower() in compact.lower():
                    start = max(0, compact.lower().find(needle.lower()) - 180)
                    end = min(len(compact), compact.lower().find(needle.lower()) + 520)
                    evidence.append(
                        {
                            "evidence_id": key,
                            "source": str(pdf_path),
                            "page": page_no,
                            "snippet": compact[start:end],
                        }
                    )
    return evidence


def upsert_catalog(path: Path, row: dict, run_id: str, root: Path) -> str:
    backup = backup_file(path, run_id, root)
    if path.exists():
        df = pd.read_excel(path)
    else:
        df = pd.DataFrame(columns=CATALOG_COLUMNS)
    for col in CATALOG_COLUMNS:
        if col not in df.columns:
            df[col] = ""
    df = df[df["source_id"].astype(str) != SOURCE_ID]
    df = pd.concat([df[CATALOG_COLUMNS], pd.DataFrame([row])[CATALOG_COLUMNS]], ignore_index=True)
    df.to_excel(path, index=False)
    return backup


def upsert_sheet_index(path: Path, rows: list[dict], run_id: str, root: Path) -> str:
    backup = backup_file(path, run_id, root)
    if path.exists():
        df = pd.read_excel(path)
    else:
        df = pd.DataFrame(columns=SHEET_INDEX_COLUMNS)
    for col in SHEET_INDEX_COLUMNS:
        if col not in df.columns:
            df[col] = ""
    df = df[df["source_id"].astype(str) != SOURCE_ID]
    new_df = pd.DataFrame(rows)
    for col in SHEET_INDEX_COLUMNS:
        if col not in new_df.columns:
            new_df[col] = ""
    df = pd.concat([df[SHEET_INDEX_COLUMNS], new_df[SHEET_INDEX_COLUMNS]], ignore_index=True)
    df.to_excel(path, index=False)
    return backup


def upsert_label_dictionary(path: Path, rows: list[dict], run_id: str, root: Path) -> str:
    backup = backup_file(path, run_id, root)
    if path.exists():
        df = pd.read_excel(path)
    else:
        df = pd.DataFrame(columns=LABEL_COLUMNS)
    for col in LABEL_COLUMNS:
        if col not in df.columns:
            df[col] = ""
    mask = ~(
        (df["label_raw_name"].astype(str) == "label")
        & (df["normalized_label"].astype(str) == "editing_activity_binary")
        & (df["path_type"].astype(str) == "editing_activity")
    )
    df = df[mask]
    new_df = pd.DataFrame(rows)
    for col in LABEL_COLUMNS:
        if col not in new_df.columns:
            new_df[col] = ""
    df = pd.concat([df[LABEL_COLUMNS], new_df[LABEL_COLUMNS]], ignore_index=True)
    df.to_excel(path, index=False)
    return backup


def write_markdown(path: Path, content: str, run_id: str, root: Path, backups: list[str]) -> None:
    backup = backup_file(path, run_id, root)
    if backup:
        backups.append(backup)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.strip() + "\n", encoding="utf-8")


def append_or_replace_block(path: Path, marker: str, block: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    old = read_text(path, max_chars=200000) if path.exists() else ""
    start = f"<!-- BEGIN {marker} -->"
    end = f"<!-- END {marker} -->"
    new_block = f"{start}\n{block.strip()}\n{end}\n"
    pattern = re.compile(re.escape(start) + r".*?" + re.escape(end) + r"\n?", flags=re.S)
    if pattern.search(old):
        text = pattern.sub(new_block, old)
    else:
        text = (old.rstrip() + "\n\n" + new_block).lstrip()
    path.write_text(text, encoding="utf-8")


def update_candidate_readme(path: Path, path_en: Path) -> None:
    zh_block = """
### `editing_activity_deepcas12a/`

DeepCas12a 2026 的候选 editing activity 数据。该数据属于 AsCas12a on-target editing activity 二分类任务，不属于 diagnostic activity，不能与 EasyDesign fluorescence/RFU 标签合并。

主要文件：

- `DeepCas12a_2026_editing_activity_binary_v0.csv`：推荐的候选主表，包含 baseline_train、HT1-2 holdout test、HT2/HT3 independent test。
- `DeepCas12a_2026_editing_activity_feature_table_v0.csv`：基础序列和 epigenetic 特征表。
- `DeepCas12a_2026_9fold_partitions_v0.csv`：训练集 9-fold 交叉验证划分。
- `DeepCas12a_2026_data_usage_guide_zh.md` / `DeepCas12a_2026_data_usage_guide_en.md`：如何使用该数据。
"""
    en_block = """
### `editing_activity_deepcas12a/`

Candidate editing activity data from DeepCas12a 2026. This source is an AsCas12a on-target editing activity binary classification task. It is not diagnostic activity and must not be merged with EasyDesign fluorescence/RFU labels.

Key files:

- `DeepCas12a_2026_editing_activity_binary_v0.csv`: recommended candidate main table with baseline_train, HT1-2 holdout test, and HT2/HT3 independent tests.
- `DeepCas12a_2026_editing_activity_feature_table_v0.csv`: basic sequence and epigenetic feature table.
- `DeepCas12a_2026_9fold_partitions_v0.csv`: 9-fold cross-validation partitions for the training set.
- `DeepCas12a_2026_data_usage_guide_zh.md` / `DeepCas12a_2026_data_usage_guide_en.md`: usage guide for this dataset.
"""
    append_or_replace_block(path, "DeepCas12a_2026_EDITING_ACTIVITY", zh_block)
    append_or_replace_block(path_en, "DeepCas12a_2026_EDITING_ACTIVITY", en_block)


def build_docs(context: dict) -> dict[str, str]:
    inv_rows = "\n".join(
        f"| {r.file_path} | {r.file_type} | {r.file_size_bytes} | {r.possible_usage} |"
        for r in context["inventory"].itertuples(index=False)
    )
    table_rows = "\n".join(
        f"| {row['file_name']} | {row['n_rows']} | {row['label_counts']} | {row['recommended_action']} |"
        for row in context["table_summary_rows"]
    )
    pdf_rows_zh = "\n".join(
        f"| {e['page']} | {e['evidence_id']} | {e['snippet']} |" for e in context["pdf_evidence"]
    )
    pdf_rows_en = pdf_rows_zh
    quality = context["quality"]
    outputs = "\n".join(f"- `{p}`" for p in context["outputs"])
    unresolved_zh = "\n".join(f"- {q}" for q in context["unresolved_zh"])
    unresolved_en = "\n".join(f"- {q}" for q in context["unresolved_en"])

    data_audit_zh = f"""
# DeepCas12a_2026 数据审计

## 范围

本轮只处理 `01_raw/DeepCas12a_2026` 和论文 PDF `{context['paper_pdf']}`。`01_raw` 未被修改；没有训练模型；没有把 DeepCas12a 与 EasyDesign 或任何 diagnostic activity 数据合并。

## 确认事实

- DeepCas12a 属于 `editing_activity` 路径。
- 模型输入是 34 bp AsCas12a target-context sequence、34 位 methylation feature 和 34 位 DNase accessibility feature。
- 原始模型文件中的 `label` 是二分类 AsCas12a on-target activity 标签，`1` 表示 high activity，`0` 表示 low activity。
- 论文说明二分类标签来自 background-corrected indel frequency 阈值，不是 fluorescence/RFU。

## 文件清单

| file_path | file_type | file_size_bytes | possible_usage |
| --- | --- | ---: | --- |
{inv_rows}

## 表格判断

| file_name | n_rows | label_counts | recommended_action |
| --- | ---: | --- | --- |
{table_rows}

## PDF 证据

| page | evidence_id | snippet |
| ---: | --- | --- |
{pdf_rows_zh}

## 最值得清洗的表

- `Dataset/train_HT1-1_plus_HEK_in_situ.txt`：推荐训练集。
- `Dataset/HT1-2_test.txt`：HT1 holdout test。
- `Dataset/HT2_test.txt` 和 `Dataset/HT3_test.txt`：独立测试集。
- `splits/deepcas12a_9fold_partitions.csv`：训练集 9-fold validation 划分。

## 不确定问题

{unresolved_zh}
"""

    data_audit_en = f"""
# DeepCas12a_2026 Data Audit

## Scope

This round processed only `01_raw/DeepCas12a_2026` and the paper PDF `{context['paper_pdf']}`. `01_raw` was not modified; no model was trained; DeepCas12a was not merged with EasyDesign or any diagnostic activity data.

## Confirmed Facts

- DeepCas12a belongs to the `editing_activity` path.
- Model input consists of a 34 bp AsCas12a target-context sequence, a 34-character methylation feature, and a 34-character DNase accessibility feature.
- The model-ready `label` is a binary AsCas12a on-target activity label: `1` means high activity and `0` means low activity.
- The paper states that the binary label is derived from background-corrected indel-frequency thresholds, not fluorescence/RFU.

## File Inventory

| file_path | file_type | file_size_bytes | possible_usage |
| --- | --- | ---: | --- |
{inv_rows}

## Table Decisions

| file_name | n_rows | label_counts | recommended_action |
| --- | ---: | --- | --- |
{table_rows}

## PDF Evidence

| page | evidence_id | snippet |
| ---: | --- | --- |
{pdf_rows_en}

## Highest-Value Tables For Cleaning

- `Dataset/train_HT1-1_plus_HEK_in_situ.txt`: recommended training set.
- `Dataset/HT1-2_test.txt`: HT1 holdout test.
- `Dataset/HT2_test.txt` and `Dataset/HT3_test.txt`: independent test sets.
- `splits/deepcas12a_9fold_partitions.csv`: 9-fold validation partitions for the training set.

## Unresolved Questions

{unresolved_en}
"""

    run_report_zh = f"""
# 运行报告：{COMMIT_TITLE}

## 范围

数据源：`01_raw/DeepCas12a_2026`；论文 PDF：`{context['paper_pdf']}`。

## 输入

- DeepCas12a GitHub 仓库本地副本：`01_raw/DeepCas12a_2026`
- 论文 PDF：`{context['paper_pdf']}`
- 读取的关键说明文件：`README.md`、`Dataset/README.md`、`Dataset/Data_Descriptions.txt`、`splits/README.md`、`scripts/README.md`

## 输出

{outputs}

## 分类判断

- path_type：`editing_activity`
- record unit：34 bp AsCas12a target-context record
- label：`label`，二分类 high/low AsCas12a on-target activity
- label_status：`measured`，但属于由 measured indel frequency 阈值化得到的 binary label
- priority：high

## 数据质量检查

- candidate v0 行数：{quality['candidate_rows']}
- feature table 行数：{quality['feature_rows']}
- candidate label 分布：{quality['candidate_label_counts']}
- 序列长度异常行数：{quality['bad_sequence_length']}
- DNA alphabet 异常行数：{quality['bad_dna_alphabet']}
- methylation 长度异常行数：{quality['bad_methylation_length']}
- DNase 长度异常行数：{quality['bad_dnase_length']}
- PAM 不匹配 TTTV 行数：{quality['bad_pam_tttv']}
- candidate 重复 key 行数：{quality['candidate_duplicate_keys']}

## 下一步建议

- 若要训练 DeepCas12a 路线 baseline，只使用 `editing_activity_deepcas12a/` 子目录内的数据。
- 不要与 EasyDesign 的 `diagnostic_activity` fluorescence/RFU 标签合并。
- 若后续需要连续 editing efficiency 回归标签，需要追溯 Kim et al. 原始 indel frequency，而不是使用本仓库已阈值化的 `label`。
"""

    run_report_en = f"""
# Run Report: {COMMIT_TITLE}

## Scope

Data source: `01_raw/DeepCas12a_2026`; paper PDF: `{context['paper_pdf']}`.

## Inputs

- Local DeepCas12a GitHub copy: `01_raw/DeepCas12a_2026`
- Paper PDF: `{context['paper_pdf']}`
- Key documentation read: `README.md`, `Dataset/README.md`, `Dataset/Data_Descriptions.txt`, `splits/README.md`, `scripts/README.md`

## Outputs

{outputs}

## Classification Decisions

- path_type: `editing_activity`
- record unit: 34 bp AsCas12a target-context record
- label: `label`, binary high/low AsCas12a on-target activity
- label_status: `measured`, but represented as a binary label thresholded from measured indel frequency
- priority: high

## Data Quality Checks

- candidate v0 rows: {quality['candidate_rows']}
- feature table rows: {quality['feature_rows']}
- candidate label counts: {quality['candidate_label_counts']}
- bad sequence length rows: {quality['bad_sequence_length']}
- bad DNA alphabet rows: {quality['bad_dna_alphabet']}
- bad methylation length rows: {quality['bad_methylation_length']}
- bad DNase length rows: {quality['bad_dnase_length']}
- PAM rows not matching TTTV: {quality['bad_pam_tttv']}
- duplicate candidate key rows: {quality['candidate_duplicate_keys']}

## Next Recommended Actions

- For a DeepCas12a-route baseline, use only the data inside `editing_activity_deepcas12a/`.
- Do not merge this source with EasyDesign `diagnostic_activity` fluorescence/RFU labels.
- If a continuous editing-efficiency regression label is needed later, trace back to the original Kim et al. indel-frequency data rather than using this repository's thresholded `label`.
"""

    evidence_trace_zh = """
# DeepCas12a_2026 证据链

## Decision: DeepCas12a 属于 editing_activity

Evidence:
- 论文标题和摘要描述 AsCas12a efficiency prediction。
- 方法部分说明数据来自 AsCas12a on-target cleavage/editing efficiency。
- GitHub README 将任务描述为 AsCas12a on-target guide efficiency prediction。

Reasoning:
该数据描述的是 Cas12a 编辑/切割效率，不是 CRISPR diagnostics 荧光检测读数。

Remaining uncertainty:
无；path_type 使用 `editing_activity`。

## Decision: `label` 是二分类 editing activity label

Evidence:
- `Dataset/README.md` 说明 label 为 binary，`0` low activity，`1` high activity。
- `Data_Descriptions.txt` 说明 `1` 表示 high activity，`0` 表示 low activity。
- 论文方法部分说明二分类标签基于 background-corrected indel frequencies 的阈值。

Reasoning:
该列可以作为 primary binary classification label，但不能解释为连续 indel frequency，也不能解释为 fluorescence/RFU。

Remaining uncertainty:
原始连续 indel frequency 未包含在当前 model-ready 仓库中。

## Decision: 34 bp sequence 是 target-context sequence

Evidence:
- README 和 Dataset 说明均定义 sequence 为 4 bp upstream context + PAM + 23 bp protospacer + 3 bp downstream context。
- 论文方法部分说明 target sequences 为 34 bp。

Reasoning:
可以从 positions 5-8 推断 PAM，从 positions 9-31 推断 protospacer；但没有独立 crRNA sequence 列。

Remaining uncertainty:
如果后续需要 crRNA 序列，需明确方向和互补关系后再派生。
"""

    evidence_trace_en = """
# DeepCas12a_2026 Evidence Trace

## Decision: DeepCas12a belongs to editing_activity

Evidence:
- The paper title and abstract describe AsCas12a efficiency prediction.
- The methods describe AsCas12a on-target cleavage/editing efficiency data.
- The GitHub README describes the task as AsCas12a on-target guide efficiency prediction.

Reasoning:
The source describes Cas12a editing/cleavage efficiency, not CRISPR diagnostics fluorescence readouts.

Remaining uncertainty:
None; `path_type` is `editing_activity`.

## Decision: `label` is a binary editing activity label

Evidence:
- `Dataset/README.md` states that the label is binary, with `0` for low activity and `1` for high activity.
- `Data_Descriptions.txt` states that `1` indicates high activity and `0` indicates low activity.
- The paper methods state that binary labels were assigned using thresholds on background-corrected indel frequencies.

Reasoning:
This column can be used as a primary binary classification label, but it is not a continuous indel frequency and not fluorescence/RFU.

Remaining uncertainty:
The original continuous indel frequency values are not included in the current model-ready repository.

## Decision: The 34 bp sequence is a target-context sequence

Evidence:
- The README and Dataset documentation define the sequence as 4 bp upstream context + PAM + 23 bp protospacer + 3 bp downstream context.
- The paper methods describe 34 bp target sequences.

Reasoning:
PAM can be inferred from positions 5-8 and protospacer from positions 9-31. There is no independent crRNA sequence column.

Remaining uncertainty:
If crRNA sequences are needed later, strand orientation and complement rules must be confirmed before derivation.
"""

    method_notes_zh = """
# DeepCas12a_2026 方法记录

原始 GitHub 仓库文件保持不变。模型就绪 TXT 数据使用 pandas 以空白分隔格式读取，并添加显式列名 `sequence`、`methylation_status`、`dnase_signal_status` 和 `label`。论文 PDF、仓库 README、Dataset 说明和 split 说明被用于校对字段含义与标签来源。DeepCas12a 被归入 `editing_activity` 路径，`label` 被保留为由 measured indel activity 阈值化得到的二分类 AsCas12a on-target activity 标签。34 bp `sequence` 被拆分为 4 bp upstream context、PAM、23 bp protospacer 和 3 bp downstream context，并计算基础序列和 epigenetic 特征。没有训练模型，也没有把该数据与 diagnostic activity 数据合并。
"""

    method_notes_en = """
# DeepCas12a_2026 Method Notes

Raw GitHub repository files were left unchanged. Model-ready TXT data were read with pandas as whitespace-delimited files and assigned explicit column names: `sequence`, `methylation_status`, `dnase_signal_status`, and `label`. The paper PDF, repository README, Dataset documentation, and split documentation were used to verify field meanings and label provenance. DeepCas12a was classified as `editing_activity`, and `label` was retained as a binary AsCas12a on-target activity label thresholded from measured indel activity. The 34 bp `sequence` was split into 4 bp upstream context, PAM, 23 bp protospacer, and 3 bp downstream context, and basic sequence and epigenetic features were computed. No model was trained, and the data were not merged with diagnostic activity data.
"""

    problems_zh = f"""
# 待解决问题 DeepCas12a_2026

## 已确认

- DeepCas12a 属于 `editing_activity`，不是 `diagnostic_activity`。
- `label` 是二分类 AsCas12a on-target activity 标签，不能当作 fluorescence/RFU。
- 34 bp `sequence` 是 target-context sequence，包含 upstream context、PAM、protospacer 和 downstream context。
- HT 数据的 methylation/DNase 特征是仓库说明中的标准化模型输入，不应解释为真实整合位点的 epigenetic 状态。

## 仍需确认

{unresolved_zh}
"""

    problems_en = f"""
# Problems To Resolve DeepCas12a_2026

## Confirmed

- DeepCas12a belongs to `editing_activity`, not `diagnostic_activity`.
- `label` is a binary AsCas12a on-target activity label and must not be treated as fluorescence/RFU.
- The 34 bp `sequence` is a target-context sequence containing upstream context, PAM, protospacer, and downstream context.
- The HT methylation/DNase features are standardized model inputs according to the repository documentation and should not be interpreted as true epigenetic states at unknown integration loci.

## Still Needs Confirmation

{unresolved_en}
"""

    usage_zh = """
# DeepCas12a_2026 数据使用指南

## 推荐入口

第一次 DeepCas12a editing activity baseline 使用：

`DeepCas12a_2026_editing_activity_feature_table_v0.csv`

## 默认任务

- path_type：`editing_activity`
- 任务类型：二分类
- 标签列：`label_normalized`
- 正类：`1`，high AsCas12a on-target activity
- 负类：`0`，low AsCas12a on-target activity
- 输入主序列：`target_context_sequence`
- PAM：`pam_sequence`，由 34 bp sequence 的 positions 5-8 推断
- protospacer：`protospacer_sequence`，由 positions 9-31 推断

## 推荐划分

- 训练：`default_split == baseline_train`
- HT1 holdout 测试：`default_split == holdout_test_HT1-2`
- 独立测试：`default_split == independent_test_HT2` 和 `default_split == independent_test_HT3`
- 内部 9-fold validation：使用 `DeepCas12a_2026_9fold_partitions_v0.csv`

## 禁止事项

- 不要和 EasyDesign 的 fluorescence/RFU diagnostic activity 标签合并。
- 不要把 `label` 当作连续 indel frequency。
- 不要把 HT 标准化 epigenetic 特征解释为真实整合位点 methylation/DNase 状态。
"""

    usage_en = """
# DeepCas12a_2026 Data Usage Guide

## Recommended Entry Point

For the first DeepCas12a editing activity baseline, use:

`DeepCas12a_2026_editing_activity_feature_table_v0.csv`

## Default Task

- path_type: `editing_activity`
- task type: binary classification
- label column: `label_normalized`
- positive class: `1`, high AsCas12a on-target activity
- negative class: `0`, low AsCas12a on-target activity
- main input sequence: `target_context_sequence`
- PAM: `pam_sequence`, inferred from positions 5-8 of the 34 bp sequence
- protospacer: `protospacer_sequence`, inferred from positions 9-31

## Recommended Split

- Training: `default_split == baseline_train`
- HT1 holdout test: `default_split == holdout_test_HT1-2`
- Independent tests: `default_split == independent_test_HT2` and `default_split == independent_test_HT3`
- Internal 9-fold validation: use `DeepCas12a_2026_9fold_partitions_v0.csv`

## Do Not

- Do not merge with EasyDesign fluorescence/RFU diagnostic activity labels.
- Do not treat `label` as a continuous indel frequency.
- Do not interpret HT standardized epigenetic features as true methylation/DNase states at unknown integration loci.
"""

    split_plan_zh = """
# DeepCas12a_2026 划分计划

## 默认划分

- `baseline_train`：`Dataset/train_HT1-1_plus_HEK_in_situ.txt`，15,203 行。
- `holdout_test_HT1-2`：`Dataset/HT1-2_test.txt`，1,292 行。
- `independent_test_HT2`：`Dataset/HT2_test.txt`，2,963 行。
- `independent_test_HT3`：`Dataset/HT3_test.txt`，1,251 行。

## 9-fold validation

使用 `DeepCas12a_2026_9fold_partitions_v0.csv`。该文件来自 `splits/deepcas12a_9fold_partitions.csv`，用于 `train_HT1-1_plus_HEK_in_situ.txt` 的内部交叉验证。

## 注意

不要随机重新划分全部数据后再报告与论文可比的结果；HT1-2、HT2、HT3 应保留为测试集。
"""

    split_plan_en = """
# DeepCas12a_2026 Split Plan

## Default Split

- `baseline_train`: `Dataset/train_HT1-1_plus_HEK_in_situ.txt`, 15,203 rows.
- `holdout_test_HT1-2`: `Dataset/HT1-2_test.txt`, 1,292 rows.
- `independent_test_HT2`: `Dataset/HT2_test.txt`, 2,963 rows.
- `independent_test_HT3`: `Dataset/HT3_test.txt`, 1,251 rows.

## 9-fold validation

Use `DeepCas12a_2026_9fold_partitions_v0.csv`. It comes from `splits/deepcas12a_9fold_partitions.csv` and is intended for internal cross-validation on `train_HT1-1_plus_HEK_in_situ.txt`.

## Note

Do not randomly repartition all rows if the goal is to report results comparable to the paper. HT1-2, HT2, and HT3 should remain test sets.
"""

    dataset_report_zh = f"""
# DeepCas12a_2026 数据集构建报告

## 输入源表

- 推荐训练：`Dataset/train_HT1-1_plus_HEK_in_situ.txt`
- 测试：`Dataset/HT1-2_test.txt`、`Dataset/HT2_test.txt`、`Dataset/HT3_test.txt`
- 划分元数据：`splits/deepcas12a_9fold_partitions.csv`

## 输出数据

- `DeepCas12a_2026_editing_activity_binary_v0.csv`
- `DeepCas12a_2026_editing_activity_feature_table_v0.csv`
- `DeepCas12a_2026_9fold_partitions_v0.csv`
- `DeepCas12a_2026_ht1_train_test_split_v0.csv`

## 行数

- candidate v0：{quality['candidate_rows']}
- feature table：{quality['feature_rows']}

## 标签

标签列为 `label_normalized`，数值为 0/1。该标签代表 high/low AsCas12a on-target editing activity 的二分类，不是 fluorescence/RFU，也不是连续 indel frequency。
"""

    dataset_report_en = f"""
# DeepCas12a_2026 Dataset Build Report

## Input Source Tables

- Recommended training: `Dataset/train_HT1-1_plus_HEK_in_situ.txt`
- Tests: `Dataset/HT1-2_test.txt`, `Dataset/HT2_test.txt`, `Dataset/HT3_test.txt`
- Split metadata: `splits/deepcas12a_9fold_partitions.csv`

## Output Data

- `DeepCas12a_2026_editing_activity_binary_v0.csv`
- `DeepCas12a_2026_editing_activity_feature_table_v0.csv`
- `DeepCas12a_2026_9fold_partitions_v0.csv`
- `DeepCas12a_2026_ht1_train_test_split_v0.csv`

## Row Counts

- candidate v0: {quality['candidate_rows']}
- feature table: {quality['feature_rows']}

## Label

The label column is `label_normalized`, with values 0/1. It represents binary high/low AsCas12a on-target editing activity. It is not fluorescence/RFU and not continuous indel frequency.
"""

    candidate_readme_zh = """
# editing_activity_deepcas12a

本目录保存 DeepCas12a_2026 的候选 editing activity 数据。它和 EasyDesign diagnostic activity 分开存放，避免二分类 editing label 与 fluorescence/RFU label 混淆。

优先阅读：

- `DeepCas12a_2026_data_usage_guide_zh.md`
- `DeepCas12a_2026_split_plan_zh.md`
- `DeepCas12a_2026_dataset_build_report_zh.md`
"""

    candidate_readme_en = """
# editing_activity_deepcas12a

This directory stores candidate DeepCas12a_2026 editing activity data. It is separated from EasyDesign diagnostic activity to avoid mixing binary editing labels with fluorescence/RFU labels.

Read first:

- `DeepCas12a_2026_data_usage_guide_en.md`
- `DeepCas12a_2026_split_plan_en.md`
- `DeepCas12a_2026_dataset_build_report_en.md`
"""

    return {
        "data_audit_zh.md": data_audit_zh,
        "data_audit_en.md": data_audit_en,
        "run_report_zh.md": run_report_zh,
        "run_report_en.md": run_report_en,
        "evidence_trace_zh.md": evidence_trace_zh,
        "evidence_trace_en.md": evidence_trace_en,
        "method_notes_zh.md": method_notes_zh,
        "method_notes_en.md": method_notes_en,
        "problems_to_resolve_zh.md": problems_zh,
        "problems_to_resolve_en.md": problems_en,
        "usage_zh.md": usage_zh,
        "usage_en.md": usage_en,
        "split_plan_zh.md": split_plan_zh,
        "split_plan_en.md": split_plan_en,
        "dataset_report_zh.md": dataset_report_zh,
        "dataset_report_en.md": dataset_report_en,
        "candidate_readme_zh.md": candidate_readme_zh,
        "candidate_readme_en.md": candidate_readme_en,
    }


def main() -> None:
    args = parse_args()
    root = Path(args.project_root).resolve()
    raw_dir = root / "01_raw" / "DeepCas12a_2026"
    dataset_dir = raw_dir / "Dataset"
    splits_dir = raw_dir / "splits"
    paper_pdf = Path(args.paper_pdf)
    run_id = args.run_id or datetime.now().strftime("%Y%m%d_%H%M%S")
    run_dir = root / "99_notes" / "runs" / f"{run_id}_{RUN_SLUG}"
    candidate_dir = root / "04_candidate_ml_dataset" / "editing_activity_deepcas12a"
    extracted_dir = root / "02_extracted_tables" / "editing_activity"

    ensure_dirs(
        [
            root / "00_data_catalog" / "_archive" / "backups",
            root / "03_cleaned_minimal" / "_archive" / "backups",
            extracted_dir,
            candidate_dir,
            run_dir,
            root / "99_notes" / "current",
        ]
    )

    if not raw_dir.exists():
        raise FileNotFoundError(f"Raw directory not found: {raw_dir}")

    backups: list[str] = []
    outputs: list[str] = []
    inventory = file_inventory(raw_dir, root)
    pdf_evidence = extract_pdf_evidence(paper_pdf)

    raw_tables: dict[str, pd.DataFrame] = {}
    sheet_rows: list[dict] = []
    table_summary_rows: list[dict] = []

    spec_map = {spec.file_name: spec for spec in DATASET_SPECS}
    for spec in DATASET_SPECS:
        path = dataset_dir / spec.file_name
        df = load_dataset(path)
        df["source_file"] = spec.file_name
        df["dataset_role"] = spec.role
        df["default_split"] = spec.split
        df["preprocessing"] = spec.preprocessing
        df = annotate_sequence_fields(df)
        raw_tables[spec.file_name] = df
        out_name = f"DeepCas12a_2026_{safe_slug(path.stem)}_editing_activity_binary_raw.csv"
        out_path = extracted_dir / out_name
        backup = backup_file(out_path, run_id, root)
        if backup:
            backups.append(backup)
        df[
            [
                "source_file",
                "source_row",
                "sequence",
                "methylation_status",
                "dnase_signal_status",
                "label",
            ]
        ].to_csv(out_path, index=False)
        outputs.append(rel(out_path, root))
        label_counts = df["label"].value_counts().sort_index().to_dict()
        table_summary_rows.append(
            {
                "file_name": spec.file_name,
                "n_rows": len(df),
                "label_counts": json.dumps(label_counts, sort_keys=True),
                "recommended_action": "extract_to_csv",
            }
        )
        sheet_rows.append(
            {
                "source_id": SOURCE_ID,
                "file_name": spec.file_name,
                "file_path": rel(path, root),
                "sheet_name": "text_file_no_header",
                "n_rows": len(df),
                "n_cols": 4,
                "first_columns": "sequence; methylation_status; dnase_signal_status; label",
                "example_values": json.dumps(df.head(3)[["sequence", "methylation_status", "dnase_signal_status", "label"]].to_dict("records")),
                "guessed_content": "model-ready AsCas12a editing activity binary classification records",
                "record_unit_guess": "34 bp AsCas12a target-context record",
                "has_crRNA_sequence": "no",
                "has_target_sequence": "yes",
                "has_PAM": "yes",
                "has_label": "yes",
                "label_raw_candidates": "label",
                "label_status_guess": "measured",
                "path_type_guess": "editing_activity",
                "priority": spec.priority,
                "recommended_action": "extract_to_csv",
                "extracted_csv_path": rel(out_path, root),
                "notes": "Label is binary high/low AsCas12a on-target activity; target context includes PAM.",
            }
        )

    split_outputs = [
        ("ht1_train_test_split.csv", "HT1 train/test split metadata"),
        ("deepcas12a_9fold_partitions.csv", "DeepCas12a 9-fold validation partition metadata"),
    ]
    for file_name, content in split_outputs:
        src = splits_dir / file_name
        df = pd.read_csv(src)
        out_path = extracted_dir / f"DeepCas12a_2026_{safe_slug(src.stem)}_split_metadata_raw.csv"
        backup = backup_file(out_path, run_id, root)
        if backup:
            backups.append(backup)
        df.to_csv(out_path, index=False)
        outputs.append(rel(out_path, root))
        sheet_rows.append(
            {
                "source_id": SOURCE_ID,
                "file_name": file_name,
                "file_path": rel(src, root),
                "sheet_name": "csv_file",
                "n_rows": len(df),
                "n_cols": len(df.columns),
                "first_columns": "; ".join(df.columns[:20]),
                "example_values": json.dumps(df.head(3).to_dict("records")),
                "guessed_content": content,
                "record_unit_guess": "split metadata",
                "has_crRNA_sequence": "no",
                "has_target_sequence": "yes",
                "has_PAM": "yes",
                "has_label": "yes",
                "label_raw_candidates": "label",
                "label_status_guess": "measured",
                "path_type_guess": "editing_activity",
                "priority": "medium",
                "recommended_action": "keep_as_metadata",
                "extracted_csv_path": rel(out_path, root),
                "notes": "Split metadata; not an independent label table.",
            }
        )

    recommended_files = [spec.file_name for spec in DATASET_SPECS if spec.candidate_use]
    candidate_parts = []
    for file_name in recommended_files:
        df = raw_tables[file_name].copy()
        df["source_table_id"] = "DeepCas12a_2026_" + safe_slug(Path(file_name).stem)
        df["record_id_original"] = df["source_row"].map(lambda x: f"{file_name}:{x}")
        component_info = [component_for_combined(file_name, int(x)) for x in df["source_row"]]
        df["component_source"] = [x[0] for x in component_info]
        df["epigenetic_feature_interpretation"] = [x[1] for x in component_info]
        candidate_parts.append(df)
    candidate = pd.concat(candidate_parts, ignore_index=True)
    candidate["dataset_id"] = "DeepCas12a_2026_editing_activity_binary_v0"
    candidate["source_id"] = SOURCE_ID
    candidate["path_type"] = "editing_activity"
    candidate["cas_type"] = "AsCas12a"
    candidate["record_unit"] = "34bp_target_context"
    candidate["crRNA_sequence"] = ""
    candidate["label_raw_name"] = "label"
    candidate["label_raw_value"] = candidate["label"]
    candidate["label_normalized"] = candidate["label"]
    candidate["label_status"] = "measured"
    candidate["label_derivation"] = "binary_threshold_from_background_corrected_indel_frequency"
    candidate["is_measured"] = "yes"
    candidate["notes"] = "Binary high/low AsCas12a on-target editing activity; do not merge with fluorescence/RFU labels."
    candidate["record_id"] = candidate.index.map(lambda x: f"DeepCas12a_2026_record_{x:06d}")

    candidate_cols = [
        "dataset_id",
        "source_id",
        "source_table_id",
        "record_id",
        "record_id_original",
        "source_file",
        "source_row",
        "component_source",
        "default_split",
        "path_type",
        "cas_type",
        "record_unit",
        "target_context_sequence",
        "upstream_4bp",
        "pam_sequence",
        "protospacer_sequence",
        "downstream_3bp",
        "crRNA_sequence",
        "methylation_status",
        "dnase_signal_status",
        "epigenetic_feature_interpretation",
        "label_raw_name",
        "label_raw_value",
        "label_normalized",
        "label_status",
        "label_derivation",
        "is_measured",
        "notes",
    ]

    candidate_path = candidate_dir / "DeepCas12a_2026_editing_activity_binary_v0.csv"
    backup = backup_file(candidate_path, run_id, root)
    if backup:
        backups.append(backup)
    candidate[candidate_cols].to_csv(candidate_path, index=False)
    outputs.append(rel(candidate_path, root))

    feature_cols = candidate_cols + [
        "sequence_length",
        "protospacer_length",
        "target_context_gc_content",
        "protospacer_gc_content",
        "has_valid_dna_alphabet",
        "pam_matches_TTTV",
        "methylation_length",
        "dnase_length",
        "methylation_valid_AN",
        "dnase_valid_AN",
        "methylation_A_count",
        "dnase_A_count",
    ]
    feature_path = candidate_dir / "DeepCas12a_2026_editing_activity_feature_table_v0.csv"
    backup = backup_file(feature_path, run_id, root)
    if backup:
        backups.append(backup)
    candidate[feature_cols].to_csv(feature_path, index=False)
    outputs.append(rel(feature_path, root))

    minimal_path = root / "03_cleaned_minimal" / "editing_activity_minimal.csv"
    backup = backup_file(minimal_path, run_id, root)
    if backup:
        backups.append(backup)
    minimal_cols = [
        "source_id",
        "source_table_id",
        "record_id",
        "record_id_original",
        "cas_type",
        "target_context_sequence",
        "pam_sequence",
        "protospacer_sequence",
        "crRNA_sequence",
        "methylation_status",
        "dnase_signal_status",
        "label_raw_name",
        "label_raw_value",
        "label_normalized",
        "label_status",
        "is_measured",
        "default_split",
        "notes",
    ]
    candidate[minimal_cols].to_csv(minimal_path, index=False)
    outputs.append(rel(minimal_path, root))

    ninefold = pd.read_csv(splits_dir / "deepcas12a_9fold_partitions.csv")
    ninefold_path = candidate_dir / "DeepCas12a_2026_9fold_partitions_v0.csv"
    backup = backup_file(ninefold_path, run_id, root)
    if backup:
        backups.append(backup)
    ninefold.to_csv(ninefold_path, index=False)
    outputs.append(rel(ninefold_path, root))

    ht1_split = pd.read_csv(splits_dir / "ht1_train_test_split.csv")
    ht1_split_path = candidate_dir / "DeepCas12a_2026_ht1_train_test_split_v0.csv"
    backup = backup_file(ht1_split_path, run_id, root)
    if backup:
        backups.append(backup)
    ht1_split.to_csv(ht1_split_path, index=False)
    outputs.append(rel(ht1_split_path, root))

    quality = {
        "candidate_rows": int(len(candidate)),
        "feature_rows": int(len(candidate)),
        "candidate_label_counts": json.dumps(candidate["label_normalized"].value_counts().sort_index().to_dict(), sort_keys=True),
        "bad_sequence_length": int((candidate["sequence_length"] != 34).sum()),
        "bad_dna_alphabet": int((~candidate["has_valid_dna_alphabet"]).sum()),
        "bad_methylation_length": int((candidate["methylation_length"] != 34).sum()),
        "bad_dnase_length": int((candidate["dnase_length"] != 34).sum()),
        "bad_pam_tttv": int((~candidate["pam_matches_TTTV"]).sum()),
        "candidate_duplicate_keys": int(candidate.duplicated(["target_context_sequence", "methylation_status", "dnase_signal_status", "label_normalized"]).sum()),
    }

    paper_pdf_rel = rel(paper_pdf, root)
    paper_is_in_project = not paper_pdf_rel.startswith("/")
    raw_path_value = "01_raw/DeepCas12a_2026"
    if paper_is_in_project:
        raw_path_value += f"; {paper_pdf_rel}"
    data_access_status = "available_local_repo_and_local_paper_pdf" if paper_is_in_project else "available_local_repo; paper_pdf_external_path_recorded"

    master_row = {
        "source_id": SOURCE_ID,
        "paper_short": PAPER_SHORT,
        "year": YEAR,
        "full_title": FULL_TITLE,
        "path_type": "editing_activity",
        "source_type": "paper_pdf + github_repository_model_ready_data",
        "raw_path": raw_path_value,
        "file_names": "; ".join(
            [spec.file_name for spec in DATASET_SPECS]
            + ["dataset_summary.tsv", "ht1_train_test_split.csv", "deepcas12a_9fold_partitions.csv", paper_pdf.name]
        ),
        "data_access_status": data_access_status,
        "record_unit": "34 bp AsCas12a target-context record",
        "label_type": "binary AsCas12a editing activity",
        "label_status": "measured",
        "sample_size_estimated": f"{quality['candidate_rows']} candidate rows; train 15203; HT1-2 1292; HT2 2963; HT3 1251",
        "sequence_fields_detected": "sequence; target_context_sequence; PAM inferred positions 5-8; protospacer inferred positions 9-31",
        "usable_for_training": "yes",
        "usable_for_extension": "maybe",
        "priority": "high",
        "main_risk": "Binary label is thresholded from measured indel activity; continuous indel frequencies are not present in the model-ready repository.",
        "notes": "Do not merge with EasyDesign diagnostic_activity fluorescence/RFU labels.",
    }
    backups.append(upsert_catalog(root / "00_data_catalog" / "master_data_catalog.xlsx", master_row, run_id, root))
    backups.append(upsert_sheet_index(root / "00_data_catalog" / "source_sheet_index.xlsx", sheet_rows, run_id, root))
    label_rows = [
        {
            "label_raw_name": "label",
            "normalized_label": "editing_activity_binary",
            "path_type": "editing_activity",
            "biological_meaning_cn": "AsCas12a on-target 编辑活性高低的二分类标签。",
            "biological_meaning_en": "Binary high/low AsCas12a on-target editing activity label.",
            "assay_readout": "background-corrected indel frequency thresholded to high/low activity",
            "label_status": "measured",
            "trainable_as_primary_label": "yes",
            "standard_unit": "binary 0/1",
            "transform_needed": "no for binary classification; original continuous indel frequency unavailable",
            "notes": "0 = low activity; 1 = high activity. Not fluorescence/RFU and not diagnostic activity.",
        }
    ]
    backups.append(upsert_label_dictionary(root / "00_data_catalog" / "label_dictionary.xlsx", label_rows, run_id, root))
    backups = [x for x in backups if x]

    unresolved_zh = [
        "当前仓库只提供 model-ready binary labels；若后续需要连续 indel frequency，需要追溯 Kim et al. 原始数值。",
        "34 bp target-context sequence 可推断 PAM/protospacer，但没有独立 crRNA sequence；若要生成 crRNA 序列需要确认方向和互补规则。",
        "HEK in situ 数据的 A/N epigenetic feature calls 需要在后续模型解释中与 HT standardized features 分开讨论。",
    ]
    unresolved_en = [
        "The repository provides model-ready binary labels only; continuous indel frequencies require tracing back to the original Kim et al. values.",
        "PAM/protospacer can be inferred from the 34 bp target-context sequence, but there is no independent crRNA sequence; crRNA derivation requires strand and complement-rule confirmation.",
        "HEK in situ A/N epigenetic feature calls should be discussed separately from HT standardized features in downstream model interpretation.",
    ]

    context = {
        "paper_pdf": str(paper_pdf),
        "inventory": inventory,
        "pdf_evidence": pdf_evidence,
        "table_summary_rows": table_summary_rows,
        "quality": quality,
        "outputs": outputs,
        "unresolved_zh": unresolved_zh,
        "unresolved_en": unresolved_en,
    }
    docs = build_docs(context)

    write_markdown(run_dir / "README.md", f"# {COMMIT_TITLE}\n\n本目录保存 DeepCas12a_2026 editing activity 数据审计、提取和整理记录。", run_id, root, backups)
    write_markdown(run_dir / "README_en.md", f"# {COMMIT_TITLE}\n\nThis directory stores the DeepCas12a_2026 editing activity audit, extraction, and organization records.", run_id, root, backups)
    for name in [
        "data_audit_zh.md",
        "data_audit_en.md",
        "run_report_zh.md",
        "run_report_en.md",
        "evidence_trace_zh.md",
        "evidence_trace_en.md",
        "method_notes_zh.md",
        "method_notes_en.md",
        "problems_to_resolve_zh.md",
        "problems_to_resolve_en.md",
    ]:
        write_markdown(run_dir / name, docs[name], run_id, root, backups)
        outputs.append(rel(run_dir / name, root))

    write_markdown(candidate_dir / "README.md", docs["candidate_readme_zh.md"], run_id, root, backups)
    write_markdown(candidate_dir / "README_en.md", docs["candidate_readme_en.md"], run_id, root, backups)
    write_markdown(candidate_dir / "DeepCas12a_2026_data_usage_guide_zh.md", docs["usage_zh.md"], run_id, root, backups)
    write_markdown(candidate_dir / "DeepCas12a_2026_data_usage_guide_en.md", docs["usage_en.md"], run_id, root, backups)
    write_markdown(candidate_dir / "DeepCas12a_2026_split_plan_zh.md", docs["split_plan_zh.md"], run_id, root, backups)
    write_markdown(candidate_dir / "DeepCas12a_2026_split_plan_en.md", docs["split_plan_en.md"], run_id, root, backups)
    write_markdown(candidate_dir / "DeepCas12a_2026_dataset_build_report_zh.md", docs["dataset_report_zh.md"], run_id, root, backups)
    write_markdown(candidate_dir / "DeepCas12a_2026_dataset_build_report_en.md", docs["dataset_report_en.md"], run_id, root, backups)
    outputs.extend(
        [
            rel(candidate_dir / "README.md", root),
            rel(candidate_dir / "README_en.md", root),
            rel(candidate_dir / "DeepCas12a_2026_data_usage_guide_zh.md", root),
            rel(candidate_dir / "DeepCas12a_2026_data_usage_guide_en.md", root),
            rel(candidate_dir / "DeepCas12a_2026_split_plan_zh.md", root),
            rel(candidate_dir / "DeepCas12a_2026_split_plan_en.md", root),
            rel(candidate_dir / "DeepCas12a_2026_dataset_build_report_zh.md", root),
            rel(candidate_dir / "DeepCas12a_2026_dataset_build_report_en.md", root),
        ]
    )

    update_candidate_readme(root / "04_candidate_ml_dataset" / "README.md", root / "04_candidate_ml_dataset" / "README_en.md")

    append_or_replace_block(root / "99_notes" / "current" / "problems_to_resolve_zh.md", "DeepCas12a_2026", docs["problems_to_resolve_zh.md"])
    append_or_replace_block(root / "99_notes" / "current" / "problems_to_resolve_en.md", "DeepCas12a_2026", docs["problems_to_resolve_en.md"])
    outputs.extend(
        [
            rel(root / "99_notes" / "current" / "problems_to_resolve_zh.md", root),
            rel(root / "99_notes" / "current" / "problems_to_resolve_en.md", root),
            rel(root / "04_candidate_ml_dataset" / "README.md", root),
            rel(root / "04_candidate_ml_dataset" / "README_en.md", root),
        ]
    )

    manifest = {
        "source_id": SOURCE_ID,
        "run_id": run_id,
        "commit_title": COMMIT_TITLE,
        "outputs": sorted(set(outputs)),
        "backups": sorted(set(backups)),
        "quality": quality,
    }
    (run_dir / "output_manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print(json.dumps(manifest, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
