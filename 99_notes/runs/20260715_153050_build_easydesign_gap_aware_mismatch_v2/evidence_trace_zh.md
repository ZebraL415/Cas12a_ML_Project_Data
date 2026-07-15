# EasyDesign v2 证据链

## 决策 1：未找到作者公开的训练预处理脚本

**确认事实**

- 检查了官方仓库 `https://github.com/scRNA-Compt/EasyDesign` 的 main、dev 和可见提交历史；记录的 HEAD 为 `5c06a30d0a43be28a958831587f6ab706c2d4876`。
- 对仓库文件和历史搜索 `target_at_guide`、`guide_target_hamming_dist`，没有命中生成这些字段的脚本。
- 提交 `b6420fc` 只加入了四个 xlsx 数据文件；论文 Data Availability 只指向同一仓库和 README。

**判断**

在已检查的公开分支和历史中，未找到生成这两个字段的作者训练预处理代码。该结论不等于证明作者从未编写过未公开代码。

## 决策 2：`-` 是五状态编码中的对齐占位符

**确认事实**

- 原论文 one-hot encoding 方法明确说明：发生 insertion/deletion 时，在 target DNA 或 crRNA 中使用 `-`，与 A/C/T/G 一起构成五种状态；target 和 guide 在每个位点拼接成 10 维向量。
- 官方 `easyDesign/utils/predict_activity.py` 设置第五个 one-hot 索引 `onehot_idx['-'] = 4`，并用 `ACT-ACTG` 举例说明插入/缺失处理。

**判断**

`-` 可确认是统一的 alignment-gap 符号。仅凭 `target_at_guide` 中出现 `-`，不能确认生物学事件是 target deletion、guide deletion，还是相对另一通道的 insertion。因此 v2 使用表示层名称 `gap_in_target`，不把它改写为生物学 deletion 标签。

**剩余不确定性**

公开 predictor 代码的 `onehot_idx` 包含 `-`，但 `onehot()` 首先查询的 `FASTA_CODES` 不含 `-`；按静态代码路径直接传入 `-` 会发生不一致。不能用这份运行时代码替代缺失的训练预处理实现。

## 决策 3：Table S2 支持 22 x 9 模板结构

**确认事实**

- 论文方法说明有 22 条 original template，每条对应 8 条变体：6 条 substitution、1 条 deletion、1 条 insertion，共 198 条。
- Table S2 按连续九行分组后得到 22 组；组内第 1-7 行长度相同，第 8 行均更长，第 9 行均更短，所有 198 行通过结构 QC。

**判断**

可把组内第 1 行标为 original reference，第 2-7 行标为 substitution templates，第 8 行标为 insertion template，第 9 行标为 deletion template。该角色来自论文顺序和长度模式，不代表 Table S3 每行已有作者提供的 Template No. 主键。

## 决策 4：公开材料没有逐行 plate/template/replicate 对应表

**确认事实**

- 论文说明每个 96-well plate 有两个无模板阴性孔和两个高荧光阳性重复孔，并用这些孔归一化。
- 论文、补充 workbook 和官方仓库中未找到逐行 plate ID、well、template ID、replicate 或 crRNA-template pairing 表。

**判断**

v2 不生成虚构 plate/replicate 元数据。`replicate_index_within_aligned_pair` 只表示 Table S3 中相同 guide-target 对出现的顺序，不是实验板 replicate ID。

## 决策 5：Table S2 来源映射只采用可复核序列证据

**方法证据**

- 对每条 Table S3 `target_at_guide` 保留 25 位对齐，同时生成仅用于搜索的 `target_ungapped`。
- 在 198 条 Table S2 模板中同时搜索正向和反向互补窗口；保留全部位置和模板命中。
- 先做 A/C/G/T 精确匹配；无精确命中时才做 IUPAC 兼容匹配，不使用任意 mismatch 阈值或“第一个命中”。

**结果**

- 10,633/10,634 条有候选：7,421 unique exact、3,146 single-group ambiguous、50 multi-group ambiguous、16 IUPAC-compatible、1 unmapped。
- 未映射记录为 `EasyDesign_2024_TableS3_09121`。

**判断**

mapping 适合来源审计和分组敏感性分析，不是标签，也不是默认模型输入。

## 决策 6：v2 的默认训练入口先限于无 gap Table S3

**确认事实**

- Table S3 有 9,894 条无 gap 和 740 条含 gap 记录。
- 无 gap 行的新旧 mismatch 计算 9,894/9,894 一致；gap 行仅 33/740 一致。
- v2 与 v0 的标签、source table 和 split 逐行一致；pair-level split 泄漏为 0。

**判断**

第一次 baseline 使用 9,894 条 `eligible_core_v2`。740 条 `conditional_gap_aware_v2` 只在模型显式支持 gap 通道时作为第二阶段扩展。

## 主要证据来源

- 论文：`https://onlinelibrary.wiley.com/doi/10.1002/imt2.214`
- 官方仓库：`https://github.com/scRNA-Compt/EasyDesign`
- combined workbook：`01_raw/EasyDesign_2024/data/imt2214-sup-0002-tables1-9sourcedata (1).xlsx`
- 官方代码本地镜像：`01_raw/EasyDesign_2024/easyDesign/utils/predict_activity.py`
