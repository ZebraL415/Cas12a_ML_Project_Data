# 运行报告：Audit DeepCas12a 2026 editing activity data

## 范围

数据源：`01_raw/DeepCas12a_2026`；论文 PDF：`/Users/linzibo/Cas12a_ML_Project_Data/01_raw/DeepCas12a_2026/paper/s12864-026-13003-3_reference.pdf`。

## 输入

- DeepCas12a GitHub 仓库本地副本：`01_raw/DeepCas12a_2026`
- 论文 PDF：`/Users/linzibo/Cas12a_ML_Project_Data/01_raw/DeepCas12a_2026/paper/s12864-026-13003-3_reference.pdf`
- 读取的关键说明文件：`README.md`、`Dataset/README.md`、`Dataset/Data_Descriptions.txt`、`splits/README.md`、`scripts/README.md`

## 输出

- `02_extracted_tables/editing_activity/DeepCas12a_2026_HT1_1_train_editing_activity_binary_raw.csv`
- `02_extracted_tables/editing_activity/DeepCas12a_2026_HT1_2_test_editing_activity_binary_raw.csv`
- `02_extracted_tables/editing_activity/DeepCas12a_2026_HT2_test_editing_activity_binary_raw.csv`
- `02_extracted_tables/editing_activity/DeepCas12a_2026_HT3_test_editing_activity_binary_raw.csv`
- `02_extracted_tables/editing_activity/DeepCas12a_2026_HEKplasmid_in_situ_editing_activity_binary_raw.csv`
- `02_extracted_tables/editing_activity/DeepCas12a_2026_HEK_lenti_in_situ_editing_activity_binary_raw.csv`
- `02_extracted_tables/editing_activity/DeepCas12a_2026_train_HT1_1_plus_HEK_in_situ_editing_activity_binary_raw.csv`
- `02_extracted_tables/editing_activity/DeepCas12a_2026_ht1_train_test_split_split_metadata_raw.csv`
- `02_extracted_tables/editing_activity/DeepCas12a_2026_deepcas12a_9fold_partitions_split_metadata_raw.csv`
- `04_candidate_ml_dataset/editing_activity_deepcas12a/DeepCas12a_2026_editing_activity_binary_v0.csv`
- `04_candidate_ml_dataset/editing_activity_deepcas12a/DeepCas12a_2026_editing_activity_feature_table_v0.csv`
- `03_cleaned_minimal/editing_activity_minimal.csv`
- `04_candidate_ml_dataset/editing_activity_deepcas12a/DeepCas12a_2026_9fold_partitions_v0.csv`
- `04_candidate_ml_dataset/editing_activity_deepcas12a/DeepCas12a_2026_ht1_train_test_split_v0.csv`

## 分类判断

- path_type：`editing_activity`
- record unit：34 bp AsCas12a target-context record
- label：`label`，二分类 high/low AsCas12a on-target activity
- label_status：`measured`，但属于由 measured indel frequency 阈值化得到的 binary label
- priority：high

## 数据质量检查

- candidate v0 行数：20709
- feature table 行数：20709
- candidate label 分布：{"0": 12439, "1": 8270}
- 序列长度异常行数：0
- DNA alphabet 异常行数：0
- methylation 长度异常行数：0
- DNase 长度异常行数：0
- 严格 `TTTV` PAM 不匹配行数：4500；这些行全部为 `TTTT`，仍符合 `TTTN`，本轮保留并标记
- candidate 重复 key 行数：0

## 下一步建议

- 若要训练 DeepCas12a 路线 baseline，只使用 `editing_activity_deepcas12a/` 子目录内的数据。
- 不要与 EasyDesign 的 `diagnostic_activity` fluorescence/RFU 标签合并。
- 若后续需要连续 editing efficiency 回归标签，需要追溯 Kim et al. 原始 indel frequency，而不是使用本仓库已阈值化的 `label`。
