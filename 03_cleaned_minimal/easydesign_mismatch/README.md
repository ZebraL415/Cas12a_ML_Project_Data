# EasyDesign gap-aware 最小清洗表

本目录保存从权威 combined workbook 重建的 EasyDesign Table S3 对齐和来源映射。

- `EasyDesign_2024_guide_target_alignment_v2.csv`：10,634 条 Table S3 实验记录；保留 25 位 `target_aligned_25`、无 gap 的 `target_ungapped`、逐位事件和原始标签。
- `EasyDesign_2024_source_mapping_v1.csv`：每条记录的来源映射状态、置信等级和全部候选模板摘要。
- `EasyDesign_2024_mismatch_qc_v2.csv`：含 gap、原始 Hamming 不一致或来源映射非 high 的复核队列。

`gap_in_target` 只描述 Table S3 对齐表示中 target 通道该位置为 `-`，不等同于已确认的生物学 deletion 方向。默认 baseline 使用 `alignment_qc_status == pass_no_gap`；gap 行只能通过 gap-aware workflow 有条件纳入。
