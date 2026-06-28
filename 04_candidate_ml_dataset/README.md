# 04_candidate_ml_dataset

本目录保存候选建模数据。只有标签较清楚、record unit 相对一致、来源可追溯的数据才进入这里。

## 第一次 baseline 推荐入口

- `diagnostic_activity_feature_table_v0.csv`：推荐用于第一次 baseline workflow 的输入表。
- `diagnostic_activity_v0.csv`：候选诊断活性主表，保留更接近数据集定义的字段。
- `diagnostic_activity_augmented_optional_v0.csv`：可选增强数据，默认不要与主 baseline 混合。

## 配套说明

- `baseline_data_usage_guide_zh.md` / `baseline_data_usage_guide_en.md`：如何使用候选数据运行 baseline。
- `split_plan_zh.md` / `split_plan_en.md`：推荐划分方式。
- `dataset_build_report_zh.md` / `dataset_build_report_en.md`：数据构建记录。

## 使用原则

- 默认标签列是 `label_normalized`。
- 默认只使用 `label_is_primary_baseline == yes` 的行。
- `paper_prediction_*` 字段是论文模型预测值，不是实验标签。
- 训练模型前必须再次确认 split、label_status 和数据来源。

## 归档

历史备份放在 `_archive/backups/`。目录首页只保留当前 v0 数据和最新说明。
