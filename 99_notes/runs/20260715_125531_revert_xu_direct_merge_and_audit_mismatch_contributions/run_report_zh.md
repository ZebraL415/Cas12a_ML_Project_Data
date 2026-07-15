# 运行报告

## Scope

本轮处理 EasyDesign 错配相关贡献，完成 Xu 直接合并回退、林脚本独立复现、两套结果交叉核验和后续综合处理方案设计。

## Inputs Scanned

- Git 提交 `fa8d67b Integrate Xu engineered features` 及其父提交 `6a6535a`。
- 原始合并补充工作簿 `01_raw/EasyDesign_2024/data/imt2214-sup-0002-tables1-9sourcedata (1).xlsx` 的 Table S2、Table S3、Table S4 和 Table S5。
- EasyDesign 原论文 `/Users/linzibo/Downloads/iMeta - 2024 - Huang - Deep learning enhancing guide RNA design for CRISPR Cas12a‐based diagnostics.pdf`。
- 林同学目录 `/Users/linzibo/Downloads/EasyDesign_S2_scanning/` 中的两份 Python 脚本和两份 Excel 输入。
- 林同学既有输出 `/Users/linzibo/Documents/mismatch_wide_table.xlsx`。
- Xu 原脚本和整合产物，来源于 Git 提交 `fa8d67b`。
- 当前 v0 候选表和现行 EasyDesign 使用说明。

## Actions

- 确认回退前 Git 工作区干净，最新提交仅为 Xu 整合提交。
- 执行非破坏性 `git revert fa8d67b`，生成提交 `653fb6f`。
- 确认回退后文件树与 `6a6535a` 完全一致。
- 在 `/private/tmp/easydesign_s2_lins_repro/` 复跑林同学两份脚本，没有写回原目录。
- 独立比较 Table S2、Table S3、林输出和此前 Xu/v1 特征。
- 回查论文第 10-11 页，核对 22 x 9 模板结构、TTTN PAM、21 nt spacer 和 `-` indel 编码。
- 生成中英双语审查和整合路线文档。
- 更新 `99_notes/current/problems_to_resolve_zh.md` 和英文对应文件。

## Confirmed Results

- 回退可行且已完成；旧整合仍保留在 Git 历史中。
- 林输入与原始 Table S2/Table S3 对应关系成立，输出可逐单元格复现。
- 林输出 6,506 行中，5,078 行可回连 Table S3，代表 3,404 个唯一无缺口 pair 和 4,457 条实验行。
- 可回连部分与 Xu direct mismatch count 及反向换算后的 21 位位置向量均为 100% 一致。
- 1,428 条林输出不是 Table S3 实验记录，没有 fluorescence label。
- Table S3 有 740 条含 `-` 的 25 位对齐；现有 Xu 流程删除 gap 后不能正确解释位置特征。
- 原始 Hamming 与保留 gap 的 25 位直接计数一致率为 98.232%，188 行、28 个唯一 pair 不一致。
- 林来源扫描为其中 10 个异常 pair、90 行提供支持 direct count 的证据，但不能解决全部异常。

## Data Quality Issues

- Xu 现有 indel 特征存在 gap 删除和坐标平移。
- 林脚本丢失原始行号、target、label 和 replicate，产生无标签组合。
- 林固定 Hamming 和任意阈值 5 不处理 indel，也不报告全部并列命中。
- Table S2 有 BOM、空格和 IUPAC `R`；4 条林输出受规范化影响。
- 项目 standalone `Table S2.xlsx`/`Table S3.xlsx` 文件名与实际内容不一致，需要 catalog 内容说明，不修改 raw 文件。

## Outputs Generated

- `99_notes/runs/20260715_125531_revert_xu_direct_merge_and_audit_mismatch_contributions/README.md`
- `99_notes/runs/20260715_125531_revert_xu_direct_merge_and_audit_mismatch_contributions/README_en.md`
- `mismatch_contribution_review_zh.md` / `mismatch_contribution_review_en.md`
- `mismatch_integration_roadmap_zh.md` / `mismatch_integration_roadmap_en.md`
- `run_report_zh.md` / `run_report_en.md`
- 更新后的 current problems 双语文件

## Evidence Boundary

### 从文件确认的事实

行数、列数、序列内容、gap 数、输出复现、Git tree 一致性和数值一致率均来自程序化比较。模板 22 x 9 结构、TTTN/21 nt 边界和 `-` 编码来自论文方法部分，并由工作簿结构支持。

### 初步推断

原始 Hamming 很可能主要表示作者的 gap-preserving aligned distance，但 188 行异常意味着不能把该语义视为全部确认。多模板命中的具体生物来源也不能仅凭序列相同确定。

## Next Recommended Actions

按 `mismatch_integration_roadmap_zh.md` 依次构建 alignment v2、Table S2 row-level source mapping 和 feature table v2。审计通过前，默认入口保持 v0，740 条 indel 记录不使用现有位置错配特征。
