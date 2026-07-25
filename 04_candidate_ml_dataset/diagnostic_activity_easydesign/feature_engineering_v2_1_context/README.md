# EasyDesign feature engineering v2.1 context

本目录保存不覆盖 V2 的版本化上下文扩展。父表为 `EasyDesign_2024_diagnostic_activity_feature_table_v2.csv`。

## 文件

- `EasyDesign_2024_diagnostic_activity_feature_table_v2_1_context.csv`：11,992 行 × 246 列；父表 188 列加 58 个上下文特征。
- `EasyDesign_2024_feature_dictionary_v2_1_context.csv`：完整字段与公式词典。
- `EasyDesign_2024_sequence_context_feature_dictionary_v2_1.csv`：仅新增 58 列的词典。
- `v2_1_final_feature_manifest.csv`：V2-1 冻结的 188 个名义模型输入及常数列状态。
- `v2_1_context_build_qc.json`、`v2_1_context_independent_verification.json`：构建和独立 QC。
- `v2_1_context_build_report_zh.md` / `_en.md`：双语构建报告。

## 使用

模型输入以 `v2_1_final_feature_manifest.csv` 为准。每个训练折仅用训练数据拟合中位数，剩余缺失填 0，再移除该训练折内的常数列。位置 mismatch/gap 特征继续来自 `target_aligned_25`；`sequence_context` 只来自 `crRNA_sequence` 和 `target_ungapped`。

V2-1 实验证据位于 `/Users/linzibo/Cas12a_ML_Project_Expr/V2-1_feature_block_ablation/`。该表不得与 DeepCas12a `editing_activity` 合并。

英文版见 `README_en.md`。
