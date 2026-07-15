# 当前待解决问题

本文件记录当前仍需人工确认的问题，并按数据源分组。

## EasyDesign_2024

### 已解决

- `30 min`：论文方法确认 30 分钟荧光值用于活性评估；作为 Table S3 内部 baseline 主标签。
- `20 min normalized`：论文确认它是 20 分钟读数归一到 30 分钟的派生标签；不并入主标签。
- `out_logk_measurement`：属于 Table S4 augmentation；单独保存，不进入默认 baseline。
- `true value`：属于 Table S5 实验真值；保留为 external paper test，但尺度仍需确认。
- PAM：论文支持 TTTN；Excel 无独立 PAM 列，只能从 5' TTTN 前缀推断并标记 inferred。
- standalone workbooks 与 combined workbook 的实际 sheet 内容已经登记；combined workbook 继续作为权威来源。
- Table S2 的 198 条模板可按论文和长度模式重建为 22 x 9：original、6 substitution、1 insertion、1 deletion。
- `-` 已确认是 target/crRNA 五状态 one-hot 中的统一 alignment-gap 占位符，不应删除后再计算位置特征。
- 已建立保留全部并列命中的 Table S2 来源映射：10,633/10,634 条有候选，按 high/medium/review 分层。
- 已生成 gap-aware feature table v2；v0 标签、来源表和 split 均未改变，无 gap 子集可支持第一次 baseline。

### 仍需确认

- Table S3 `30 min` 与 Table S5 `true value` 是否存在可复核的同尺度转换。
- 188 条 raw `guide_target_hamming_dist` 与 25 位直接对齐计数不一致；该原始列不得作为默认训练特征。
- 官方公开仓库 main、dev 和可见历史中未找到生成 `target_at_guide`/`guide_target_hamming_dist` 的训练预处理代码；仍需作者未公开版本或书面说明。
- 未找到 Table S3 `No.` 到 Table S2 `Template No.`、plate/well、实验 replicate 或 crRNA-template pairing 的权威对应表。
- `-` 的对齐含义已确认，但每条记录的生物学 insertion/deletion 方向不能仅由 target 通道的 `-` 确认；v2 的 `gap_in_target` 只表示对齐状态。
- 官方 predictor 给 `-` 分配 one-hot 索引，但 `onehot()` 依赖的 `FASTA_CODES` 不含 `-`；需作者确认真实训练/运行版本。
- 67 条 mapping 为 review；其中 50 条跨多个模板组、16 条仅 IUPAC 兼容、`EasyDesign_2024_TableS3_09121` 未映射。
- 少数 Table S5 DNA context 不是 45 nt，其 target window 仍需人工复核。
- Table S4 augmentation 是否进入正式训练，应在模型方案确定后决定。
- Table S3 只有 type1/type2，没有具体 pathogen 名称；物种分组验证需要额外权威映射。

<!-- BEGIN DeepCas12a_2026 -->
## DeepCas12a_2026

### 已确认

- DeepCas12a 属于 `editing_activity`，不是 `diagnostic_activity`。
- `label` 是二分类 AsCas12a on-target activity 标签，不能当作 fluorescence/RFU。
- 34 bp `sequence` 是 target-context sequence，包含 upstream context、PAM、protospacer 和 downstream context。
- HT methylation/DNase 特征是仓库说明中的标准化模型输入，不应解释为未知整合位点的真实 epigenetic 状态。
- 所有候选行 PAM 均为 `TTTN`；其中 4,500 行为 `TTTT`，不满足严格 `TTTV`，本轮保留并标记。

### 仍需确认

- 仓库只提供 model-ready binary labels；若需要连续 indel frequency，需追溯 Kim et al. 原始数值。
- 34 bp target-context 可推断 PAM/protospacer，但没有独立 crRNA sequence；生成 crRNA 需要确认方向和互补规则。
- HEK in situ A/N epigenetic feature calls 需与 HT standardized features 分开解释。
- 正式模型中如何处理 `TTTT` PAM，需要模型方案确定后决定。
<!-- END DeepCas12a_2026 -->
