# 待解决问题 DeepCas12a_2026

## 已确认

- DeepCas12a 属于 `editing_activity`，不是 `diagnostic_activity`。
- `label` 是二分类 AsCas12a on-target activity 标签，不能当作 fluorescence/RFU。
- 34 bp `sequence` 是 target-context sequence，包含 upstream context、PAM、protospacer 和 downstream context。
- HT 数据的 methylation/DNase 特征是仓库说明中的标准化模型输入，不应解释为真实整合位点的 epigenetic 状态。

## 仍需确认

- 当前仓库只提供 model-ready binary labels；若后续需要连续 indel frequency，需要追溯 Kim et al. 原始数值。
- 34 bp target-context sequence 可推断 PAM/protospacer，但没有独立 crRNA sequence；若要生成 crRNA 序列需要确认方向和互补规则。
- HEK in situ 数据的 A/N epigenetic feature calls 需要在后续模型解释中与 HT standardized features 分开讨论。
