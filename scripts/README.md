# 可复现脚本

本目录保存数据审计、提取、清洗、候选表构建和验证代码。脚本只能读取 `01_raw/`，不得修改、重命名或覆盖原始文件。

## EasyDesign

- `inspect_easy_design.py`：第一轮 workbook/sheet 审计。
- `resolve_easy_design_round2.py`：结合论文证据构建 baseline v0。
- `build_easydesign_alignment_v2.py`：保留 gap 对齐并建立 Table S2 来源映射。
- `build_easydesign_feature_table_v2.py`：构建 gap-aware feature table v2、词典和 QC。
- `verify_easydesign_v2.py`：独立验证 V2。
- `build_v2_1_context_feature_table.py`：只从 `crRNA_sequence` 和 `target_ungapped` 构建 58 个 v2.1 上下文特征，不覆盖 V2。
- `verify_v2_1_context_feature_table.py`：独立检查 v2.1 行列、父表保真、gap/标签/split 和数值范围。
- `audit_vertical3_delta_g.py`：在 ViennaRNA 2.7.2 下独立重算并核验原 Vertical3 四列。
- `build_easy_design_feature_table_v3.py`：从正式 V2.1 构建四个修正 thermodynamic proxy、V3 表、词典、块清单和 QC。

v2.1 的固定配置与完整运行记录位于 `/Users/linzibo/Cas12a_ML_Project_Expr/V2-0_unified_baseline/`；V3 Package1 的完整实验代码和结果位于 `/Users/linzibo/Cas12a_ML_Project/`。运行应写入新的时间戳目录并保存输入、配置、fold 和脚本 SHA-256。

英文版见 `README_en.md`。
