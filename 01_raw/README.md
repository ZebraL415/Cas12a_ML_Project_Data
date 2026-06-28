# 01_raw

本目录是原始数据仓库，保存论文 PDF、补充表格、GitHub 仓库、README、source data、压缩包等原始来源文件。

## 核心规则

- 原始文件只读，不重命名、不覆盖、不清洗、不直接修改。
- 处理脚本只能从这里读取数据，输出应写入 `02_extracted_tables/`、`03_cleaned_minimal/` 或 `04_candidate_ml_dataset/`。
- 若需要记录原始文件含义，请写入 `00_data_catalog/` 或 `99_notes/`，不要改写原始来源文件。

## 当前来源子目录

- `DeepCpf1_Kim2018/`
- `DeepCas12a_2026/`
- `EasyDesign_2024/`
- `AdvancedScience_2025/`
- `ARTEMIS_2024/`
- `HEPSD_NAR2025/`
- `Iterative_PAMfree_2024/`

## 说明

本 README 是项目层面的使用说明，不属于任何论文或数据库的原始材料。
