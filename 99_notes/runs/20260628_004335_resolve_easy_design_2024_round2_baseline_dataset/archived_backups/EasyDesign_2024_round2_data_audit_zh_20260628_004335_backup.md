# EasyDesign_2024 第二轮数据审计

## 范围
本轮只处理 `EasyDesign_2024`。`01_raw` 未被修改；没有训练模型；没有合并不同 label system。

## PDF 证据
| 证据源 | 页码 | 结论 |
| --- | --- | --- |
| /Users/linzibo/Downloads/iMeta - 2024 - Huang - Deep learning enhancing guide RNA design for CRISPR Cas12a‐based diagnostics.pdf | 1 | 论文报告共有 11,496 个经实验验证的 Cas12a 检测案例。 |
| /Users/linzibo/Downloads/iMeta - 2024 - Huang - Deep learning enhancing guide RNA design for CRISPR Cas12a‐based diagnostics.pdf |  | 方法部分说明选择 30 分钟荧光值作为活性评估指标。 |
| /Users/linzibo/Downloads/iMeta - 2024 - Huang - Deep learning enhancing guide RNA design for CRISPR Cas12a‐based diagnostics.pdf |  | 论文说明使用同板阴性对照和阳性对照对读板数值进行归一化。 |
| /Users/linzibo/Downloads/iMeta - 2024 - Huang - Deep learning enhancing guide RNA design for CRISPR Cas12a‐based diagnostics.pdf | 10 | 数据增强对每个配对使用两个标签值：30 分钟荧光值，以及由 20 分钟读数归一到 30 分钟的值。 |
| /Users/linzibo/Downloads/iMeta - 2024 - Huang - Deep learning enhancing guide RNA design for CRISPR Cas12a‐based diagnostics.pdf | 6 | 论文描述增强数据集包含 31,993 个 guide-to-target 配对。 |
| /Users/linzibo/Downloads/iMeta - 2024 - Huang - Deep learning enhancing guide RNA design for CRISPR Cas12a‐based diagnostics.pdf |  | 方法部分描述训练集包含 10,634 个配对，测试集包含 1,358 个配对。 |
| /Users/linzibo/Downloads/iMeta - 2024 - Huang - Deep learning enhancing guide RNA design for CRISPR Cas12a‐based diagnostics.pdf |  | 方法部分描述提取 PAM 下游 21 nt，并在两端各扩展 10 nt，形成 45 nt target context。 |
| /Users/linzibo/Downloads/iMeta - 2024 - Huang - Deep learning enhancing guide RNA design for CRISPR Cas12a‐based diagnostics.pdf | 3 | 论文讨论了 Cas12a guide-target 配对中的 TTTN PAM。 |
| /Users/linzibo/Downloads/iMeta - 2024 - Huang - Deep learning enhancing guide RNA design for CRISPR Cas12a‐based diagnostics.pdf | 15 | 补充资料列表说明 Table S3-S5 是基于 CRISPR fluorescence reaction 的模型开发数据集。 |

