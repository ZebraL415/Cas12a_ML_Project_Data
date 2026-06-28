# Dataset Build Report

## Inputs
- Authoritative workbook: `01_raw/EasyDesign_2024/data/imt2214-sup-0002-tables1-9sourcedata (1).xlsx`.
- Evidence sources: original paper PDF, supporting-information screenshot, and round-1 catalog.

## Output Data
- `diagnostic_activity_v0.csv`: 11992 rows, containing the Table S3 primary internal baseline and the Table S5 external paper test.
- `diagnostic_activity_feature_table_v0.csv`: 11992 rows, containing basic sequence features.
- `diagnostic_activity_augmented_optional_v0.csv`: 31993 rows, containing the Table S4 optional augmentation.

## Retention / Exclusion Rules
- Keep original record id, source_table_id, source_sheet, label_raw_name, and label_scale_group.
- Do not force 30 min, 20 min normalized, out_logk_measurement, and true value into one label.
- Do not treat paper model prediction columns as labels.
