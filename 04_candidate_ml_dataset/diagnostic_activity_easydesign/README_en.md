# diagnostic_activity_easydesign

This directory stores EasyDesign_2024 candidate diagnostic activity data. It belongs to the CRISPR-Cas12a diagnostics activity path and must not be merged with DeepCas12a binary editing activity labels.

## Current Files

- `EasyDesign_2024_diagnostic_activity_feature_table_v0.csv`: recommended entry point for the first EasyDesign baseline.
- `EasyDesign_2024_diagnostic_activity_v0.csv`: candidate diagnostic activity main table.
- `EasyDesign_2024_diagnostic_activity_augmented_optional_v0.csv`: optional augmented data, not mixed into the default baseline.
- `EasyDesign_2024_baseline_data_usage_guide_zh.md` / `EasyDesign_2024_baseline_data_usage_guide_en.md`: data usage guide.
- `EasyDesign_2024_split_plan_zh.md` / `EasyDesign_2024_split_plan_en.md`: split plan.
- `EasyDesign_2024_dataset_build_report_zh.md` / `EasyDesign_2024_dataset_build_report_en.md`: dataset build report.

## Usage Rules

- The default label column is `label_normalized`.
- By default, use only rows with `label_is_primary_baseline == yes`.
- `paper_prediction_*` fields are paper model predictions, not experimental labels.
- Table S4 augmented data should be used only when augmentation is explicitly enabled.
- Historical backups are stored in `_archive/backups/`.
