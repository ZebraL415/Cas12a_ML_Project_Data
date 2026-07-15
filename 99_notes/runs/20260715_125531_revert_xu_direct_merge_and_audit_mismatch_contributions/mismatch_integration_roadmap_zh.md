# EasyDesign 错配数据综合处理路线

## 1. 目标和边界

目标是生成可追溯、保留 indel 对齐、坐标统一并通过来源校验的 EasyDesign mismatch v2。v2 作为新的候选表与 v0 并存，不覆盖 v0，不修改 `01_raw/`，不训练模型，也不与 DeepCas12a `editing_activity` 标签合并。

## 2. 推荐目录和产物

### 贡献原件

- Xu 原脚本恢复到 `scripts/contributions/xu/`，只作为贡献快照，不直接生成默认训练表。
- 林原脚本保存到 `scripts/contributions/lin/`，保留 SHA-256、原始说明和已知问题。
- 外部输入文件先在 run manifest 中登记；写入 `01_raw/` 仍需单独授权。

### 中间层

- `02_extracted_tables/diagnostic_activity/easydesign_mismatch_mapping/`
- `EasyDesign_2024_TableS3_alignment_preserved_raw.csv`
- `EasyDesign_2024_TableS2_template_groups_raw.csv`
- `EasyDesign_2024_TableS2_TableS3_mapping_raw.csv`

### 最小清洗层

- `03_cleaned_minimal/easydesign_mismatch/`
- `EasyDesign_2024_guide_target_alignment_v2.csv`
- `EasyDesign_2024_source_mapping_v1.csv`
- `EasyDesign_2024_mismatch_qc_v2.csv`

### 候选模型层

- `04_candidate_ml_dataset/diagnostic_activity_easydesign/`
- 保留 `EasyDesign_2024_diagnostic_activity_feature_table_v0.csv`
- 新建 `EasyDesign_2024_diagnostic_activity_feature_table_v2.csv`
- 新建 `feature_engineering_v2/`，保存特征词典、QC、选择清单和生成报告

## 3. 有序实施步骤

### 步骤 1：冻结来源和建立清单

- 对原始 combined workbook、Xu 输入/脚本、林输入/脚本和既有输出计算 SHA-256。
- 记录贡献者、文件来源、收到时间、原文件名、脚本入口和环境依赖。
- 任何外部结果都先标为 `contributor_supplied`，不能因文件名含 validated/final 就升级可信等级。

验收条件：每个输入能由 manifest 唯一定位，原始文件未修改。

### 步骤 2：从 combined workbook 重建保留对齐的 Table S3 基础表

- 以 combined workbook 的 Table S3 为权威输入。
- 保留 `target_at_guide` 原始 25 位表示，包括 `-`。
- 同时生成 `target_aligned_25` 和 `target_ungapped`，两者不得互相覆盖。
- 保留 `No.`、`guide_seq`、`30 min`、type1/type2 和原始 Hamming。
- 生成稳定 `record_id`、`guide_target_pair_id` 和 replicate index。
- 只清理 BOM、外围空格和明确的显示格式字符；IUPAC 字符单独标记。

验收条件：10,634 行不丢失，原始列可逐值回溯，740 条含 `-` 行仍为 25 位对齐。

### 步骤 3：定义统一的 25 位坐标和事件状态

统一使用 Table S3 direct 方向：

- positions 1-4：PAM
- positions 5-25：21 nt spacer
- 每个位置保存 `match`、`substitution`、`gap_in_target`、`gap_in_guide` 或 `unresolved`
- 分别计算 `substitution_count`、`gap_count_target`、`gap_count_guide`、`aligned_difference_count`
- 保留 `mismatch_pos_1..25`，并增加 `gap_pos_1..25`，避免用一个二元列混合替换和缺口
- `target_ungapped` 只用于组成特征，不用于恢复原始位置

验收条件：所有位置统计之和与逐行事件列表一致；不存在“位置缺失被写成普通匹配 0”。

### 步骤 4：重建 Table S2 模板组

- 按论文支持的 22 x 9 结构记录 `template_group_id`。
- 组内第一条标为 `reference_candidate`，同时记录证据为 paper + sequence consensus。
- 第 2-7 条标为 substitution-template candidates，第 8 条标为 insertion-template candidate，第 9 条标为 deletion-template candidate。
- 不根据命名直接断言事件方向；通过长度和组内对齐再次验证。
- 清理 BOM/空格，保留并标记 `R` 等 IUPAC 字符。

验收条件：22 组均为 9 条，组内长度模式和参考共识检查全部输出到 QC。

### 步骤 5：执行 Table S3 行级来源映射

- 不再执行“去重 guide x 全部模板”的无约束扫描。
- 对每个 Table S3 `record_id` 使用其原始 guide、含缺口 target 和候选模板组。
- 使用经过测试的局部/全局序列比对库和显式 scoring，不手写固定 Hamming 处理 indel。
- 同时检查正向和反向互补方向，输出 strand、起止坐标、alignment/CIGAR、替换数、gap 数和总 edit score。
- 保存全部同分最佳命中，生成 `mapping_count`、`mapping_status` 和 `mapping_confidence`。
- 不使用任意 `MAX_MISMATCH = 5` 决定真值；映射是否成立由原始 target、对齐完整性、PAM/spacer 一致性和歧义共同决定。

