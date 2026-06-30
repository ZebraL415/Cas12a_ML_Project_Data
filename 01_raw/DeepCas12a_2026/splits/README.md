# Split and Partition CSV Files

This directory contains the explicit split files requested for reproducibility.

## `ht1_train_test_split.csv`

This CSV records the HT1 train/test split used in this repository:

```text
HT1-1 training records: 15,000
HT1-2 test records: 1,292
Total HT1 records: 16,292
```

Columns:

```text
source_file, source_row, sequence, methylation_status, dnase_signal_status, label, ht1_index, split
```

`source_row` and `ht1_index` are zero-based. `split` is either `train` or `test`.

## `deepcas12a_9fold_partitions.csv`

This CSV records the 9-fold cross-validation partitions for `Dataset/train_HT1-1_plus_HEK_in_situ.txt`.

Columns:

```text
source_file, source_row, sequence, methylation_status, dnase_signal_status, label, training_index, fold, partition
```

`source_row` and `training_index` are zero-based. `partition` is either `train` or `validation` for each fold.
