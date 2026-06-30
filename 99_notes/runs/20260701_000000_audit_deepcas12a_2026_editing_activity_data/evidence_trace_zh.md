# DeepCas12a_2026 证据链

## Decision: DeepCas12a 属于 editing_activity

Evidence:
- 论文标题和摘要描述 AsCas12a efficiency prediction。
- 方法部分说明数据来自 AsCas12a on-target cleavage/editing efficiency。
- GitHub README 将任务描述为 AsCas12a on-target guide efficiency prediction。

Reasoning:
该数据描述的是 Cas12a 编辑/切割效率，不是 CRISPR diagnostics 荧光检测读数。

Remaining uncertainty:
无；path_type 使用 `editing_activity`。

## Decision: `label` 是二分类 editing activity label

Evidence:
- `Dataset/README.md` 说明 label 为 binary，`0` low activity，`1` high activity。
- `Data_Descriptions.txt` 说明 `1` 表示 high activity，`0` 表示 low activity。
- 论文方法部分说明二分类标签基于 background-corrected indel frequencies 的阈值。

Reasoning:
该列可以作为 primary binary classification label，但不能解释为连续 indel frequency，也不能解释为 fluorescence/RFU。

Remaining uncertainty:
原始连续 indel frequency 未包含在当前 model-ready 仓库中。

## Decision: 34 bp sequence 是 target-context sequence

Evidence:
- README 和 Dataset 说明均定义 sequence 为 4 bp upstream context + PAM + 23 bp protospacer + 3 bp downstream context。
- 论文方法部分说明 target sequences 为 34 bp。

Reasoning:
可以从 positions 5-8 推断 PAM，从 positions 9-31 推断 protospacer；但没有独立 crRNA sequence 列。

Remaining uncertainty:
如果后续需要 crRNA 序列，需明确方向和互补关系后再派生。
