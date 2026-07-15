# EasyDesign 错配处理贡献审查

## 1. 审查目的

本审查比较 Xu 同学和林同学对 EasyDesign guide-target 错配信息的处理，区分可复现事实、相互印证结果、仍需确认的推断和不得进入默认训练表的结果。错配特征是输入或注释，不是 fluorescence/RFU 活性标签。

## 2. 核验对象

### Xu 同学

- 原始贡献：`generate_validated_engineered_features.py` 和首轮 feature importance。
- 曾合并于 Git 提交：`fa8d67b Integrate Xu engineered features`。
- 主要处理：对清洗后的 `crRNA_sequence` 与 `target_sequence` 比较 direct/complement/reverse/reverse-complement 方向，选择与项目 `guide_target_hamming_dist_computed` 最一致的方向，再生成 Hamming、位置、错配类型和序列组成特征。

### 林同学

- 目录：`/Users/linzibo/Downloads/EasyDesign_S2_scanning/`。
- 输入：`guide_seq.xlsx`、`Table_S2.xlsx`。
- 脚本：`filter_templates_crrna.py`、`integrated_snv_analysis.py`。
- 已发现输出：`/Users/linzibo/Documents/mismatch_wide_table.xlsx`。
- 主要处理：去重 Table S3 guide，去除 5' TTTN，反向互补 21 nt spacer，在 198 条 Table S2 长模板中滑窗寻找不超过 5 个差异的最佳窗口。

## 3. 已确认事实

- 林同学 `guide_seq.xlsx` 的 10,634 行 `No.` 和 `guide_seq` 与原始 Table S3 逐行一致，去重后为 1,357 条 guide。
- 林同学 `Table_S2.xlsx` 的 198 条记录与原始合并补充工作簿 Table S2 一致。
- 原论文确认 Table S2 由 22 个原始模板组成，每个原始模板对应 6 个替换模板、1 个插入模板和 1 个缺失模板，共 22 x 9 = 198 条。
- Table S2 每组前 7 条等长，第 8 条更长，第 9 条更短；22 组第一条均等于前 7 条的多数共识，因此“每 9 条一组、第一条为参考模板”得到论文与数据结构共同支持。
- Table S3 全部 guide 为 25 nt 且以 TTTN 开头。原论文定义 PAM 下游 21 个位置，因此将 positions 1-4 作为 PAM、positions 5-25 作为 spacer 有依据。
- Table S3 有 740 行 `target_at_guide` 含 `-`。原论文明确使用 `-` 作为插入/缺失的第五种编码字符。
- 林同学脚本可完整复现：`mismatch_wide_table.xlsx` 为 6,506 行、30 列，临时复跑结果与既有文件逐单元格一致。

## 4. 相互印证且值得采用的内容

### 4.1 无缺口 guide-target 的直接方向

林同学输出中有 5,078 条 template-guide 映射可重建为 Table S3 中真实存在的无缺口 guide-target pair，对应 3,404 个唯一 pair 和 Table S3 的 4,457 条实验行。

在这部分数据中：

- 林同学 `No_mismatch` 与 Xu/项目 direct Hamming 的一致率为 100%。
- 林同学 21 个 spacer 位置经坐标反转后，与 Xu 的位置向量一致率为 100%。
- 坐标关系为 `Lin pos_i = Xu mismatch_pos_(26-i)`；林同学没有表示 Xu positions 1-4 的 PAM 区域。

这为无缺口子集的 direct 方向和错配计算提供了独立 Table S2 来源证据。该证据可用于确认计算方向，但不能把两套同义特征重复加入模型。

### 4.2 PAM 与 spacer 边界

Xu 使用完整 25 nt guide-target 表示，林同学使用 21 nt 反向互补 spacer。结合全部序列的 TTTN 前缀和论文方法，可确认项目应显式区分：

- `pam_aligned = positions 1-4`
- `spacer_aligned = positions 5-25`
- `template_window` 为相反链方向时必须保存方向和坐标映射

### 4.3 序列组成特征

Xu 脚本中的长度、GC、碱基比例、entropy、homopolymer 和 k-mer 计算在输入为明确 A/C/G/T 序列时原理成立，并且可复现。它们可以在修正后的序列层重新计算，但应去除常量、重复和线性等价特征，并避免依据一次 feature importance 自动选择最终特征。

### 4.4 对原始 Hamming 异常的进一步认识

Table S3 原始 `guide_target_hamming_dist` 与保留 `-` 的 25 位字符对齐直接计数一致率为 98.232%。共有 188 行、28 个唯一 pair 不一致。

林同学来源扫描覆盖其中 10 个异常 pair、90 行；这些模板证据支持直接序列计数 0 或 1，而不支持原始列中的 1-10。因此原始列很可能主要表示作者的对齐距离，但包含异常值或混合处理，仍不得作为默认训练特征。

## 5. Xu 处理的局限和不当之处

### 5.1 indel 对齐在上游被破坏

现有 v0 清洗把 Table S3 `target_at_guide` 中的 `-` 删除，使 740 条 target 缩短为 17、18、23 或 24 nt。Xu 脚本随后左对齐短序列并增加长度差惩罚。第一个缺口之后的碱基位置发生平移，因此这些行的 mismatch position、mismatch type、连续匹配区段和区域错配特征不能按原始生物学位置解释。

