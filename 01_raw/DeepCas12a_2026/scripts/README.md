# Reproducibility Scripts

This directory contains the scripts used to reproduce DeepCas12a training and the reported hyperparameter optimization procedure.

## Train DeepCas12a

```bash
python scripts/train_deepcas12a.py \
  --train-data Dataset/train_HT1-1_plus_HEK_in_situ.txt \
  --test-data Dataset/HT1-2_test.txt \
  --partitions-csv splits/deepcas12a_9fold_partitions.csv \
  --output-dir results/deepcas12a
```

The default training settings match the manuscript response:

```text
batch_size = 256
learning_rate = 2.001718570896886e-4
weight_decay = 1e-4
epochs = 70
early_stopping_patience = 10
early_stopping_min_delta = 0.0
n_splits = 9
seed = 42
```

## Optuna Hyperparameter Search

```bash
python scripts/optuna_search_deepcas12a.py \
  --train-data Dataset/train_HT1-1_plus_HEK_in_situ.txt \
  --partitions-csv splits/deepcas12a_9fold_partitions.csv \
  --output-dir results/optuna
```

This script implements the Optuna TPE search procedure described in the manuscript. It uses the following search space:

```text
learning_rate: log-uniform [1e-5, 1e-3]
attention_dropout: uniform [0.1, 0.5]
dropout: uniform [0.1, 0.5]
depth: integer [4, 12]
embed_dim: {64, 128, 256, 512}
mlp_ratio: uniform [1.0, 4.0]
num_heads: {4, 8, 12, 16}
```
