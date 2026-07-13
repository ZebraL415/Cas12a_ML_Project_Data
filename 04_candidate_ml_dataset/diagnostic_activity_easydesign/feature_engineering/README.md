# EasyDesign 特征工程

本目录保存 EasyDesign 特征工程的完整产物和筛选记录。

- `EasyDesign_2024_feature_selection_manifest_v1.csv`：逐特征说明是否进入 v1、参考重要性、选择或排除理由。
- `EasyDesign_2024_feature_table_v1_qc.json`：v1 构建后的行列数、split、重复和位置缺失编码检查。
- `full_generated/`：徐同学脚本原样复跑得到的完整 139 特征、方向比较、逐行审计、特征词典和生成报告。

默认训练入口仍是上一级的 `EasyDesign_2024_diagnostic_activity_feature_table_v1.csv`。完整生成表用于追踪和后续研究，不能因列更多就自动视为更优模型输入。
