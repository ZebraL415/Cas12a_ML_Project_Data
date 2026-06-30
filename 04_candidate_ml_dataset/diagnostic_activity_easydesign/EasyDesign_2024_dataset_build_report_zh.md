# 数据集构建报告

## 输入
- 权威 workbook：`01_raw/EasyDesign_2024/data/imt2214-sup-0002-tables1-9sourcedata (1).xlsx`。
- 证据源：原论文 PDF、补充资料截图、上一轮 catalog。

## 输出数据
- `EasyDesign_2024_diagnostic_activity_v0.csv`：11992 行，包含 Table S3 primary internal baseline 与 Table S5 external paper test。
- `EasyDesign_2024_diagnostic_activity_feature_table_v0.csv`：11992 行，包含基础序列特征。
- `EasyDesign_2024_diagnostic_activity_augmented_optional_v0.csv`：31993 行，包含 Table S4 optional augmentation。

## 保留/排除规则
- 保留原始 record id、source_table_id、source_sheet、label_raw_name、label_scale_group。
- 不把 30 min、20 min normalized、out_logk_measurement、true value 强行合并为同一标签。
- 不把 paper model prediction columns 当作 label。
