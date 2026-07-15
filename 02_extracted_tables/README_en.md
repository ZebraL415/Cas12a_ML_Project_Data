# 02_extracted_tables

This directory stores intermediate tables extracted from `01_raw/`. They retain original column names and value semantics and need only be readable and traceable; they are not final training datasets.

- `diagnostic_activity/`: fluorescence/RFU/diagnostic activity; EasyDesign mismatch source tables are under `diagnostic_activity/easydesign_mismatch_mapping/`.
- `editing_activity/`: indel frequency, editing efficiency, or binary editing activity.
- `snv_annotation/`: SNVs, WT/alt sequences, and annotations.
- `snv_specificity/`: WT/mutant discrimination and specificity ratios.
- `predicted_library/`: model prediction scores or candidate libraries, not experimental labels.

File names should include source, year, table/sheet ID, data type, and `raw`. Standardized outputs go to `03_cleaned_minimal/`; label systems must not be merged here. Store historical data backups in the relevant subdirectory's `_archive/backups/`.
