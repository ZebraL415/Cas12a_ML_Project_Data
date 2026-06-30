# Dataset

This directory contains the model-ready datasets used for DeepCas12a training and evaluation.

## Format

All `.txt` files are whitespace-delimited and do not include a header. The column order is:

```text
sequence methylation_status dnase_signal_status label
```

Each `sequence`, `methylation_status`, and `dnase_signal_status` value is 34 characters long. Labels are binary: `0` for low AsCas12a on-target activity and `1` for high AsCas12a on-target activity.

## Files

| File | Source file | Role | Records | Preprocessing |
|---|---|---:|---:|---|
| `HT1-1_train.txt` | `Dataset_HT_1_3new.txt` plus 2 records from HT1-2 | HT1-1 training split | 15,000 | HT epigenetic features standardized to unmethylated/open |
| `HT1-2_test.txt` | `Dataset_HT_1_4new.txt` after moving 2 records to HT1-1 | HT1-2 test split | 1,292 | HT epigenetic features standardized to unmethylated/open |
| `HT2_test.txt` | `Dataset_HT2.txt` | independent HT2 test set | 2,963 | HT epigenetic features standardized to unmethylated/open |
| `HT3_test.txt` | `Dataset_HT3.txt` | independent HT3 test set | 1,251 | HT epigenetic features standardized to unmethylated/open |
| `HEKplasmid_in_situ.txt` | `data-HEKplasmid.txt` | added HEK in situ training data | 55 | supplied A/N feature calls retained |
| `HEK_lenti_in_situ.txt` | `DatasetHEK-lenti.txt` | added HEK in situ training data | 148 | supplied A/N feature calls retained |
| `train_HT1-1_plus_HEK_in_situ.txt` | combined | final training set | 15,203 | `HT1-1_train.txt` plus both HEK in situ datasets |
| `dataset_summary.tsv` | generated summary | dataset manifest | 7 rows | record counts, labels, and skipped source lines |

HT1-1 and HT1-2 together contain 16,292 HT1 records.

## HT Epigenetic Standardization

The HT-derived datasets were generated from lentiviral-library target measurements. Because the actual integration loci are not known, genomic methylation and DNase values inferred from sequence alignment should not be interpreted as the true epigenetic context of the integrated targets.

For this reason, all HT-derived records were standardized before model input:

```text
methylation_status = NNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNN
dnase_signal_status = AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
```

This represents the HT records as unmethylated and accessible instead of assigning potentially misleading locus-specific epigenetic states.

## HEK In Situ Data

Two additional HEK datasets were added to the training set:

```text
HEKplasmid_in_situ.txt
HEK_lenti_in_situ.txt
```

Their supplied A/N feature calls were retained.

## Recommended Use

Use `train_HT1-1_plus_HEK_in_situ.txt` for model training and evaluate against:

```text
HT1-2_test.txt
HT2_test.txt
HT3_test.txt
```

For HT-only experiments, use `HT1-1_train.txt` as the training set.
