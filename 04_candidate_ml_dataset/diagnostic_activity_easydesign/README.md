# diagnostic_activity_easydesign

本目录保存 EasyDesign_2024 `diagnostic_activity` 候选数据。标签是 Cas12a diagnostics 实验荧光活性，不能与 DeepCas12a 二分类 `editing_activity` 合并。

## 版本入口

- `EasyDesign_2024_diagnostic_activity_feature_table_v2.csv`：V2 gap-aware core 父表，11,992 行 × 188 列；130 个 core 候选输入。
- `feature_engineering_v2/`：V2 特征词典与 QC。
- `feature_engineering_v2_1_context/`：不覆盖 V2 的上下文扩展，11,992 行 × 246 列；冻结清单含 188 个名义输入。
- `feature_engineering_v3_package1/`：当前 Package1 数据入口，11,992 行 × 250 列；完整继承 V2.1 并加入 4 个经核验修正的 thermodynamic proxy，共 192 个名义输入。
- `EasyDesign_2024_v2_data_usage_guide_zh.md` / `_en.md`：来源、标签、split 和 gap-aware 使用边界。

## 当前推荐工作流

复现旧基准时使用 V2 core。Package1 及后续 Horizontal 实验默认使用 `feature_engineering_v3_package1/EasyDesign_2024_feature_block_manifest_v3.csv` 定义输入，并将 P1-0 作为统一基准。Table S3 的 10,634 条记录用于开发；target-grouped CV 只在 8,417 条 `baseline_train` 上选择特征。Table S5 的 1,358 条记录只用于外部排序验证，不能进入特征选择或训练。

V3 的 `nonpositional4_candidate` 表只保留 alignment、substitution、context、thermodynamic 四块；该名称不代表四块均已证明为高影响。P1-1 证明 context、substitution 和 alignment 最有用，thermodynamic 尚未通过正式晋级阈值。

每个训练折只用训练记录拟合中位数，剩余缺失填 0，再移除该折常数列。`mapping_*` 是来源审计字段，不是标签，也不是默认模型输入。

## 历史兼容

`feature_table_v0`、`diagnostic_activity_v0` 和 augmentation 文件只用于历史复现或明确的可选实验。历史备份放 `_archive/backups/`，不得与当前目标文件混放。

英文版见 `README_en.md`。
