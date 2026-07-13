# EasyDesign Engineered-Feature Data Audit

## Confirmed Facts

- The v0 input has 11,992 rows and 28 columns, no duplicate `record_id`, and valid DNA alphabets.
- The primary Table S3 baseline contains 10,634 rows: 8,417 train and 2,217 validation rows. The 1,358 Table S5 rows remain `external_test_scale_unconfirmed`.
- Xu's script reran unchanged and generated 139 engineered features. The full output has 11,992 rows and 155 columns and exactly preserves v0 record order.
- `direct` agrees exactly with `guide_target_hamming_dist_computed` across all 10,634 primary rows. Exact agreement with `guide_target_hamming_dist_raw` is 91.593%, with low correlation.
- Length, crRNA GC, and computed Hamming are reproduced exactly. The maximum target-GC difference is `4.35e-7`, caused by six-decimal rounding in v0.
- In Table S3, 740 targets are shorter than their crRNA: 585 train and 155 validation rows. The original generator writes `0` for unaligned positions; v1 changes 827 unaligned positional cells to missing.
- Xu's first-run `top30` file contains only five feature rows.
- The reference improved prediction file has 2,217 rows, all in the current `baseline_validation`; record IDs, sequences, and labels match row by row.
- Metrics recomputed from predictions are Spearman 0.765651, Pearson 0.747238, MAE 0.327815, RMSE 0.424830, and R2 0.554858.

## Preliminary Inferences

- The reference improved result supports modeling value in mismatch amount, fraction, position, type, and local sequence composition.
- Importance is affected by redundant variables: engineered mismatch count exactly duplicates computed Hamming, while match fraction equals one minus mismatch fraction. Using both weakens interpretation stability.
- Computational agreement supports reproducible generation under `direct`, but does not establish biological PAM-proximal, seed, or distal orientation.

## Exclusions

- `/Users/linzibo/Documents/mismatch_wide_table.xlsx` was scanned as a possible unspecified third file, but its 6,506-row, 30-column structure does not match EasyDesign v0 or the generator output, so it was not integrated.
- No `01_raw/` file was modified, no Table S3/S4/S5 label scales were merged, and no model was trained.
