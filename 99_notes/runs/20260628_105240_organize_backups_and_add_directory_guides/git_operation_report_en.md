# Git Operation Record: Organize Backups And Add Directory Guides

## Git information

- Time: 2026-06-28 10:52:40 +0800
- Commit: `d4bbe55`
- Commit title: `Organize backups and add directory guides`
- Branch: `main`
- Remote: `origin/main`

## Operation

- Moved 75 historical backup files into the corresponding `_archive/backups/` directories.
- Added Chinese and English README files under `00_data_catalog/`, `01_raw/`, `02_extracted_tables/`, `03_cleaned_minimal/`, `04_candidate_ml_dataset/`, and `99_notes/`.
- Updated the root README to state that directory front pages keep only current active files and historical backups go into `_archive/backups/`.

## Note

This operation did not modify existing raw source files under `01_raw`; it only added project-level README files there.
