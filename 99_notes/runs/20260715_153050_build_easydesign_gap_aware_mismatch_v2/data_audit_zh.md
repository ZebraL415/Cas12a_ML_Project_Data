# EasyDesign gap-aware v2 数据审计

## 范围

本轮只处理 EasyDesign_2024 `diagnostic_activity`。读取原论文、官方仓库、combined supplementary workbook、现有 v0 和既有审计记录；未修改 `01_raw/`，未训练模型，未合并其他 label system。

## 确认事实

- combined workbook Table S2 有 198 条模板，可组成 22 个九条模板组。
- Table S3 有 10,634 条实验测量记录，`30 min` 标签无缺失。
- 所有 guide 和 `target_at_guide` 对齐表示均为 25 位。
- 9,894 条 target 不含 `-`；740 条含 `-`，ungapped 长度为 17、18、23 或 24。
- 740 条 gap 记录在对齐表示中均为 target 通道 gap，未观察到 guide 通道 `-`。
- 原始 `guide_target_hamming_dist` 与 25 位对齐差异计数在 10,446 行一致、188 行不一致。
- 公开仓库中的 `predict_activity.py` 与本地 raw 镜像 SHA-256 一致。

## 初步推断

- Table S2 的组内第 8/9 条可分别按论文顺序和长度模式解释为 insertion/deletion template；这是结构推断，不是 Table S3 行级实验 ID。
- 10,633 条 Table S3 记录的精确/IUPAC 兼容窗口可用于来源候选映射；多模板或多组命中不能自动升级为唯一真值。
- raw Hamming 的 188 条异常说明该字段不能作为默认训练特征；其含义可能包含未公开预处理逻辑，但当前证据不足。

## 数据质量分层

- `eligible_core_v2`：9,894 条无 gap Table S3 行。
- `conditional_gap_aware_v2`：740 条保留 gap 的 Table S3 行。
- `external_test_only_scale_unconfirmed`：1,358 条 Table S5 行。
- mapping high/medium/review：7,421 / 3,146 / 67。
- 唯一无法由精确或 IUPAC 兼容窗口映射的记录：`EasyDesign_2024_TableS3_09121`。

## 最值得后续复核的记录

- 188 条 raw Hamming 不一致记录。
- 67 条 mapping review 记录，其中包括 50 条多组命中、16 条 IUPAC 兼容和 1 条未映射。
- 740 条 gap 记录，尤其 ungapped 长度 17/18 的 6 条多 gap 记录。
- Table S5 非 45 nt context 和 Table S3/Table S5 标签尺度问题。
