# Split Plan

## Split Plan
- Table S3 was split into baseline_train=8417 rows and baseline_validation=2217 rows.
- Method: compute a SHA1 hash bucket from `target_sequence`; bucket < 80 goes to training, and the rest goes to validation.
- Purpose: reduce the risk that the same target sequence appears in both training and validation.
- Table S5 is retained as external_test_scale_unconfirmed=1358 rows; it is not the default test set until label scale is confirmed.
- Table S4 is retained as optional_augmentation=31993 rows; the default baseline does not use it.
