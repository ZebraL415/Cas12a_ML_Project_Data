# 方法记录

徐同学提供的工程特征脚本以 EasyDesign v0 特征表为输入，在 direct、complement、reverse 和 reverse-complement 四种 target 表示下计算 guide-target Hamming 距离，并以现有 `guide_target_hamming_dist_computed` 的精确一致率选择计算表示。选定 direct 后，脚本生成单序列组成、局部 GC、k-mer、配对错配数量、位置和类型特征，同时输出方向比较、逐行审计、特征词典和生成报告。

完整生成表通过 `record_id`、行顺序、序列、split 和标签与 v0 逐行核对。项目构建脚本保留 v0 全部字段，从完整生成表筛选 60 个无标签泄漏、可解释且不简单重复的工程特征。由于部分 target 短于 guide，未对齐的 position-specific mismatch 单元被编码为空值，而不是匹配值 0。所有区域三等分特征因缺少独立生物学方向确认而排除。

参考预测文件只用于验证保存结果的一致性。评价指标由逐行 `label_normalized` 和 `predicted_activity` 重新计算；本轮未拟合或训练任何模型。
