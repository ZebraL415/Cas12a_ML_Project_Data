# Baseline 数据使用指南

## 文件位置选择
这份文档放在 `04_candidate_ml_dataset/diagnostic_activity_easydesign/`，因为它直接说明 EasyDesign 诊断活性候选建模数据如何进入第一次 baseline workflow。原始提取表仍在 `02_extracted_tables/`，最小清洗表在 `03_cleaned_minimal/`，但 EasyDesign baseline 入口应从本目录读取。

## 推荐的第一次 baseline 输入
- 默认训练/验证文件：`EasyDesign_2024_diagnostic_activity_feature_table_v0.csv`。
- 只使用 `label_is_primary_baseline == yes` 的行。
- 训练集：`baseline_split == baseline_train`。
- 验证集：`baseline_split == baseline_validation`。
- 标签列：`label_normalized`，但只在 `label_scale_group == table_s3_log_or_transformed_30min_activity` 内使用。

## 暂不默认使用的数据
- `baseline_split == external_test_scale_unconfirmed`：这是 Table S5 外部测试集，保留 `true value`，但数值尺度与 Table S3 尚未确认。
- `EasyDesign_2024_diagnostic_activity_augmented_optional_v0.csv`：这是 Table S4 增强数据，只有显式启用 augmentation 时才使用。
- 所有 `paper_prediction_*` 列：这是论文模型预测值，只能用于复现实验对照或 sanity check，不是 label。

## 最低可运行 workflow
1. 读取 `EasyDesign_2024_diagnostic_activity_feature_table_v0.csv`。
2. 过滤 `label_is_primary_baseline == yes`。
3. 使用 `crRNA_sequence`、`target_sequence` 和基础数值特征做 baseline 特征。
4. 使用 `baseline_train` 训练，`baseline_validation` 验证。
5. 暂不报告 Table S5 外部测试性能，除非先解决 label scale transform。
