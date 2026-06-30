# Cas12a ML Project Data

本目录用于整理 CRISPR-Cas12a 相关论文和仓库数据，目标是为后续机器学习建模提供可追溯、可复核、可扩展的数据基础。

核心原则：

- 先审计，后清洗，再建模。
- `01_raw/` 中的原始文件只读，不重命名、不覆盖、不直接修改。
- 不合并不同 label system：editing activity、diagnostic activity、SNV annotation、specificity、prediction score、metadata 必须分开记录。
- 所有进入建模的数据必须能追溯到 source、workbook、sheet、原始列名和处理脚本。
- 各目录首页只保留当前有效数据和最新说明文件；数据层历史备份放入对应目录的 `_archive/backups/`，`99_notes/` 的历史记录按每次操作放入 `runs/`。

## 目录结构

### `00_data_catalog/`

项目导航中心，不存放原始数据。

- `master_data_catalog.xlsx`：数据源级索引。一行代表一个来源，例如一篇论文、一个 GitHub 仓库或一个补充数据包。
- `source_sheet_index.xlsx`：Excel sheet 级索引。记录每个 workbook/sheet 的行列数、示例值、初步分类、是否含序列/标签、是否建议导出。
- `label_dictionary.xlsx`：标签词典。说明原始标签列如何理解，例如 `30 min`、`true value`、prediction score 等。

第一次接触本库时，先从这里开始看。

历史备份位于 `00_data_catalog/_archive/backups/`。

### `01_raw/`

原始数据仓库。所有论文 PDF、supplementary xlsx、GitHub repo、README、source data 等都原封不动保存在这里。

重要规则：不要修改这里的任何文件。脚本只能读取，不能写回。

本目录下的 `README.md` 和 `README_en.md` 是项目层面的使用说明，不属于任何原始来源文件。

### `02_extracted_tables/`

从原始 workbook 或其他 raw 文件中拆出的中间表。这里的 CSV 仍然保留原始列名和原始含义，只要求能打开、能追溯来源。

常见子目录：

- `diagnostic_activity/`
- `editing_activity/`
- `snv_annotation/`
- `snv_specificity/`
- `predicted_library/`

各数据类型子目录如产生历史备份，应放入该子目录自己的 `_archive/backups/`。

### `03_cleaned_minimal/`

最小清洗层。这里开始出现统一字段，例如：

- `source_id`
- `source_table_id`
- `record_id`
- `crRNA_sequence`
- `target_sequence`
- `label_raw_name`
- `label_raw_value`
- `label_status`

这一层不是最终训练集，而是把高价值表整理成可比较、可追溯的标准形态。

历史备份位于 `03_cleaned_minimal/_archive/backups/`。

### `04_candidate_ml_dataset/`

候选建模数据层。只有 label 较清楚、record unit 相对一致、来源可追溯的数据才进入这里。

当前候选数据按来源和任务放入子目录：

- `diagnostic_activity_easydesign/`：EasyDesign_2024 diagnostic activity 候选数据。
- `editing_activity_deepcas12a/`：DeepCas12a_2026 editing activity 候选数据。
- `snv_specificity_extension/`：SNV specificity extension 预留路径。

各子目录自行保存当前 v0 文件、使用说明、split plan、build report 和 `_archive/backups/`。顶层只作为导航页。

### `99_notes/`

审计、问题和决策记录。

- `current/`：当前仍在使用的问题清单、会议决策和论文数据备注。
- `runs/`：每次数据整理、目录调整或 Git 上传的独立记录目录。
- `runs/*/data_audit_*.md`：数据审计报告。
- `runs/*/run_report_*.md`：每轮脚本或目录操作的运行报告。
- `runs/*/evidence_trace_*.md`：关键判断的证据来源。
- `runs/*/method_notes_*.md`：可用于论文 methods 的流程记录。

如果不确定某个字段含义，优先查这里，不要自己猜。

`99_notes/` 不再使用顶层 `_archive/backups/`。历史审计、运行报告、证据链、方法记录和 Git 操作记录按轮次存放在 `99_notes/runs/YYYYMMDD_HHMMSS_<operation-title-slug>/`；若某一轮内部有反复运行产生的旧副本，则放在该运行目录自己的 `archived_backups/`。

### `scripts/`

可复现脚本。所有重要整理步骤应尽量脚本化。

当前主要脚本：

- `inspect_easy_design.py`：第一轮 EasyDesign 数据侦察。
- `resolve_easy_design_round2.py`：结合原论文 PDF 和补充资料截图后的第二轮整理与 baseline v0 生成。

## 推荐使用顺序

1. 看 `00_data_catalog/master_data_catalog.xlsx`，了解有哪些数据源、属于哪条路径、是否可训练。
2. 看 `00_data_catalog/source_sheet_index.xlsx`，确认每个 workbook/sheet 的内容和推荐操作。
3. 看 `00_data_catalog/label_dictionary.xlsx`，确认标签列含义，避免把预测分数当实验标签。
4. 如需追溯原始表，去 `02_extracted_tables/`。
5. 如需看标准化后的最小表，去 `03_cleaned_minimal/`。
6. 如需运行 EasyDesign baseline，使用 `04_candidate_ml_dataset/diagnostic_activity_easydesign/EasyDesign_2024_diagnostic_activity_feature_table_v0.csv`，并先读同目录下的 `EasyDesign_2024_baseline_data_usage_guide_zh.md` 或 `EasyDesign_2024_baseline_data_usage_guide_en.md`。
7. 遇到不确定问题，查 `99_notes/current/problems_to_resolve_zh.md` 或 `99_notes/current/problems_to_resolve_en.md`；如需追溯历史依据，再查 `99_notes/runs/`。

## 当前 EasyDesign baseline 说明

当前最成熟的数据主线是 EasyDesign 2024 的 `diagnostic_activity`。

推荐第一次 baseline：

- 输入文件：`04_candidate_ml_dataset/diagnostic_activity_easydesign/EasyDesign_2024_diagnostic_activity_feature_table_v0.csv`
- 默认训练集：`baseline_split == baseline_train`
- 默认验证集：`baseline_split == baseline_validation`
- 默认标签列：`label_normalized`
- 默认只使用：`label_is_primary_baseline == yes`

暂不默认使用：

- `external_test_scale_unconfirmed`：Table S5 外部测试集，label 尺度尚未与 Table S3 完全确认。
- `04_candidate_ml_dataset/diagnostic_activity_easydesign/EasyDesign_2024_diagnostic_activity_augmented_optional_v0.csv`：增强数据，只有明确启用 augmentation 时才使用。
- `paper_prediction_*` 列：论文模型预测值，不是实验 label。

## 协作注意事项

- 新增数据源时，先更新 `00_data_catalog/`，再导出到 `02_extracted_tables/`。
- 不确定的字段或标签写入 `99_notes/current/problems_to_resolve_zh.md` 或 `99_notes/current/problems_to_resolve_en.md`。
- 不要直接把不同论文、不同 assay、不同 label status 的数据合并成训练集。
- 每次整理都应留下脚本和 run report，方便复现。
