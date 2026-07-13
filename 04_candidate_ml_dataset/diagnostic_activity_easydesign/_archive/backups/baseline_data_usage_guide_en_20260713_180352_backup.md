# Baseline Data Usage Guide

## Why This File Lives Here
This document is stored in `04_candidate_ml_dataset/diagnostic_activity_easydesign/` because it explains how EasyDesign diagnostic-activity candidate modeling data should enter the first baseline workflow. Raw extracted tables remain in `02_extracted_tables/`, and minimally cleaned tables remain in `03_cleaned_minimal/`, but the EasyDesign baseline should start from this directory.

## Recommended First Baseline Inputs
- Default training/validation file: `EasyDesign_2024_diagnostic_activity_feature_table_v0.csv`.
- Use only rows where `label_is_primary_baseline == yes`.
- Training set: `baseline_split == baseline_train`.
- Validation set: `baseline_split == baseline_validation`.
- Label column: `label_normalized`, but only within `label_scale_group == table_s3_log_or_transformed_30min_activity`.

## Data Not Used By Default Yet
- `baseline_split == external_test_scale_unconfirmed`: this is the Table S5 external test set with `true value`, but its numeric scale versus Table S3 is not confirmed.
- `EasyDesign_2024_diagnostic_activity_augmented_optional_v0.csv`: this is the Table S4 augmented dataset and should only be used when augmentation is explicitly enabled.
- All `paper_prediction_*` columns: these are paper model predictions and may be used only for reproduction checks or sanity checks, not as labels.

## Minimal Runnable Workflow
1. Read `EasyDesign_2024_diagnostic_activity_feature_table_v0.csv`.
2. Filter `label_is_primary_baseline == yes`.
3. Use `crRNA_sequence`, `target_sequence`, and the basic numeric features as baseline features.
4. Train on `baseline_train` and validate on `baseline_validation`.
5. Do not report Table S5 external test performance until the label-scale transform is resolved.
