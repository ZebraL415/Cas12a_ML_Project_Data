# EasyDesign 工程特征数据审计

## 已确认事实

- 输入 v0 表含 11,992 行、28 列，`record_id` 无重复，DNA 字母检查通过。
- 主 baseline 为 Table S3 的 10,634 行：训练 8,417 行，验证 2,217 行；Table S5 的 1,358 行仍为 `external_test_scale_unconfirmed`。
- 徐同学脚本原样复跑成功，生成 139 个工程特征；完整输出含 11,992 行、155 列，record 顺序与 v0 完全一致。
- `direct` 模式与 `guide_target_hamming_dist_computed` 在 10,634 条主 baseline 行上 100% 一致；与 `guide_target_hamming_dist_raw` 的精确一致率为 91.593%，相关性较低。
- 长度、crRNA GC 和计算 Hamming 可被新脚本精确复算；target GC 的最大差为 `4.35e-7`，来自 v0 六位小数舍入。
- Table S3 中 740 行 target 短于 crRNA，其中训练 585 行、验证 155 行。原脚本把未对齐位置填为 `0`；v1 将 827 个未对齐位置单元改为空值。
- 徐同学首轮 `top30` 文件实际只有 5 个特征行。
- 参考改进预测含 2,217 行，全部属于现有 `baseline_validation`；record ID、序列和标签逐行完全匹配。
- 参考指标可从预测文件重算：Spearman 0.765651、Pearson 0.747238、MAE 0.327815、RMSE 0.424830、R2 0.554858。

## 初步判断

- 参考改进结果支持错配数量、错配比例、位置、错配类型和局部序列组成具有建模价值。
- 重要性排序受重复特征影响：工程错配数与现有计算 Hamming 完全相同，match fraction 与 mismatch fraction 互为补数，若同时使用会降低解释稳定性。
- `direct` 的计算一致性足以支持可复算特征生成，但不足以确认 PAM proximal、seed 或 distal 的生物学方向。

## 排除项

- `/Users/linzibo/Documents/mismatch_wide_table.xlsx` 曾作为未明确的第三文件候选进行扫描，但其 6,506 行、30 列结构与 EasyDesign v0/生成器输出不匹配，因此未纳入本轮项目文件。
- 未修改 `01_raw/`，未混合 Table S4、Table S5 和 Table S3 的标签尺度，未训练模型。
