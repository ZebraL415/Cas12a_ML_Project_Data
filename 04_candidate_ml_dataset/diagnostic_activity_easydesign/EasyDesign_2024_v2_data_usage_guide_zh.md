# EasyDesign 2024 v2 数据使用指南

## 1. 适用范围

本指南用于后续尚未确定模型类型的 baseline workflow。数据属于 `diagnostic_activity`，标签是实验测得的 Cas12a 荧光活性，不得与 DeepCas12a 的二分类 `editing_activity` 合并。

主文件：`EasyDesign_2024_diagnostic_activity_feature_table_v2.csv`。该表有 11,992 行、188 列，其中 Table S3 10,634 行，Table S5 1,358 行。v2 没有新增、删除或改写标签，也没有改变 v0 的 `baseline_split`。

## 2. 推荐的第一次 baseline

只选择以下记录：

```text
default_training_eligibility == eligible_core_v2
baseline_split in {baseline_train, baseline_validation}
label_is_primary_baseline == yes
```

得到 9,894 条无 gap 的 Table S3 记录：训练 7,832 条，验证 2,062 条。标签使用 `label_normalized`。相同 `guide_target_pair_id` 不跨训练/验证集合。

第一轮可从特征词典中筛选 `default_model_role == candidate_input` 的数值列。为保持模型无关性，建议先使用：

- pair-level：`aligned_difference_count`、`substitution_count`、PAM/spacer difference count、首末错配位置和最长连续匹配/替换长度。
- position-level：`difference_pos_01..25` 和 `substitution_pos_01..25`。
- composition：guide、target、guide spacer 和 target spacer 的 GC、碱基比例、Shannon entropy、最长 homopolymer。

不要把 `label_*`、`paper_prediction_*`、`mapping_*`、`source_*`、`record_id`、`guide_target_hamming_dist_raw` 或 `guide_target_hamming_dist_computed_v0_legacy` 放入默认输入。

## 3. gap-aware 第二阶段

在无 gap baseline 跑通后，可单独加入：

```text
default_training_eligibility == conditional_gap_aware_v2
```

该层有 740 条记录，训练 585 条、验证 155 条。模型必须能够显式处理 `target_gap_pos_01..25`，不得使用删除 `-` 后左移的旧位置特征。应分别报告 no-gap 与 gap 子集表现，并进行“仅无 gap”对“加入 gap”的消融比较。

`gap_in_target` 是对齐通道名称，不是已确认的生物学 deletion 方向；解释 indel 类型时必须保留这一限制。

## 4. Table S5 外部测试

`default_training_eligibility == external_test_only_scale_unconfirmed` 的 1,358 行来自 Table S5。它们只能作为论文外部测试候选，不能加入训练；`true value` 与 Table S3 `30 min` 的尺度关系未确认，跨表比较前需要单独的标度决策。

## 5. 来源映射的使用

- `mapping_confidence == high`：7,421 条 Table S3 记录具有唯一精确模板窗口。
- `mapping_confidence == medium`：3,146 条在单一模板组内有多模板命中。
- `mapping_confidence == review`：67 条涉及多组、IUPAC 兼容或未映射情况。

mapping 字段适合做来源审计、template-group 分组验证和敏感性分析，不适合作为默认模型输入。需要最严格来源子集时，可额外筛选 `mapping_confidence == high`，但应同时报告样本量变化。

## 6. 最小加载示例

```python
import pandas as pd

data = pd.read_csv(
    "EasyDesign_2024_diagnostic_activity_feature_table_v2.csv",
    low_memory=False,
)
dictionary = pd.read_csv(
    "feature_engineering_v2/EasyDesign_2024_feature_dictionary_v2.csv"
)

core = data.query("default_training_eligibility == 'eligible_core_v2'")
train = core.query("baseline_split == 'baseline_train'")
valid = core.query("baseline_split == 'baseline_validation'")

feature_names = dictionary.loc[
    dictionary["default_model_role"].eq("candidate_input"), "feature_name"
].tolist()
feature_names = [name for name in feature_names if name in data.columns]

X_train = train[feature_names]
y_train = train["label_normalized"]
X_valid = valid[feature_names]
y_valid = valid["label_normalized"]
```

本示例只完成安全取数，不包含缺失值策略、标准化、模型选择、调参或训练。

## 7. 结果报告要求

每次建模至少记录数据文件 SHA-256、筛选条件、使用的 feature list、train/validation 行数、随机种子和软件版本。分别报告 no-gap、gap、high/medium/review mapping 分层结果，避免把来源歧义或 indel 处理差异隐藏在总体指标中。
