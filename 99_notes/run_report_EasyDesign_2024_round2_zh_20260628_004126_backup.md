# EasyDesign_2024 第二轮运行报告

## 范围
输入数据源：`01_raw/EasyDesign_2024`、原论文 PDF、补充资料截图。

## 本轮生成文件
- `00_data_catalog/master_data_catalog.xlsx`
- `00_data_catalog/source_sheet_index.xlsx`
- `00_data_catalog/label_dictionary.xlsx`
- `03_cleaned_minimal/diagnostic_activity_minimal.csv`
- `03_cleaned_minimal/diagnostic_activity_augmented_optional.csv`
- `04_candidate_ml_dataset/diagnostic_activity_v0.csv`
- `04_candidate_ml_dataset/diagnostic_activity_feature_table_v0.csv`
- `04_candidate_ml_dataset/diagnostic_activity_augmented_optional_v0.csv`

## 分类判断
- Table S3：diagnostic_activity，高优先级，内部 baseline 主表。
- Table S4：diagnostic_activity，高优先级，但作为 optional augmentation。
- Table S5：diagnostic_activity，高优先级，external paper test；预测列不作为标签。
- Table S7/S8：experimental validation metadata。
- Fig.S3：metadata/figure source data，不作为训练数据。

## 数据质量检查
- primary v0 总行数：11992。
- feature table 总行数：11992。
- Table S5 的 45 nt DNA context 均可定位到 25 nt target window；窗口起点统计：{"10": 1339, "7": 8, "1": 8, "9": 3}。
- Table S3 中 unique target_at_guide：8621。

## 下一步建议
- 第一次 baseline 先使用 `baseline_split` 中的 baseline_train/baseline_validation。
- 不要把 Table S4 加入默认 baseline，除非显式启用 augmentation。
- 在确认 label transform 前，不要把 Table S5 与 Table S3 作为同尺度评价。
