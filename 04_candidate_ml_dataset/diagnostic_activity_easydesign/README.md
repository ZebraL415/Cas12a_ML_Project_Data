# diagnostic_activity_easydesign

本目录保存 EasyDesign_2024 `diagnostic_activity` 候选数据。标签是 Cas12a diagnostics 实验荧光活性，不能与 DeepCas12a 二分类 `editing_activity` 合并。

## 推荐入口

- `EasyDesign_2024_diagnostic_activity_feature_table_v2.csv`：当前推荐 baseline 输入，gap-aware，11,992 行、188 列。
- `EasyDesign_2024_v2_data_usage_guide_zh.md` / `_en.md`：运行任何模型前必读。
- `EasyDesign_2024_dataset_build_report_v2_zh.md` / `_en.md`：v2 来源、行数、修正和限制。
- `feature_engineering_v2/`：145 行特征词典和自动 QC。

第一次 baseline 只使用 `default_training_eligibility == eligible_core_v2`，再按现有 `baseline_split` 分训练/验证，共 9,894 条无 gap Table S3 记录。740 条 `conditional_gap_aware_v2` 只能在模型显式支持 gap 时加入；Table S5 的 1,358 条外部测试记录不能进入训练。

## 兼容和可选文件

- `EasyDesign_2024_diagnostic_activity_feature_table_v0.csv`：保留用于历史复现；其中删除 gap 后的旧位置特征不适用于 740 条 indel 行。
- `EasyDesign_2024_diagnostic_activity_v0.csv`：v0 候选主表。
- `EasyDesign_2024_diagnostic_activity_augmented_optional_v0.csv`：Table S4 augmentation，默认不使用。
- 原 v0 usage guide、split plan 和 build report：仅用于复现旧版。

`mapping_*` 是来源审计字段，不是标签，也不应作为默认数值模型输入。历史备份放 `_archive/backups/`。
