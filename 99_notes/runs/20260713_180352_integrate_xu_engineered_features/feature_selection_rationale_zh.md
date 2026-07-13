# v1 特征筛选依据

## 保留原则

v1 是模型无关的候选特征表，不按单次 XGBoost 排名机械截取 top N。特征需要同时满足：可由序列确定性复算、不使用预测值或标签派生值、具有可解释含义、与现有字段不完全重复，并由参考重要性或完整特征家族支持。

## 纳入的 60 个工程特征

- 7 个配对特征：共享位置错配数/比例、首末错配位置、最长匹配/错配连续段和 GC 差。
- 25 个位置特征：`mismatch_pos_1` 至 `mismatch_pos_25`，作为完整家族保留，避免只选择一次运行中的位置 2 和 4。
- 12 个错配类型计数：A/C/G/T 的所有非同碱基方向组合。
- 16 个序列特征：guide/target entropy、homopolymer、局部 GC，以及参考 top30 支持的 TTT、AAA、GA、GT、AG k-mer。

## 主要排除

- `mismatch_count_validated`：与 `guide_target_hamming_dist_computed` 100% 重复。
- `match_fraction_shared_positions`：与 mismatch fraction 完全互补。
- engineered length/GC：与 v0 长度和 GC 字段重复。
- `aligned_length` 与 `target_length` 完全相同；`length_difference` 可由现有长度精确推出。
- generic thirds：不能在当前证据下重命名为 proximal/middle/distal 生物学区域。
- 位置 26 至 30：超出本数据 25 nt 最大对齐长度。
- 未入选的完整 k-mer 集：可以复算，但会显著扩张表宽；当前参考重要性不足以支持全部纳入紧凑 v1。
- `guide_target_hamming_dist_raw`：保留在表中用于追踪，但默认模型必须排除，因为其来源语义仍未解决。

逐列结果见 `04_candidate_ml_dataset/diagnostic_activity_easydesign/feature_engineering/EasyDesign_2024_feature_selection_manifest_v1.csv`。
