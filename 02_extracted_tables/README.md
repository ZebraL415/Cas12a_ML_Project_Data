# 02_extracted_tables

本目录保存从 `01_raw/` 拆出的中间表。这里保留原始列名和数值语义，只要求可打开、可追溯，不是最终训练集。

- `diagnostic_activity/`：荧光/RFU/诊断活性；EasyDesign mismatch 来源表位于 `diagnostic_activity/easydesign_mismatch_mapping/`。
- `editing_activity/`：indel frequency、editing efficiency 或二分类 editing activity。
- `snv_annotation/`：SNV、WT/alt 序列和注释。
- `snv_specificity/`：WT/mutant 区分和 specificity ratio。
- `predicted_library/`：模型预测分数或候选库，不能当实验标签。

文件名应包含来源、年份、table/sheet ID、数据类型和 `raw`。进入标准化流程后输出到 `03_cleaned_minimal/`；不同标签体系不得在本层合并。历史数据备份放对应子目录 `_archive/backups/`。
