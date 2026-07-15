# Cas12a ML Project Data

本库用于把 CRISPR-Cas12a 论文和仓库数据整理成可追溯的机器学习候选数据。中心逻辑是：**先审计，后清洗，再建模**。

## 核心规则

- `01_raw/` 只读：不修改、不覆盖、不重命名。
- 不合并不同标签体系：diagnostic fluorescence、editing binary label、indel frequency、specificity ratio、prediction score 和 annotation 必须分开。
- 每条候选数据必须能追溯到 source、文件、sheet、原始列和处理脚本。
- 不确定字段写入 `99_notes/current/problems_to_resolve_*.md`，不要猜。
- 数据层历史备份放各目录 `_archive/backups/`；每轮操作记录放 `99_notes/runs/YYYYMMDD_HHMMSS_<git-title-slug>/`。

## 目录导航

- `00_data_catalog/`：数据源、sheet 和标签词典；第一次接触本库先看这里。
- `01_raw/`：论文、补充表和仓库原件，只读。
- `02_extracted_tables/`：从 raw 拆出的可追溯中间表，仍保留原始语义。
- `03_cleaned_minimal/`：最小标准化和 QC 表，不是最终训练集。
- `04_candidate_ml_dataset/`：按任务和来源分开的候选建模表及使用指南。
- `99_notes/current/`：当前问题、决策和论文备注。
- `99_notes/runs/`：每轮审计、方法、证据链和 Git 记录。
- `scripts/`：可复现处理和验证脚本。

## 当前两条数据主线

### EasyDesign diagnostic activity

推荐入口：`04_candidate_ml_dataset/diagnostic_activity_easydesign/EasyDesign_2024_diagnostic_activity_feature_table_v2.csv`。

第一次 baseline 只用：

```text
default_training_eligibility == eligible_core_v2
baseline_split in {baseline_train, baseline_validation}
label_is_primary_baseline == yes
```

这得到 9,894 条无 gap Table S3 记录。先读同目录 `EasyDesign_2024_v2_data_usage_guide_zh.md`；740 条 gap 行只能在明确支持 gap 的第二阶段加入，1,358 条 Table S5 行只作尺度未确认的外部测试候选。

### DeepCas12a editing activity

入口位于 `04_candidate_ml_dataset/editing_activity_deepcas12a/`。它的标签是二分类 AsCas12a editing activity，不是 fluorescence/RFU，不能与 EasyDesign 合并。

## 新成员使用顺序

1. 读 `00_data_catalog/README.md` 和三份 xlsx catalog。
2. 在 `04_candidate_ml_dataset/` 选择正确任务，只读对应使用指南。
3. 用 `03_cleaned_minimal/` 和 `02_extracted_tables/` 追溯字段；必要时再查看 `01_raw/`，不要写入。
4. 运行前查看 `99_notes/current/`；复现处理时从项目根目录运行 `scripts/`，并把记录写入新的 run 目录。

本库当前只准备候选数据和 baseline workflow 输入，不在数据整理步骤中训练模型。
