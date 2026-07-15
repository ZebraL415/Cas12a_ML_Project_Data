# EasyDesign feature engineering v2

本目录记录 `EasyDesign_2024_diagnostic_activity_feature_table_v2.csv` 的特征定义和自动 QC。

- `EasyDesign_2024_feature_dictionary_v2.csv`：145 个新增或关键字段的输入、公式、gap 行为和默认模型角色。
- `EasyDesign_2024_feature_qc_v2.json`：行数、标签/split 保真、gap 分层、Hamming 对照和 pair-level split 泄漏检查。

默认候选输入只包括 `default_model_role == candidate_input` 的字段。`source_mapping`、原始 Hamming、标签、来源 ID 和 QC 字段不得作为默认数值特征。
