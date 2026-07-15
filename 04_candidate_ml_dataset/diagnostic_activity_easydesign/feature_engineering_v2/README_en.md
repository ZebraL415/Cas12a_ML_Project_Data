# EasyDesign Feature Engineering v2

This directory documents feature definitions and automated QC for `EasyDesign_2024_diagnostic_activity_feature_table_v2.csv`.

- `EasyDesign_2024_feature_dictionary_v2.csv`: inputs, formulas, gap behavior, and default model roles for 145 new or key fields.
- `EasyDesign_2024_feature_qc_v2.json`: row-count, label/split preservation, gap strata, Hamming comparison, and pair-level split-leakage checks.

Default candidate inputs are limited to fields with `default_model_role == candidate_input`. `source_mapping`, raw Hamming, labels, source IDs, and QC fields must not be used as default numeric features.
