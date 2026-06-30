# DeepCas12a_2026 Dataset Build Report

## Input Source Tables

- Recommended training: `Dataset/train_HT1-1_plus_HEK_in_situ.txt`
- Tests: `Dataset/HT1-2_test.txt`, `Dataset/HT2_test.txt`, `Dataset/HT3_test.txt`
- Split metadata: `splits/deepcas12a_9fold_partitions.csv`

## Output Data

- `DeepCas12a_2026_editing_activity_binary_v0.csv`
- `DeepCas12a_2026_editing_activity_feature_table_v0.csv`
- `DeepCas12a_2026_9fold_partitions_v0.csv`
- `DeepCas12a_2026_ht1_train_test_split_v0.csv`

## Row Counts

- candidate v0: 20709
- feature table: 20709

## Label

The label column is `label_normalized`, with values 0/1. It represents binary high/low AsCas12a on-target editing activity. It is not fluorescence/RFU and not continuous indel frequency.
