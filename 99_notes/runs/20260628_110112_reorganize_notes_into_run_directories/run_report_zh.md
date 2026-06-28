# 运行报告：Reorganize Notes Into Run Directories

## 范围

本次处理范围仅为 `99_notes/`。未修改 `01_raw/`、`02_extracted_tables/`、`03_cleaned_minimal/` 或 `04_candidate_ml_dataset/` 中的数据文件。

## 目录规则

新增规则为：每一次数据整理、目录调整或 Git 上传都应在 `99_notes/runs/` 下建立独立目录，命名格式为 `YYYYMMDD_HHMMSS_<operation-title-slug>/`。如果本次操作会提交到 Git，`operation-title-slug` 应与 commit 标题对应。

## 已完成整理

- 建立 `current/` 用于保存当前活动问题、会议决策和论文数据备注。
- 建立 `runs/20260627_203620_audit_easy_design_2024_round1/` 保存第一轮 EasyDesign 审计记录。
- 建立 `runs/20260628_004335_resolve_easy_design_2024_round2_baseline_dataset/` 保存第二轮 EasyDesign PDF 校对和 baseline 数据整理记录。
- 建立 `runs/20260628_010938_initial_data_project_snapshot/` 追溯记录首次 Git 上传。
- 建立 `runs/20260628_105240_organize_backups_and_add_directory_guides/` 追溯记录上一次目录整理提交。
- 建立 `runs/20260628_110112_reorganize_notes_into_run_directories/` 保存本次整理记录。

## 文件命名

同一运行目录内使用统一文件名，例如 `data_audit_zh.md`、`data_audit_en.md`、`run_report_zh.md`、`run_report_en.md`、`evidence_trace_zh.md`、`method_notes_en.md`、`problems_to_resolve_zh.md`。

## 额外纳入的用户变更

用户确认 `04_candidate_ml_dataset/split_plan.md` 的删除由用户发起，本次一并纳入提交。该删除不属于 `99_notes` 重组本身，但随本次 Git 提交记录。
