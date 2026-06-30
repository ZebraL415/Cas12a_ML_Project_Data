# Run Report: Organize Candidate ML Datasets By Source Path

## Scope

This round only reorganized the `04_candidate_ml_dataset/` directory structure and README files. It did not modify `01_raw/`.

## Completed

- Created `diagnostic_activity_easydesign/` for EasyDesign_2024 diagnostic activity v0 data, usage guides, split plans, and build reports.
- Renamed EasyDesign current files with an explicit source prefix, for example `EasyDesign_2024_diagnostic_activity_feature_table_v0.csv`.
- Moved EasyDesign historical backups from the top-level `_archive/backups/` into `diagnostic_activity_easydesign/_archive/backups/`.
- Created `snv_specificity_extension/` and moved the empty placeholder `snv_specificity_extension_v0.csv`.
- Kept `editing_activity_deepcas12a/` as the DeepCas12a_2026 editing activity data directory.
- Updated `04_candidate_ml_dataset/README.md` and `README_en.md` so the top level serves only as a navigation page.
- Updated the root README paths pointing to `04_candidate_ml_dataset/`.

## Decision

`04_candidate_ml_dataset/` should be organized by task path and source, rather than mixing all v0 tables at the top level. This reduces the risk of accidentally merging EasyDesign diagnostic activity labels with DeepCas12a editing activity labels.
