# Cas12a ML Project Data

本目录用于整理 CRISPR-Cas12a 相关论文和仓库数据，目标是为后续机器学习建模提供可追溯、可复核、可扩展的数据基础。

核心原则：

- 先审计，后清洗，再建模。
- `01_raw/` 中的原始文件只读，不重命名、不覆盖、不直接修改。
- 不合并不同 label system：editing activity、diagnostic activity、SNV annotation、specificity、prediction score、metadata 必须分开记录。
- 所有进入建模的数据必须能追溯到 source、workbook、sheet、原始列名和处理脚本。
- 各目录首页只保留当前有效数据和最新说明文件；历史备份统一放入对应目录的 `_archive/backups/`。

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

当前 EasyDesign baseline 相关文件：

- `diagnostic_activity_v0.csv`：候选诊断活性 v0 主表。
- `diagnostic_activity_feature_table_v0.csv`：第一次 baseline 推荐入口，包含基础序列特征。
- `diagnostic_activity_augmented_optional_v0.csv`：可选增强数据，默认不要混入 baseline。
- `baseline_data_usage_guide_zh.md` / `baseline_data_usage_guide_en.md`：如何使用 v0 数据运行第一次 baseline。
- `split_plan_zh.md` / `split_plan_en.md`：训练/验证/外部测试划分说明。
- `dataset_build_report_zh.md` / `dataset_build_report_en.md`：数据集构建记录。

历史备份位于 `04_candidate_ml_dataset/_archive/backups/`。

### `99_notes/`

审计、问题和决策记录。

- `*_data_audit*.md`：数据审计报告。
- `run_report*.md`：每轮脚本运行报告。
- `evidence_trace*.md`：关键判断的证据来源。
- `problems_to_resolve*.md`：仍需人工确认的问题。
- `method_notes*.md`：可用于论文 methods 的流程记录。

如果不确定某个字段含义，优先查这里，不要自己猜。

历史备份位于 `99_notes/_archive/backups/`。

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
6. 如需运行第一次 baseline，使用 `04_candidate_ml_dataset/diagnostic_activity_feature_table_v0.csv`，并先读 `baseline_data_usage_guide_zh.md` 或 `baseline_data_usage_guide_en.md`。
7. 遇到不确定问题，查 `99_notes/problems_to_resolve*.md`。

## 当前 EasyDesign baseline 说明

当前最成熟的数据主线是 EasyDesign 2024 的 `diagnostic_activity`。

推荐第一次 baseline：

- 输入文件：`04_candidate_ml_dataset/diagnostic_activity_feature_table_v0.csv`
- 默认训练集：`baseline_split == baseline_train`
- 默认验证集：`baseline_split == baseline_validation`
- 默认标签列：`label_normalized`
- 默认只使用：`label_is_primary_baseline == yes`

暂不默认使用：

- `external_test_scale_unconfirmed`：Table S5 外部测试集，label 尺度尚未与 Table S3 完全确认。
- `diagnostic_activity_augmented_optional_v0.csv`：增强数据，只有明确启用 augmentation 时才使用。
- `paper_prediction_*` 列：论文模型预测值，不是实验 label。

## 协作注意事项

- 新增数据源时，先更新 `00_data_catalog/`，再导出到 `02_extracted_tables/`。
- 不确定的字段或标签写入 `99_notes/problems_to_resolve.md`。
- 不要直接把不同论文、不同 assay、不同 label status 的数据合并成训练集。
- 每次整理都应留下脚本和 run report，方便复现。