## 截图/补充资料证据
| 证据源 | 表格 | 结论 |
| --- | --- | --- |
| /var/folders/c9/xvbkv1hs5kz09g_fbjx8txd40000gn/T/codex-clipboard-e3e49006-b253-48c9-80e1-98d4742dde7b.png | Table S1 | 用于构建 crRNA 文库的病毒和细菌物种类型信息。 |
| /var/folders/c9/xvbkv1hs5kz09g_fbjx8txd40000gn/T/codex-clipboard-e3e49006-b253-48c9-80e1-98d4742dde7b.png | Table S2 | 用于构建 crRNA 文库的病毒和细菌核酸模板信息。 |
| /var/folders/c9/xvbkv1hs5kz09g_fbjx8txd40000gn/T/codex-clipboard-e3e49006-b253-48c9-80e1-98d4742dde7b.png | Table S3 | 基于 CRISPR 荧光反应生成的模型开发训练数据集。 |
| /var/folders/c9/xvbkv1hs5kz09g_fbjx8txd40000gn/T/codex-clipboard-e3e49006-b253-48c9-80e1-98d4742dde7b.png | Table S4 | 基于 CRISPR 荧光反应生成的模型开发增强数据集。 |
| /var/folders/c9/xvbkv1hs5kz09g_fbjx8txd40000gn/T/codex-clipboard-e3e49006-b253-48c9-80e1-98d4742dde7b.png | Table S5 | 基于 CRISPR 荧光反应生成的模型开发测试数据集。 |
| /var/folders/c9/xvbkv1hs5kz09g_fbjx8txd40000gn/T/codex-clipboard-e3e49006-b253-48c9-80e1-98d4742dde7b.png | Table S6 | k-fold 交叉验证的模型性能评估。 |
| /var/folders/c9/xvbkv1hs5kz09g_fbjx8txd40000gn/T/codex-clipboard-e3e49006-b253-48c9-80e1-98d4742dde7b.png | Table S7 | 四种病原体的 DNA 模板，用于实验活性测试。 |
| /var/folders/c9/xvbkv1hs5kz09g_fbjx8txd40000gn/T/codex-clipboard-e3e49006-b253-48c9-80e1-98d4742dde7b.png | Table S8 | 四种病原体的 crRNAs，用于实验活性测试。 |
| /var/folders/c9/xvbkv1hs5kz09g_fbjx8txd40000gn/T/codex-clipboard-e3e49006-b253-48c9-80e1-98d4742dde7b.png | Table S9 | 由 EasyDesign 一站式网页平台生成的最优 HPV crRNAs 和 RPA primers。 |

## 已解决问题
- `30 min`：PDF 方法部分确认 30 分钟荧光值被选为活性指标；本轮作为 Table S3 内部 baseline 的主标签。
- `20 min normalized`：PDF 确认它是 20 分钟读数归一到 30 分钟的派生/增强标签；不并入主标签。
- `out_logk_measurement`：对应 Table S4 增强数据；本轮单独保存为 optional augmentation，不进入默认 baseline。
- `true value`：对应 Table S5 测试集实验真值；保留为 external paper test，但与 Table S3 数值尺度仍需确认。
- standalone workbook 与 combined source-data workbook：以 combined workbook 为权威来源，standalone 表视为重复来源。
- figure source data：保留为证据或 metadata，不直接作为 tidy crRNA-target 训练行。
- `guide-expected-activities` 和模型列：全部归为 predicted score，不是 primary training label。
- PAM：PDF 支持 TTTN PAM；Excel 无独立 PAM 列，本轮只从序列 5' 端 TTTN 前缀推断并标记为 inferred。
- Fig.S3：属于特征/活性相关的聚合图源数据，不作为逐条训练标签。

## 仍需解决的问题
- Table S3 的负值 `30 min` 标签与 Table S5 的正值 `true value` 是否可通过已知转换映射到同一尺度，仍需人工确认或方法学决定。
- Table S3 原始 `guide_target_hamming_dist` 与从 `guide_seq`/`target_at_guide` 直接计算的 mismatch 并不总一致；该原始列的真实语义仍需确认。
- Excel 中没有明确独立 PAM 列；当前 PAM 仅根据 TTTN 前缀推断，后续若要作为模型特征需要确认序列定义。
- Table S4 增强数据是否进入首个正式训练流程，需要在模型方案确定后决定。
- Table S3 只有 type1/type2，不含具体 pathogen 名称；如果要做物种分组验证，需要额外映射。

## 第二轮数据整理结论
- Table S3 作为主 baseline 内部分割来源：baseline_train=8417，baseline_validation=2217。
- Table S5 保留为 external paper test：1358 行，但标记为 scale_unconfirmed。
- Table S4 作为 optional augmentation：31993 行，不进入默认 baseline。
