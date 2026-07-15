# 本轮结束时仍需解决的问题

1. 未在官方公开仓库 main、dev 或可见历史中找到生成 `target_at_guide` 和 `guide_target_hamming_dist` 的训练预处理代码；若作者另有未公开脚本，仍需取得。
2. 未找到 Table S3 `No.` 到 Table S2 `Template No.`、plate/well、实验 replicate 或合成模板 ID 的权威对应表。
3. `-` 已确认是 target/crRNA 五状态编码中的 alignment gap，但每行的生物学 insertion/deletion 方向仍不能仅从 Table S3 确认。
4. 官方 predictor 给 `-` 分配 one-hot 索引，但 `onehot()` 依赖的 `FASTA_CODES` 不含 `-`；需作者确认真实运行或训练版本。
5. 188 条 raw Hamming 与直接对齐计数不一致，不能把 raw Hamming 作为默认特征。
6. 67 条来源映射为 review；`EasyDesign_2024_TableS3_09121` 无精确或 IUPAC 兼容命中。
7. Table S3 `30 min` 与 Table S5 `true value` 的尺度转换仍未确认。
8. 少数 Table S5 DNA context 不是 45 nt；其 target window 仍需人工复核。
9. Table S4 augmentation 是否进入正式训练流程，应在模型方案确定后决定。
10. Table S3 缺少具体 pathogen 名称；若做物种分组验证，需要额外权威映射。
