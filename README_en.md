# Cas12a ML Project Data

This repository organizes CRISPR-Cas12a paper and repository data into a traceable basis for later machine-learning work.

Core rules:

- Audit first, clean second, model last.
- Treat `01_raw/` as read-only: do not rename, overwrite, or modify source files.
- Keep label systems separate. Editing activity, diagnostic activity, SNV annotation, specificity, prediction scores, and metadata are different data paths.
- Every modeling row must remain traceable to its source, workbook, sheet, raw field, and processing script.
- Directory front pages contain current data and current documentation. Data backups belong in source-specific `_archive/backups/`; historical notes belong in run-specific `99_notes/runs/` directories.

## Directory Structure

### `00_data_catalog/`

Project navigation center. It contains the source-level catalog, workbook/sheet index, and label dictionary, but no raw data. Start here when first using the repository.

### `01_raw/`

Unmodified papers, supplementary workbooks, repositories, README files, and source data. Scripts may read these files but must not write back to them.

### `02_extracted_tables/`

Traceable tables extracted from raw workbooks or other source files. Columns still retain their source meanings at this stage.

### `03_cleaned_minimal/`

Minimally standardized tables with fields such as `source_id`, `source_table_id`, `record_id`, sequence fields, raw labels, and label status. This is not the final training layer.

### `04_candidate_ml_dataset/`

Candidate modeling data organized by task and source:

- `diagnostic_activity_easydesign/`: EasyDesign_2024 diagnostic activity.
- `editing_activity_deepcas12a/`: DeepCas12a_2026 binary editing activity.
- `snv_specificity_extension/`: reserved SNV-specificity extension path.

Never merge labels directly across these subdirectories.

### `99_notes/`

Audit reports, evidence, unresolved questions, and decisions. Active questions are in `current/`; each operation and Git update has its own `runs/YYYYMMDD_HHMMSS_<operation-title-slug>/` directory.

### `scripts/`

Reproducible inspection, cleaning, feature-generation, and verification scripts. Contributor-supplied originals are preserved under `scripts/contributions/`.

## Recommended Workflow

1. Read `00_data_catalog/master_data_catalog.xlsx`, `source_sheet_index.xlsx`, and `label_dictionary.xlsx`.
2. Trace source tables through `02_extracted_tables/` and standardized rows through `03_cleaned_minimal/`.
3. For the EasyDesign baseline, use `04_candidate_ml_dataset/diagnostic_activity_easydesign/EasyDesign_2024_diagnostic_activity_feature_table_v1.csv` and read the bilingual baseline data usage guide first.
4. Use `baseline_train` for training and `baseline_validation` for validation, with `label_normalized` as the Table S3 primary label.
5. Keep Table S5 `external_test_scale_unconfirmed`, Table S4 optional augmentation, and paper prediction columns outside the default workflow.
6. Record uncertainties in `99_notes/current/problems_to_resolve_en.md` instead of guessing.

The v1 EasyDesign table preserves all v0 traceability fields and adds audited, deduplicated pairwise, positional, mismatch-type, and local-sequence features. Full generated features and QC live under `feature_engineering/`; collaborator and reference evaluation outputs live under `evaluation/` and are not experimental labels.
