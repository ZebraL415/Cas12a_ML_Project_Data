# EasyDesign v2.1 上下文特征表构建报告

## 范围

本层以只读 V2 gap-aware core 为父表，逐行从 `crRNA_sequence` 和 `target_ungapped` 重算 58 个序列上下文特征。未重算或覆盖 `target_aligned_25` 及其 mismatch/gap 位置特征，标签、split、来源字段与记录顺序均保持不变。

## 结果

- 父表：`/Users/linzibo/Cas12a_ML_Project_Data/04_candidate_ml_dataset/diagnostic_activity_easydesign/EasyDesign_2024_diagnostic_activity_feature_table_v2.csv`
- 输出表：`/Users/linzibo/Cas12a_ML_Project_Expr/V2-0_unified_baseline/runs/20260724T010300_V2-0-v2.1-context-build/EasyDesign_2024_diagnostic_activity_feature_table_v2_1_context.csv`
- 行数：11,992
- 父表列数：188
- 新增上下文列数：58
- 输出总列数：246
- 候选模型输入：188 个
- 输出 SHA-256：`39cda8368c216784507ac002df687b28a4f9cc6f81e2b0e84043e45eddb4c1c0`

## 质量控制

- 通过：`expected_58_context_features`
- 通过：`no_missing_context_values`
- 通过：`all_context_values_finite`
- 通过：`frequency_and_gc_values_in_0_1`
- 通过：`unique_base_count_in_1_4`
- 通过：`dinucleotide_frequencies_sum_to_one`
- 通过：`target_ungapped_contains_no_gap`
- 通过：`record_id_unique`
- 通过：`record_id_and_order_unchanged`
- 通过：`parent_columns_value_exact_after_roundtrip`
- 通过：`no_duplicate_output_columns`
- 通过：`expected_output_shape`
- 通过：`candidate_input_count_188`
- 通过：`label_unchanged`
- 通过：`split_unchanged`
- 通过：`source_table_id_unchanged`

## 使用边界

该表是 V2 的版本化候选扩展，不替代或覆盖 V2。`sequence_context` 已通过单 seed 的训练集内部 grouped CV，仍须在 V2-1 中完成多 seed 与整块消融后，才能决定其正式模型输入地位。
