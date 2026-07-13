# 完整生成结果

这些文件由徐同学提供的 `generate_validated_engineered_features.py` 对 v0 特征表原样复跑生成。它们保留全部工程特征和 QC，便于追踪，不是默认训练入口。

方向比较选择 `direct`，对 10,634 条主 baseline 行与 `guide_target_hamming_dist_computed` 的一致率为 100%，但对原始 `guide_target_hamming_dist_raw` 的一致率为 91.593%。这不解决原始 Hamming 列语义，也不构成独立生物学方向确认。
