# diagnostic_activity_easydesign

本目录保存 EasyDesign_2024 的候选 diagnostic activity 数据。该数据属于 CRISPR-Cas12a diagnostics 活性路径，不能与 DeepCas12a editing activity 二分类标签合并。

## 当前文件

- `EasyDesign_2024_diagnostic_activity_feature_table_v0.csv`：第一次 EasyDesign baseline 推荐入口。
- `EasyDesign_2024_diagnostic_activity_v0.csv`：候选诊断活性主表。
- `EasyDesign_2024_diagnostic_activity_augmented_optional_v0.csv`：可选增强数据，默认不要混入主 baseline。
- `EasyDesign_2024_baseline_data_usage_guide_zh.md` / `EasyDesign_2024_baseline_data_usage_guide_en.md`：数据使用说明。
- `EasyDesign_2024_split_plan_zh.md` / `EasyDesign_2024_split_plan_en.md`：划分说明。
- `EasyDesign_2024_dataset_build_report_zh.md` / `EasyDesign_2024_dataset_build_report_en.md`：构建报告。

## 使用原则

- 默认标签列是 `label_normalized`。
- 默认只使用 `label_is_primary_baseline == yes` 的行。
- `paper_prediction_*` 字段是论文模型预测值，不是实验标签。
- Table S4 增强数据只有在明确启用 augmentation 时才使用。
- 历史备份位于 `_archive/backups/`。
