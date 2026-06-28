# 04_candidate_ml_dataset

This directory stores candidate modeling datasets. Data enter this layer only when labels are relatively clear, record units are consistent enough, and sources are traceable.

## Recommended entry point for the first baseline

- `diagnostic_activity_feature_table_v0.csv`: recommended input table for the first baseline workflow.
- `diagnostic_activity_v0.csv`: candidate diagnostic activity main table with dataset-oriented fields.
- `diagnostic_activity_augmented_optional_v0.csv`: optional augmented data, not mixed into the default baseline.

## Supporting documents

- `baseline_data_usage_guide_zh.md` / `baseline_data_usage_guide_en.md`: how to use the candidate data for baseline work.
- `split_plan_zh.md` / `split_plan_en.md`: recommended data split plan.
- `dataset_build_report_zh.md` / `dataset_build_report_en.md`: dataset construction report.

## Usage rules

- The default label column is `label_normalized`.
- By default, use only rows with `label_is_primary_baseline == yes`.
- `paper_prediction_*` fields are paper model predictions, not experimental labels.
- Before model training, confirm split, label status, and source provenance again.

## Archive

Historical backups are stored in `_archive/backups/`. The directory front page keeps only current v0 data and latest documentation.
