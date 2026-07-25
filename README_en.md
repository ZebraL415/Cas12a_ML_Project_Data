# Cas12a ML Project Data

This repository organizes CRISPR-Cas12a paper and repository data into traceable machine-learning candidates. Its central logic is: **audit first, clean second, model last**.

## Core Rules

- `01_raw/` is read-only: do not modify, overwrite, or rename files.
- Do not merge label systems: diagnostic fluorescence, editing binary labels, indel frequency, specificity ratios, prediction scores, and annotations remain separate.
- Every candidate row must trace to a source, file, sheet, original column, and processing script.
- Record uncertain fields in `99_notes/current/problems_to_resolve_*.md`; do not guess.
- Store data-layer backups under each directory's `_archive/backups/`; store every operation under `99_notes/runs/YYYYMMDD_HHMMSS_<git-title-slug>/`.

## Directory Map

- `00_data_catalog/`: source, sheet, and label dictionaries; start here when first using the repository.
- `01_raw/`: read-only paper, supplement, and repository originals.
- `02_extracted_tables/`: traceable raw-derived intermediate tables retaining source semantics.
- `03_cleaned_minimal/`: minimally standardized and QC tables, not final training datasets.
- `04_candidate_ml_dataset/`: candidate model tables and usage guides separated by task and source.
- `99_notes/current/`: current questions, decisions, and paper notes.
- `99_notes/runs/`: per-run audits, methods, evidence traces, and Git records.
- `scripts/`: reproducible processing and verification scripts.

## Current Two Data Tracks

### EasyDesign Diagnostic Activity

Current Package1 entry: `04_candidate_ml_dataset/diagnostic_activity_easydesign/feature_engineering_v3_package1/EasyDesign_2024_diagnostic_activity_feature_table_v3.csv`. Formal input columns must be read from `EasyDesign_2024_feature_block_manifest_v3.csv` in the same directory.

The P1-0 unified baseline uses:

```text
baseline_split in {baseline_train, baseline_validation}
label_is_primary_baseline == yes
source_table_id == EasyDesign_2024_TableS3_training
```

This yields 10,634 Table S3 development records: 8,417 training and 2,217 fixed-validation rows. Gap-aware V3 no longer excludes the 740 gap records by default. The 1,358 Table S5 rows remain external ranking validation and must not enter feature selection. V3 thermodynamic columns are conditionally retained proxies, not measured R-loop Delta G. Complete P1-0/P1-1 code and results are stored locally in `/Users/linzibo/Cas12a_ML_Project/`.

### DeepCas12a Editing Activity

Its entry is under `04_candidate_ml_dataset/editing_activity_deepcas12a/`. Its label is binary AsCas12a editing activity, not fluorescence/RFU, and must not be merged with EasyDesign.

## New-Member Workflow

1. Read `00_data_catalog/README_en.md` and the three xlsx catalogs.
2. Select the correct task under `04_candidate_ml_dataset/` and read its usage guide.
3. Trace fields through `03_cleaned_minimal/` and `02_extracted_tables/`; inspect `01_raw/` only when necessary and never write to it.
4. Check `99_notes/current/` before running work; reproduce processing from the project root with `scripts/` and record it in a new run directory.

The repository currently prepares candidate data and baseline-workflow inputs; model training is not performed during data organization.
