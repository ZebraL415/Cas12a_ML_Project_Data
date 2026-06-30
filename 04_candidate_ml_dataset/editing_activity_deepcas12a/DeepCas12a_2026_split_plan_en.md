# DeepCas12a_2026 Split Plan

## Default Split

- `baseline_train`: `Dataset/train_HT1-1_plus_HEK_in_situ.txt`, 15,203 rows.
- `holdout_test_HT1-2`: `Dataset/HT1-2_test.txt`, 1,292 rows.
- `independent_test_HT2`: `Dataset/HT2_test.txt`, 2,963 rows.
- `independent_test_HT3`: `Dataset/HT3_test.txt`, 1,251 rows.

## 9-fold validation

Use `DeepCas12a_2026_9fold_partitions_v0.csv`. It comes from `splits/deepcas12a_9fold_partitions.csv` and is intended for internal cross-validation on `train_HT1-1_plus_HEK_in_situ.txt`.

## Note

Do not randomly repartition all rows if the goal is to report results comparable to the paper. HT1-2, HT2, and HT3 should remain test sets.
