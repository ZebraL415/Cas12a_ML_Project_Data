# 02_extracted_tables

This directory stores intermediate tables extracted from raw files. These tables usually preserve original column names and original values. They are not final training datasets.

## Subdirectory meanings

- `diagnostic_activity/`: diagnostic activity tables, such as crRNA-target pairs, fluorescence, RFU, or activity scores.
- `editing_activity/`: editing activity tables, such as indel frequency or editing efficiency.
- `snv_annotation/`: SNV annotations, WT/alt sequences, or variant information.
- `snv_specificity/`: SNV discrimination, WT/mutant ratios, or specificity assay results.
- `predicted_library/`: predicted libraries, model scores, or candidate design outputs.

## Usage rules

- This layer only extracts traceable tables. It does not merge across label systems.
- File names should include source, year, table or sheet ID, data type, and the `raw` status.
- If a table enters cleaning, standardized outputs should be written to `03_cleaned_minimal/`.

## Archive

Historical backups for each subdirectory are stored in its own `_archive/backups/`. The subdirectory front page keeps only current active exports.
