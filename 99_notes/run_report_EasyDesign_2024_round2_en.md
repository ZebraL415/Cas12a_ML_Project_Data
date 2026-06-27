# EasyDesign_2024 Round-2 Run Report

## Scope
Input sources: `01_raw/EasyDesign_2024`, the original paper PDF, and the supporting-information screenshot.

## Files Generated In This Round
- `00_data_catalog/master_data_catalog.xlsx`
- `00_data_catalog/source_sheet_index.xlsx`
- `00_data_catalog/label_dictionary.xlsx`
- `03_cleaned_minimal/diagnostic_activity_minimal.csv`
- `03_cleaned_minimal/diagnostic_activity_augmented_optional.csv`
- `04_candidate_ml_dataset/diagnostic_activity_v0.csv`
- `04_candidate_ml_dataset/diagnostic_activity_feature_table_v0.csv`
- `04_candidate_ml_dataset/diagnostic_activity_augmented_optional_v0.csv`

## Classification Decisions
- Table S3: diagnostic_activity, high priority, primary internal-baseline table.
- Table S4: diagnostic_activity, high priority, but optional augmentation.
- Table S5: diagnostic_activity, high priority, external paper test; prediction columns are not labels.
- Table S7/S8: experimental validation metadata.
- Fig.S3: metadata/figure source data, not training data.

## Data Quality Checks
- Primary v0 rows: 11992.
- Feature table rows: 11992.
- Table S5 target-window method counts: {"source_defined_10nt_flank_window": 1337, "best_match_fallback": 21}.
- Table S5 DNA context length counts: {"45": 1337, "42": 10, "36": 8, "44": 3}.
- Table S5 target-window start counts: {"10": 1339, "7": 8, "1": 8, "9": 3}.
- Unique Table S3 target_at_guide sequences: 8621.

## Next Recommended Actions
- Run the first baseline on `baseline_split` values baseline_train/baseline_validation.
- Do not include Table S4 in the default baseline unless augmentation is explicitly enabled.
- Do not treat Table S5 and Table S3 as one shared numeric label scale until a label transform is confirmed.
