# 04_candidate_ml_dataset

This directory stores candidate modeling datasets. The top level is only a navigation page; concrete datasets are stored in subdirectories named by `path_type + source` so different tasks and label systems do not mix.

## Subdirectories

- `diagnostic_activity_easydesign/`: EasyDesign_2024 diagnostic activity candidate data. Labels come from the CRISPR fluorescence/activity system.
- `editing_activity_deepcas12a/`: DeepCas12a_2026 editing activity candidate data. Labels are binary AsCas12a editing activity labels.
- `snv_specificity_extension/`: reserved directory for SNV specificity extension data. It currently contains only an empty placeholder table.

## Usage Rules

- Enter the relevant subdirectory and read `README.md` / `README_en.md` first.
- Do not directly merge labels across subdirectories; diagnostic activity, editing activity, and SNV specificity are different tasks.
- Each subdirectory manages its own current v0 files, usage guide, split plan, build report, and `_archive/backups/`.
- The top level no longer stores concrete data tables.

## Recommended Entry Points

- EasyDesign baseline: `diagnostic_activity_easydesign/EasyDesign_2024_diagnostic_activity_feature_table_v0.csv`
- DeepCas12a baseline: `editing_activity_deepcas12a/DeepCas12a_2026_editing_activity_feature_table_v0.csv`
