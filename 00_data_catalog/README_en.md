# 00_data_catalog

This directory is the navigation center of the project. It stores indexes, dictionaries, and source-level documentation, not raw experimental files.

## Files to inspect first

- `master_data_catalog.xlsx`: source-level catalog. Each row represents one data source and records source identity, path type, label status, and trainability.
- `source_sheet_index.xlsx`: worksheet-level catalog. Each row represents one workbook sheet and records sheet name, dimensions, example values, preliminary classification, and extraction recommendation.
- `label_dictionary.xlsx`: label dictionary. It prevents experimental labels, prediction scores, annotation fields, and metadata fields from being mixed.

## Usage rules

- Register a new source here before exporting tables to `02_extracted_tables/`.
- Do not merge different label systems into a single label.
- If a field meaning is uncertain, record the question in `99_notes/problems_to_resolve.md`.

## Archive

Historical backups are stored in `_archive/backups/`. The directory front page keeps only the current active versions.
