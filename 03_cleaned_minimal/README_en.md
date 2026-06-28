# 03_cleaned_minimal

This directory stores minimally standardized tables. Data here have been mapped from original column names into comparable fields, but they are still not final machine-learning training datasets.

## Current key files

- `diagnostic_activity_minimal.csv`: main minimally cleaned EasyDesign diagnostic activity table.
- `diagnostic_activity_augmented_optional.csv`: optional augmented data, not included in the default baseline.
- `README_cleaning_notes.md`: cleaning notes.
- Other `*_minimal.csv` files: placeholders or tables reserved for later paths.

## Usage rules

- Each row should be traceable to a source, source table, record ID, and original label column.
- `label_status` must distinguish measured, predicted, annotation, metadata, or unclear.
- Do not force uncertain fields into standardized columns. Record unresolved issues in `99_notes/problems_to_resolve.md`.

## Archive

Historical backups are stored in `_archive/backups/`. The directory front page keeps only current minimally cleaned versions.
