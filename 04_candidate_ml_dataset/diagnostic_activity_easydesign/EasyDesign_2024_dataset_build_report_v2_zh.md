# EasyDesign 2024 feature table v2 构建报告

## 输入和边界

v2 以 combined supplementary workbook 的 Table S2/Table S3、已有 feature table v0、原论文 PDF 和官方 GitHub 仓库为输入证据。`01_raw/` 未被修改；没有训练模型，没有并入 Table S4 augmentation，也没有把 Table S5 与 Table S3 标签强制统一。

## 构建结果

- v2 主表：11,992 行、188 列。
- Table S3：10,634 行，其中 9,894 行无 gap，740 行含 target-channel gap。
- Table S5：1,358 行，仅保留为尺度未确认的外部测试候选。
- 标签、`source_table_id` 和 `baseline_split` 与 v0 逐行一致。
- feature dictionary：145 行。
- Table S2：198 条模板，可按论文支持的 22 x 9 结构完整分组；所有组的长度模式通过自动 QC。
- 来源映射：10,633/10,634 条 Table S3 记录有精确或 IUPAC 兼容候选，7,421 high、3,146 medium、67 review。

## 与 v0 的关系

v0 保留为兼容版本。v2 新增 `target_aligned_25` 并保留 `-`，将旧 Hamming 保存为 `guide_target_hamming_dist_computed_v0_legacy`，再用 25 位直接对齐重算 `guide_target_hamming_dist_computed`。无 gap 的 9,894 行新旧计算完全一致；gap 的 740 行仅 33 行一致，因此 v0 的 gap 位置特征不应用于默认训练。

## 行处理

本轮未删除任何 v0 行。Table S3 行被分为 9,894 条 `eligible_core_v2` 和 740 条 `conditional_gap_aware_v2`；Table S5 行被标为 1,358 条 `external_test_only_scale_unconfirmed`。没有把无标签 Table S2 扫描结果加入实验训练数据。

## 仍有限制

官方公开材料未提供 Table S3 行到 Template No./plate/replicate 的权威对应表，也未找到生成 `target_at_guide` 或 `guide_target_hamming_dist` 的训练预处理脚本。v2 的 Table S2 mapping 因此是序列证据映射，不是作者提供的实验主键。`gap_in_target` 也是表示层事件，不足以单独判断生物学 insertion/deletion 方向。
