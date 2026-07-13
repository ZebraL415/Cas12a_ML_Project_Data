# 证据链

## 决定 1：保留徐同学脚本原件

证据：接收文件 SHA-256 为 `cf8cd2f...a1830`；脚本可在当前 v0 表上无修改运行。

处理：原件保存于 `scripts/contributions/xu/`，项目修正写入独立的 v1 构建脚本。

## 决定 2：计算方向使用 direct，但不称为生物学已验证

证据：`direct` 对计算 Hamming 精确一致率 1.0；其他三种方向接近 0。脚本自身也声明仍需来源文档确认生物学约定。

处理：允许按 direct 复算配对特征；所有 proximal/seed/distal 解释仍标记未确认。

## 决定 3：不直接采用全部重要性高的列

证据：`eng_mismatch_count` 与现有计算 Hamming 完全重复；`eng_match_fraction + eng_mismatch_fraction = 1`。原始 Hamming 语义仍未解决。

处理：v1 去除简单重复和未解决语义字段，只保留一个可解释表示。

## 决定 4：位置特征成组保留并修正未对齐编码

证据：位置 2、4 在参考结果中重要，但 740 条主 baseline target 短于 25 nt；原脚本把不存在的位置写为 0。

处理：保留 1 至 25 的完整位置家族，未对齐位置写为空值，并使用现有 `target_length` 解释对齐范围。

## 决定 5：参考改进结果只作为内部一致的参考

证据：逐行预测与项目验证集完全匹配，指标可重算；但缺少训练代码、参数、依赖和随机种子。

处理：复制到 `evaluation/reference_improved_feature_run/`，不称为独立复现或最终模型性能。
