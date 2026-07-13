# Baseline 数据使用指南

## 推荐入口

- 默认文件：`EasyDesign_2024_diagnostic_activity_feature_table_v1.csv`，共 11,992 行、89 列。
- 基础对照：`EasyDesign_2024_diagnostic_activity_feature_table_v0.csv`。
- v1 保留 v0 的全部来源、序列、标签和 split 字段，并加入 60 个审计后的工程特征。
- 完整 139 特征结果位于 `feature_engineering/full_generated/`，仅用于追踪、复算和进一步研究，不是默认训练表。

## 训练与验证范围

- 只使用 `label_is_primary_baseline == yes` 且 `label_scale_group == table_s3_log_or_transformed_30min_activity` 的行。
- 训练集：`baseline_split == baseline_train`，8,417 行。
- 验证集：`baseline_split == baseline_validation`，2,217 行。
- 标签：`label_normalized`，对应 Table S3 的实验测得 30 分钟诊断活性读数。
- 不重新随机划分现有行；同一 target sequence 已通过 hash 规则固定到同一 split。

## 默认模型输入

可直接作为候选数值特征的字段包括：

- v0 基础特征：`crRNA_length`、`target_length`、`crRNA_GC_content`、`target_GC_content`、`guide_target_hamming_dist_computed`。
- v1 配对特征：`mismatch_count_shared_positions`、`mismatch_fraction_shared_positions`、首末错配位置、最长连续匹配/错配和 GC 差。
- v1 位置特征：`mismatch_pos_1` 至 `mismatch_pos_25`。
- v1 错配类型：全部 12 个 `mismatch_type_*` 计数。
- v1 序列特征：entropy、homopolymer、局部 GC，以及经参考重要性支持的少量 k-mer。

完整选择依据见 `feature_engineering/EasyDesign_2024_feature_selection_manifest_v1.csv`。

## 必须排除的字段

不要把以下字段送入模型：

- 标识与来源：`dataset_id`、`feature_table_version`、`source_id`、`source_table_id`、`record_id`、`paper_split`、`baseline_split`、`data_role`。
- 原始序列和说明：`crRNA_sequence`、`target_sequence`、`target_context_sequence`、`notes`；只有在使用专门序列编码器时才单独处理序列。
- 所有标签与标签元数据：`label_raw_name`、`label_raw_value`、`label_normalized`、`label_scale_group`、`label_is_primary_baseline`。
- `guide_target_hamming_dist_raw`：其原始语义尚未解决，虽然首轮重要性较高，仍不得作为默认输入。
- `pam`、`pam_type`：当前 PAM 是由 5' TTTN 前缀推断，不是独立原始列；确认序列定义前不作默认特征。
- `has_valid_DNA_alphabet`、`contains_ambiguous_base`：主 baseline 中为常量 QC 字段，不提供有效变化。

## 缺失值和方向边界

- 740 条 Table S3 记录的 target 短于 25 nt。v1 对未对齐的 `mismatch_pos_*` 写为空值，不能把这些空值解释为匹配。
- 支持原生 missing 的模型可保留为空；其他模型应使用 `-1` 等独立状态并同时保留 `target_length`，或增加显式对齐指示变量。
- `direct` 方向已在计算上复现现有 Hamming 列，但尚未从独立生物学证据确认。不要把 generic thirds 重命名为 PAM proximal、seed 或 distal。

## 暂不默认使用

- `baseline_split == external_test_scale_unconfirmed`：Table S5 的 1,358 行，标签尺度尚未与 Table S3 对齐。
- `EasyDesign_2024_diagnostic_activity_augmented_optional_v0.csv`：Table S4 增强数据，只有显式启用 augmentation 时才使用。
- `paper_prediction_*`：论文模型预测，不是实验标签。
- `evaluation/` 中的预测与特征重要性：仅作为结果审计和方法参考，不能替代可复现训练代码。

## 建议的第一次比较

1. 用 v0 五个基础数值特征运行控制组。
2. 用 v1 的已选工程特征运行增强组，保持相同 split 和评价指标。
3. 至少报告 Spearman、Pearson、MAE、RMSE 和 R2，并保存逐行预测。
4. 在独立复现训练代码前，不把参考改进结果写成项目已确认的最终性能。