验收条件：每个源行都有 `unique`、`ambiguous`、`unmapped` 或 `invalid_input` 状态，不生成无标签训练行。

### 步骤 6：建立三层证据等级

- `high`：Table S3 原始 pair 有效、Table S2 唯一映射、方向和 25 位事件向量一致。
- `medium`：Table S3 pair 有效但对应多个同组/同源模板，错配向量一致。
- `review`：含 indel、IUPAC、原始 Hamming 异常、窗口并列或无法唯一确定事件方向。
- `exclude`：不属于 Table S3 实验记录、没有 label、无法回溯或输入损坏。

验收条件：训练候选行不依赖猜测；所有降级原因均为机器可筛选字段。

### 步骤 7：重算 Xu 类特征，而不是恢复旧 v1

- 从修正后的 `target_aligned_25` 生成 gap-aware pair features。
- 从 `target_ungapped`、guide、PAM 和 spacer 生成 sequence-composition features。
- 去除常量、完全重复、线性等价和由标签派生的列。
- 旧 feature importance 只用于标注 `prior_reference_rank`，不自动控制 include/exclude。
- 每个特征在词典中记录输入字段、公式、坐标方向、gap 行为、缺失值规则和是否允许默认训练。

验收条件：无缺口子集与 Xu 既有正确结果完全一致；740 条 indel 行通过人工抽样和逐行不变量检查。

### 步骤 8：构建 v2，但保持字段分层

建议 v2 由四类字段组成：

- 追溯层：`dataset_id`、`source_id`、`source_table_id`、`record_id`、`guide_target_pair_id`
- 标签层：`label_raw_name`、`label_raw_value`、`label_normalized`、`label_status`、`label_scale_group`
- 序列/对齐层：`crRNA_sequence`、`target_aligned_25`、`target_ungapped`、`pam`、`spacer`、事件计数和位置状态
- 来源/QC 层：`template_no`、`template_group_id`、`mapping_status`、`mapping_confidence`、`raw_hamming_agreement`、`alignment_qc_status`

模板 ID、group 和 mapping confidence 默认用于审计、分组和敏感性分析，不默认作为数值模型输入，以降低病原体或实验批次泄漏风险。

验收条件：v2 行数与 v0 对应来源行一致；任何新增行必须有独立 label 来源，不能来自林同学无标签候选。

### 步骤 9：制定安全的 baseline 使用方式

- 第一阶段 baseline：只使用 9,894 条无缺口 Table S3 行，验证 v2 与现有可靠子集的一致性。
- 第二阶段 baseline：加入 740 条 gap-aware 行，比较加入前后的性能和误差分层。
- 同一 `guide_target_pair_id` 的重复实验不得跨 train/validation。
- 保留现有 paper split 或 hash split，同时增加按 template group/pathogen group 的敏感性验证；在来源映射稳定前不强制替换主 split。
- 分别报告 no-gap、indel、unique mapping、ambiguous mapping 的指标。

## 4. 自动 QC 清单

- 行数、唯一主键、重复 pair 和 replicate 数。
- guide 长度、target 对齐长度、ungapped 长度和 DNA/IUPAC 字符。
- PAM 是否为 TTTN，且 PAM/spacer 切片能重建完整 guide。
- 逐位置事件总数是否等于 aligned difference count。
- 原始 Hamming、gap-aware Hamming 和 Xu 无缺口 Hamming 的一致性。
- Table S2 mapping 的命中数、并列数、方向、坐标和组内参考一致性。
- label、split、source mapping 和 sequence feature 之间是否存在泄漏字段。
- v0 与 v2 的行级 join 是否一对一，未匹配行是否有明确原因。

## 5. 停止条件

出现以下任一情况，不得发布 v2 为默认训练入口：

- 740 条含 `-` 行被删除 gap 后参与位置特征计算。
- 无标签 Table S2 扫描候选被加入实验训练行。
- 多模板命中未标记歧义。
- mismatch 坐标未说明 direct/template orientation。
- 原始 Hamming 被当作已确认真值。
- v2 覆盖 v0 或无法回溯到原始 Table S3 行。

## 6. 推荐执行顺序

1. 编写 `build_easydesign_alignment_v2.py`，只完成步骤 2-4 和 QC。
2. 编写 `map_easydesign_table_s2_sources.py`，完成步骤 5-6。
3. 人工复核全部 188 条 Hamming 异常和分层抽样 indel 行。
4. 编写 `build_easydesign_feature_table_v2.py`，完成步骤 7-8。
5. 独立验证脚本确认行级、坐标和特征不变量。
6. 审计通过后，才允许 baseline workflow 读取 v2。
