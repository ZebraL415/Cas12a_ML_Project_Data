# 03_cleaned_minimal

本目录保存最小标准化表。这里的数据已经从原始列名整理成可比较字段，但仍不是最终机器学习训练集。

## 当前重点文件

- `diagnostic_activity_minimal.csv`：EasyDesign 诊断活性最小清洗主表。
- `diagnostic_activity_augmented_optional.csv`：可选增强数据，默认不混入 baseline。
- `README_cleaning_notes.md`：清洗注意事项。
- 其他 `*_minimal.csv`：为后续路径预留或待进一步整理。

## 使用原则

- 每行应能追溯到 source、source table、record ID 和原始标签列。
- `label_status` 必须明确区分 measured、predicted、annotation、metadata 或 unclear。
- 不确定字段不要强行标准化，应记录到 `99_notes/problems_to_resolve.md`。

## 归档

历史备份统一放在 `_archive/backups/`。目录首页只保留当前最小清洗版本。
