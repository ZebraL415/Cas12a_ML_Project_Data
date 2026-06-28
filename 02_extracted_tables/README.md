# 02_extracted_tables

本目录保存从原始文件中拆出的中间表。这里的表通常仍保留原始列名和原始数值，不是最终训练集。

## 子目录含义

- `diagnostic_activity/`：诊断活性相关表，例如 crRNA-target pair、荧光、RFU、activity score。
- `editing_activity/`：编辑活性相关表，例如 indel frequency 或 editing efficiency。
- `snv_annotation/`：SNV 注释、WT/alt 序列或变异信息。
- `snv_specificity/`：SNV 区分能力、WT/mutant 比值或特异性实验结果。
- `predicted_library/`：预测库、模型打分或候选设计结果。

## 使用原则

- 本层只做“可打开、可追溯”的拆表，不做跨标签合并。
- 文件名应包含来源、年份、表格或 sheet ID、数据类型和 `raw` 状态。
- 若表格进入清洗流程，标准化输出应写入 `03_cleaned_minimal/`。

## 归档

各子目录的历史备份放入对应的 `_archive/backups/`。子目录首页只保留当前有效导出表。
