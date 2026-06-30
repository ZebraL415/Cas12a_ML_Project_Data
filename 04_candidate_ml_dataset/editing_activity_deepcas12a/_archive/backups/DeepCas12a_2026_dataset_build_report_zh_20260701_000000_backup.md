# DeepCas12a_2026 数据集构建报告

## 输入源表

- 推荐训练：`Dataset/train_HT1-1_plus_HEK_in_situ.txt`
- 测试：`Dataset/HT1-2_test.txt`、`Dataset/HT2_test.txt`、`Dataset/HT3_test.txt`
- 划分元数据：`splits/deepcas12a_9fold_partitions.csv`

## 输出数据

- `DeepCas12a_2026_editing_activity_binary_v0.csv`
- `DeepCas12a_2026_editing_activity_feature_table_v0.csv`
- `DeepCas12a_2026_9fold_partitions_v0.csv`
- `DeepCas12a_2026_ht1_train_test_split_v0.csv`

## 行数

- candidate v0：20709
- feature table：20709

## 标签

标签列为 `label_normalized`，数值为 0/1。该标签代表 high/low AsCas12a on-target editing activity 的二分类，不是 fluorescence/RFU，也不是连续 indel frequency。
