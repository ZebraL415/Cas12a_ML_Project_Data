# DeepCas12a_2026 数据使用指南

## 推荐入口

第一次 DeepCas12a editing activity baseline 使用：

`DeepCas12a_2026_editing_activity_feature_table_v0.csv`

## 默认任务

- path_type：`editing_activity`
- 任务类型：二分类
- 标签列：`label_normalized`
- 正类：`1`，high AsCas12a on-target activity
- 负类：`0`，low AsCas12a on-target activity
- 输入主序列：`target_context_sequence`
- PAM：`pam_sequence`，由 34 bp sequence 的 positions 5-8 推断
- protospacer：`protospacer_sequence`，由 positions 9-31 推断

## PAM 说明

所有候选行的 `pam_sequence` 都是 `TTTN`。其中 4,500 行为 `TTTT`，不满足严格 `TTTV`；本轮不删除这些行，而是在 feature table 中用 `pam_matches_TTTV` 标记。

## 推荐划分

- 训练：`default_split == baseline_train`
- HT1 holdout 测试：`default_split == holdout_test_HT1-2`
- 独立测试：`default_split == independent_test_HT2` 和 `default_split == independent_test_HT3`
- 内部 9-fold validation：使用 `DeepCas12a_2026_9fold_partitions_v0.csv`

## 禁止事项

- 不要和 EasyDesign 的 fluorescence/RFU diagnostic activity 标签合并。
- 不要把 `label` 当作连续 indel frequency。
- 不要把 HT 标准化 epigenetic 特征解释为真实整合位点 methylation/DNase 状态。
- 不要在没有方法学决定前直接过滤 `TTTT` PAM 行。
