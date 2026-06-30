# 运行报告：Organize Candidate ML Datasets By Source Path

## 范围

本轮只整理 `04_candidate_ml_dataset/` 的目录结构和 README，不修改 `01_raw/`。

## 已完成

- 新建 `diagnostic_activity_easydesign/`，存放 EasyDesign_2024 diagnostic activity v0 数据、使用指南、split plan 和 build report。
- 将 EasyDesign 当前文件重命名为带来源前缀的文件名，例如 `EasyDesign_2024_diagnostic_activity_feature_table_v0.csv`。
- 将原顶层 `_archive/backups/` 中的 EasyDesign 历史备份移入 `diagnostic_activity_easydesign/_archive/backups/`。
- 新建 `snv_specificity_extension/`，移动空占位表 `snv_specificity_extension_v0.csv`。
- 保留 `editing_activity_deepcas12a/` 作为 DeepCas12a_2026 editing activity 数据目录。
- 更新 `04_candidate_ml_dataset/README.md` 和 `README_en.md`，使顶层只作为导航页。
- 更新根目录 README 中指向 04 的路径。

## 判断

`04_candidate_ml_dataset/` 应按任务路径和来源组织，而不是把所有 v0 数据表混放在顶层。这样可以避免 EasyDesign 的 diagnostic activity 标签与 DeepCas12a 的 editing activity 标签被误合并。
