# Run Report

## Scope

整合徐同学的 EasyDesign 工程特征脚本和首轮重要性结果，审计指定的改进结果，构建并说明 EasyDesign diagnostic activity 特征表 v1。

## Inputs Scanned

- `EasyDesign_2024_diagnostic_activity_feature_table_v0.csv`
- `/Users/linzibo/Documents/generate_validated_engineered_features.py`
- `/Users/linzibo/Documents/first_run_feature_importance_top30.csv`
- `/Users/linzibo/Desktop/MLRS/improved_feature_outputs/` 下 6 个结果文件
- `/Users/linzibo/Documents/mismatch_wide_table.xlsx`：仅作为未明确第三文件候选检查，确认不属于本流程后跳过

## Outputs Generated

- 推荐数据：`EasyDesign_2024_diagnostic_activity_feature_table_v1.csv`
- 完整特征与 QC：`feature_engineering/`
- 组员及参考结果：`evaluation/`
- 可复现脚本：`scripts/build_easydesign_feature_table_v1.py`、`scripts/verify_easydesign_feature_results.py`
- 贡献原件：`scripts/contributions/xu/generate_validated_engineered_features.py`
- 本运行目录中的双语审计、证据、方法、筛选和报告文件

## Classification Decisions

- 全部新表继续归为 `diagnostic_activity`；标签仍是 Table S3 实验 30 分钟活性。
- 特征重要性、预测值和指标归为 evaluation artifact，不是 label。
- Table S4 augmentation 和 Table S5 scale-unconfirmed 数据状态不变。

## Data Quality Checks

- v1：11,992 行、89 列、`record_id` 无重复、split 计数与 v0 一致。
- 60 个新工程特征；827 个未对齐位置单元改为空值。
- 计算 Hamming 复算一致率 100%；无 label 或 split 变化。
- 参考预测的 2,217 个 record 全部属于验证集，指标差异小于 `3.1e-9`；residual 最大舍入差 `1.19e-7`。

## Evidence Boundary

确认事实来自文件结构、列值、脚本运行和逐行复算。关于特征生物学区域、训练过程和性能提升原因的判断仍是初步推断，因为缺少独立方向证据和改进模型训练代码。

## Next Recommended Actions

- 用同一 split 分别运行 v0 五特征控制组和 v1 工程特征组，并保存完整训练配置。
- 修复参考流程中的重复特征后重新评估重要性稳定性。
- 人工确认 740 条短 target 的来源约定，以及 guide/target/PAM 的生物学方向。
- 在尺度转换确认前，不使用 Table S5 报告外部测试性能。
