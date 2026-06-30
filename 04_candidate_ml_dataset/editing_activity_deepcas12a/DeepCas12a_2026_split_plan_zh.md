# DeepCas12a_2026 划分计划

## 默认划分

- `baseline_train`：`Dataset/train_HT1-1_plus_HEK_in_situ.txt`，15,203 行。
- `holdout_test_HT1-2`：`Dataset/HT1-2_test.txt`，1,292 行。
- `independent_test_HT2`：`Dataset/HT2_test.txt`，2,963 行。
- `independent_test_HT3`：`Dataset/HT3_test.txt`，1,251 行。

## 9-fold validation

使用 `DeepCas12a_2026_9fold_partitions_v0.csv`。该文件来自 `splits/deepcas12a_9fold_partitions.csv`，用于 `train_HT1-1_plus_HEK_in_situ.txt` 的内部交叉验证。

## 注意

不要随机重新划分全部数据后再报告与论文可比的结果；HT1-2、HT2、HT3 应保留为测试集。
