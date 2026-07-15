# Run Report

## Scope

本次处理 EasyDesign_2024 `diagnostic_activity` 的 gap-aware mismatch v2。目标是回查论文/官方仓库证据、修正 v0 删除 gap 的问题、建立可审计来源映射并准备模型无关 baseline 输入。未训练模型，未修改 `01_raw/`，未把 EasyDesign 与 DeepCas12a 合并。

## Inputs scanned

- 原论文 PDF：`/Users/linzibo/Downloads/iMeta - 2024 - Huang - Deep learning enhancing guide RNA design for CRISPR Cas12a‐based diagnostics.pdf`。
- 官方仓库：`https://github.com/scRNA-Compt/EasyDesign`，检查 main、dev 和可见历史，HEAD `5c06a30d0a43be28a958831587f6ab706c2d4876`。
- combined workbook：`01_raw/EasyDesign_2024/data/imt2214-sup-0002-tables1-9sourcedata (1).xlsx` 的 Table S2/Table S3。
- 本地官方代码镜像：`01_raw/EasyDesign_2024/README.md` 和 `easyDesign/utils/predict_activity.py`。
- 既有 v0：`04_candidate_ml_dataset/diagnostic_activity_easydesign/EasyDesign_2024_diagnostic_activity_feature_table_v0.csv`。

没有找到也没有读取作者未公开的训练预处理代码、plate layout 或逐行 template/replicate mapping。

## Outputs generated

- `02_extracted_tables/diagnostic_activity/easydesign_mismatch_mapping/`：Table S3 保留对齐原始导出、Table S2 模板组、全部 mapping hit。
- `03_cleaned_minimal/easydesign_mismatch/`：行级 alignment v2、source mapping v1、mismatch QC 队列。
- `04_candidate_ml_dataset/diagnostic_activity_easydesign/EasyDesign_2024_diagnostic_activity_feature_table_v2.csv`：11,992 x 188。
- `04_candidate_ml_dataset/diagnostic_activity_easydesign/feature_engineering_v2/`：145 行 feature dictionary 和 QC JSON。
- `scripts/build_easydesign_alignment_v2.py`、`scripts/build_easydesign_feature_table_v2.py`、`scripts/verify_easydesign_v2.py`。
- 中英文使用指南、build report、审计、证据链、方法和本运行报告。

## Classification decisions

- Table S3：`diagnostic_activity`、measured、crRNA-target pair，是主训练来源。
- Table S2：template metadata/source mapping，不是 label。
- Table S5：measured external test candidate，但与 Table S3 的 label scale 未确认。
- gap 行：保留为 `conditional_gap_aware_v2`，不进入默认首轮 baseline。

## Evidence

**从文件确认的事实**

- 论文定义 A/C/T/G/`-` 五状态 one-hot，并说明 `-` 可出现在 target 或 crRNA。
- 论文定义 22 个 original templates 和每组 8 个变体，并记录 96-well plate control 归一化方法。
- Table S3 有 10,634 行，其中 740 行 target 表示含 `-`。
- 官方公开仓库未出现 `target_at_guide` 或 `guide_target_hamming_dist` 生成脚本。

**根据结构和序列做出的初步判断**

- Table S2 连续九行可按论文顺序分组，长度模式支持第 8/9 行为 insertion/deletion template。
- 通过 exact/IUPAC-compatible window search 生成 Table S3 来源候选；这是序列证据，不是作者实验主键。

## Data quality checks

- 10,634 条 alignment 的 guide 和 aligned target 均为 25 位；740 条 gap 全部保留。
- gap ungapped 长度分布：17 nt 4 条、18 nt 2 条、23 nt 47 条、24 nt 687 条。
- 原始 Hamming 一致 10,446 条，不一致 188 条。
- source mapping 有候选 10,633 条；high 7,421、medium 3,146、review 67。
- v2 与 v0 的 11,992 条 label、source table、baseline split 全部一致。
- no-gap 新旧 mismatch 9,894/9,894 一致；gap 新旧仅 33/740 一致。
- 相同 pair 跨 train/validation 的数量为 0；独立验证 25 项全部通过。

## Unresolved questions

- 缺失作者训练预处理代码和逐行 Template No./plate/replicate 对应表。
- `-` 的对齐含义已确认，但每行的生物学 insertion/deletion 方向仍不能仅由公开字段确定。
- 公开 predictor 的 `-` one-hot 代码路径存在静态不一致。
- 188 条 raw Hamming 异常、67 条 mapping review 和记录 9121 未映射仍需人工或作者证据。
- Table S3/Table S5 label scale 和少数 Table S5 context 问题仍未解决。

## Next recommended actions

1. 先按 v2 使用指南运行 9,894 条无 gap baseline；本轮不执行训练。
2. 固定同一 feature list，对 740 条 gap 做单独加入的消融和分层评估。
3. 若获得作者预处理代码或实验对应表，重新运行 source mapping 并升级/降级 evidence tiers。
4. 对 188 条 Hamming 异常和 67 条 mapping review 进行机器列表加人工抽样复核。
