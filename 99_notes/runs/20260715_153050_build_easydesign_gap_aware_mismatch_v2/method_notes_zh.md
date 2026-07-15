# 方法记录：EasyDesign gap-aware mismatch v2

原始补充数据在只读条件下保存，未进行覆盖或重命名。使用 pandas 读取 combined supplementary workbook 的 Table S2 和 Table S3。序列清理仅移除 BOM、空白和非序列显示字符；Table S3 `target_at_guide` 中的 `-` 被保留在 25 位 `target_aligned_25` 中，同时生成仅用于组成统计和模板搜索的 `target_ungapped`。

guide 与 target 在统一 direct orientation 的 25 位坐标中逐位比较。每个位置被记录为 match、substitution、gap in target、gap in guide 或 unresolved，并分别计算 PAM（1-4 位）与 spacer（5-25 位）的事件计数。`gap_in_target` 被定义为表示层状态，不解释为已确认的生物学 deletion。原始 Hamming 值被保留用于审计，但不作为默认模型输入。

Table S2 模板按论文描述的 22 个原始模板及每组 8 个变体重建为 22 x 9 分组。来源映射同时搜索 `target_ungapped` 的正向和反向互补窗口，保留所有模板和位置命中。优先使用 A/C/G/T 精确匹配；仅在无精确命中时使用 IUPAC 兼容匹配。没有采用可调 mismatch 阈值，也没有以第一个命中替代并列结果。

feature table v2 以 v0 为行级骨架，保持标签、source table 和 split 不变。新增 gap-aware pair features、逐位 difference/substitution/target-gap 特征、替换类型计数，以及 guide/target/PAM/spacer 的组成特征。来源映射、QC、标签和标识字段被明确排除在默认候选输入之外。独立验证脚本检查行数、主键、对齐长度、事件计数、标签与 split 保真、pair-level split 泄漏和 feature dictionary 唯一性。

默认 baseline 限于无 gap Table S3 记录。gap 记录作为条件扩展，Table S5 作为尺度未确认的外部测试候选。整个流程未执行模型训练。
