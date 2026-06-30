# DeepCas12a_2026 方法记录

原始 GitHub 仓库文件保持不变。模型就绪 TXT 数据使用 pandas 以空白分隔格式读取，并添加显式列名 `sequence`、`methylation_status`、`dnase_signal_status` 和 `label`。论文 PDF、仓库 README、Dataset 说明和 split 说明被用于校对字段含义与标签来源。DeepCas12a 被归入 `editing_activity` 路径，`label` 被保留为由 measured indel activity 阈值化得到的二分类 AsCas12a on-target activity 标签。34 bp `sequence` 被拆分为 4 bp upstream context、PAM、23 bp protospacer 和 3 bp downstream context，并计算基础序列和 epigenetic 特征。没有训练模型，也没有把该数据与 diagnostic activity 数据合并。
