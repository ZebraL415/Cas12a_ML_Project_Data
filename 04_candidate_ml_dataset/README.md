# 04_candidate_ml_dataset

本目录保存候选建模数据。顶层只作为导航页；具体数据集按 `path_type + source` 放入子目录，避免不同任务、不同标签体系混在一起。

## 子目录

- `diagnostic_activity_easydesign/`：EasyDesign_2024 诊断活性候选数据。标签来自 CRISPR fluorescence/activity 体系。
- `editing_activity_deepcas12a/`：DeepCas12a_2026 编辑活性候选数据。标签是 AsCas12a editing activity 二分类。
- `snv_specificity_extension/`：SNV specificity extension 预留目录，目前只有空占位表。

## 使用原则

- 先进入对应子目录阅读 `README.md` / `README_en.md`。
- 不要跨子目录直接合并标签；diagnostic activity、editing activity、SNV specificity 是不同任务。
- 每个子目录自己管理当前 v0 文件、使用指南、split plan、build report 和 `_archive/backups/`。
- 顶层不再存放具体数据表。

## 推荐入口

- EasyDesign baseline：`diagnostic_activity_easydesign/EasyDesign_2024_diagnostic_activity_feature_table_v0.csv`
- DeepCas12a baseline：`editing_activity_deepcas12a/DeepCas12a_2026_editing_activity_feature_table_v0.csv`
