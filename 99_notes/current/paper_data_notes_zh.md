# 当前论文数据备注

## EasyDesign_2024

- 论文：Huang et al., *Deep learning enhancing guide RNA design for CRISPR Cas12a-based diagnostics*, iMeta 2024，DOI `10.1002/imt2.214`。
- 数据路径：`diagnostic_activity`；主实验标签为 Table S3 `30 min` fluorescence activity。
- 论文方法说明 22 个 original DNA templates，每个对应 6 substitution、1 insertion、1 deletion 变体，共 198 条 Table S2 templates。
- insertion/deletion 使用 `-` 作为 target DNA 或 crRNA 的 alignment placeholder，并与 A/C/T/G 组成五状态 one-hot；每个位点 target+guide 为 10 维。
- 公开仓库：`https://github.com/scRNA-Compt/EasyDesign`；本轮检查 commit `5c06a30d0a43be28a958831587f6ab706c2d4876` 的 main/dev/可见历史，未找到生成 `target_at_guide` 或 `guide_target_hamming_dist` 的训练预处理脚本。
- 论文只说明每个 96-well plate 的两个阴性孔、两个阳性重复孔及归一化方法，没有公开逐行 plate/well/template/replicate 对应表。
- v2 保留 10,634 条 Table S3 记录的 25 位对齐，其中 740 条含 target-channel gap；第一次 baseline 推荐 9,894 条无 gap 行。
- Table S2 序列证据映射覆盖 10,633 条，但 mapping 是审计元数据，不是实验标签或默认模型输入。

## DeepCas12a_2026

- 数据路径：`editing_activity`。
- label 是 AsCas12a editing activity 二分类标签，不是 fluorescence/RFU，也不与 EasyDesign 合并。
