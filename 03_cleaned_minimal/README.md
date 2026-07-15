# 03_cleaned_minimal

本目录保存可追溯的最小标准化表和 QC 表。这里开始统一 source、record、sequence 和 label 字段，但仍不是最终训练集。

- `diagnostic_activity_minimal.csv`：EasyDesign 诊断活性最小主表。
- `diagnostic_activity_augmented_optional.csv`：可选 augmentation，默认不进 baseline。
- `easydesign_mismatch/`：Table S3 保留 gap 的 alignment v2、Table S2 source mapping 和 mismatch review queue。
- `editing_activity_minimal.csv`：DeepCas12a editing activity 最小表。
- 其他 `*_minimal.csv`：对应独立标签路径。

每行必须能追溯到 source、source table、record ID 和原始标签。`label_status` 必须区分 measured、predicted、annotation、metadata 或 unclear。不确定字段写入 `99_notes/current/`。历史备份放 `_archive/backups/`。
