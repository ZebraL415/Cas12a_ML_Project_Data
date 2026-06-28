# 待解决问题 EasyDesign_2024 第二轮

## 已解决
- `30 min`：PDF 方法部分确认 30 分钟荧光值被选为活性指标；本轮作为 Table S3 内部 baseline 的主标签。
- `20 min normalized`：PDF 确认它是 20 分钟读数归一到 30 分钟的派生/增强标签；不并入主标签。
- `out_logk_measurement`：对应 Table S4 增强数据；本轮单独保存为 optional augmentation，不进入默认 baseline。
- `true value`：对应 Table S5 测试集实验真值；保留为 external paper test，但与 Table S3 数值尺度仍需确认。
- standalone workbook 与 combined source-data workbook：以 combined workbook 为权威来源，standalone 表视为重复来源。
- figure source data：保留为证据或 metadata，不直接作为 tidy crRNA-target 训练行。
- `guide-expected-activities` 和模型列：全部归为 predicted score，不是 primary training label。
- PAM：PDF 支持 TTTN PAM；Excel 无独立 PAM 列，本轮只从序列 5' 端 TTTN 前缀推断并标记为 inferred。
- Fig.S3：属于特征/活性相关的聚合图源数据，不作为逐条训练标签。

## 仍需确认
- Table S3 的负值 `30 min` 标签与 Table S5 的正值 `true value` 是否可通过已知转换映射到同一尺度，仍需人工确认或方法学决定。
- Table S3 原始 `guide_target_hamming_dist` 与从 `guide_seq`/`target_at_guide` 直接计算的 mismatch 并不总一致；该原始列的真实语义仍需确认。
- Excel 中没有明确独立 PAM 列；当前 PAM 仅根据 TTTN 前缀推断，后续若要作为模型特征需要确认序列定义。
- Table S5 有少数 DNA context 不是 45 nt；这些行使用 best-match fallback 定位 target window，后续应人工复核。
- Table S4 增强数据是否进入首个正式训练流程，需要在模型方案确定后决定。
- Table S3 只有 type1/type2，不含具体 pathogen 名称；如果要做物种分组验证，需要额外映射。