### 5.2 方向验证不是独立生物学验证

Xu 选择 direct，是因为它与项目使用同一清洗序列计算的 `guide_target_hamming_dist_computed` 完全一致。这证明代码内部一致，但参考列与待验证结果共享输入和定义，不构成独立来源验证。林同学对 3,404 个无缺口唯一 pair 的 Table S2 回连才提供了部分外部支持。

### 5.3 缺失位置被编码为普通值

Xu 完整生成器对超出对齐长度的位置写 0，会把“该位置不存在”混同为“存在且匹配”。即使后续 v1 构建曾改为空值，缺口后的坐标平移问题仍未解决。

### 5.4 feature importance 证据边界

首轮 feature importance 和参考 improved outputs 缺少完整训练代码、模型参数、依赖锁定、随机种子和可复现 split 证明。它们只能作为候选特征线索，不能证明特征具有稳定因果或跨模型价值。

### 5.5 直接合并过早

在 740 条 indel 记录和原始 Hamming 语义未解决时，将 Xu 特征直接并入默认 v1 会把已知对齐问题包装成模型就绪数据。本轮已用 Git revert 撤销该默认合并。

## 6. 林处理的局限和不当之处

### 6.1 丢失实验记录主键和标签

脚本只保留并去重 guide，丢弃 Table S3 `No.`、`target_at_guide`、`30 min`、重复实验和原始 split。随后执行 1,357 x 198 的候选扫描，因此输出不是 Table S3 的逐行校验表。

### 6.2 产生无标签的附加组合

6,506 条输出中只有 5,078 条能回连 Table S3 pair，剩余 1,428 条不是原始实验记录。所有 3-5 mismatch 输出均位于这部分。它们没有 fluorescence 标签，不得进入 diagnostic activity 训练集。

### 6.3 固定 Hamming 不能处理 indel

脚本把 spacer 固定为 21 nt，并用等长滑窗 Hamming。它没有读取或保留 Table S3 的 `-` 对齐，因此没有解决最需要修复的 740 条 indel 记录。

### 6.4 阈值和命名缺乏依据

`MAX_MISMATCH = 5` 没有论文、README 或数据分布依据。脚本名中的 `snv` 也不准确，因为结果包含 0-5 个差异且没有限制为单碱基变异。

### 6.5 最优窗口和模板歧义未报告

3,404 个可回连唯一 pair 中，2,762 个只对应一个模板，642 个对应多个模板，最多为 9 个。脚本只保留最早最优窗口，遇到 0 mismatch 提前停止，没有保存全部并列命中或 ambiguity status。

### 6.6 输入字符未规范处理

Table S2 有 17 行包含 BOM、空格或 `R`。脚本只做大写转换；规范处理后有 4 条输出的最佳窗口或 mismatch 数改变。BOM/空格可作为格式字符清理，`R` 必须作为 IUPAC 歧义字符标记，不能静默删除或当普通 mismatch。

### 6.7 参考模板没有进入实际计算

22 x 9 分组与第一条参考模板本身是可信的，但 `Reference_Template` 只被写入结果。脚本没有计算突变模板相对参考模板的变化，也没有利用组内同源关系约束 guide 的来源映射。

## 7. 当前采用决定

| 内容 | 状态 | 用途 |
|---|---|---|
| EasyDesign v0 实验标签、来源字段和 split | 保留 | 当前默认候选数据 |
| Xu 无缺口序列组成特征 | 重算后采用 | v2 候选输入 |
| Xu 无缺口 direct mismatch 特征 | 有条件采用 | 仅 25 nt A/C/G/T 对齐通过 QC 的行 |
| Xu 对 740 条 indel 的现有 mismatch 特征 | 暂停 | 重新保留 `-` 后生成 |
| Xu feature importance | 仅作参考 | 候选优先级，不作最终选择依据 |
| 林 22 x 9 分组和第一条参考关系 | 采用 | 来源映射元数据 |
| 林唯一且可回连 Table S3 的模板命中 | 修正后采用 | `source_mapping` 注释，不作标签 |
| 林多模板命中 | 保留并标记歧义 | 分组验证或人工复核 |
| 林 1,428 条非 Table S3 候选 | 不进入训练 | 无标签候选库或暂不处理 |
| 林当前 `pos_1..pos_21` | 不直接合并 | 转为统一 25 位 direct 坐标后再用 |
| 原始 `guide_target_hamming_dist` | 暂不采用 | 保留原值和异常标记供审计 |

## 8. 仍未解决的问题

- 188 条原始 Hamming 异常中，未被唯一 Table S2 映射解释的行仍需逐条核验或咨询作者。
- Table S3 的 `-` 在每一行究竟表示 guide 相对 target 的 deletion、target 相对 guide 的 deletion，还是作者编码层的统一 gap，需要结合模型输入代码和补充方法确认后命名。
- 多模板同序列命中应作为同源来源、技术重复还是不可区分映射，需要在构建 template-level split 前决定。
- 项目中 standalone `Table S2.xlsx` 实际包含 Training/Augment/Test，`Table S3.xlsx` 实际包含四种病原体 DNA/crRNA；原文件不修改，但 catalog 需要按内容纠正说明。
