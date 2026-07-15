# 03_cleaned_minimal

This directory stores traceable minimally standardized tables and QC tables. Source, record, sequence, and label fields begin to use shared names here, but these are still not final training datasets.

- `diagnostic_activity_minimal.csv`: main minimally cleaned EasyDesign diagnostic-activity table.
- `diagnostic_activity_augmented_optional.csv`: optional augmentation, excluded from the default baseline.
- `easydesign_mismatch/`: gap-preserving Table S3 alignment v2, Table S2 source mapping, and mismatch review queue.
- `editing_activity_minimal.csv`: minimally cleaned DeepCas12a editing-activity table.
- Other `*_minimal.csv` files: separate label paths.

Every row must trace to a source, source table, record ID, and original label. `label_status` must distinguish measured, predicted, annotation, metadata, or unclear. Record uncertainty under `99_notes/current/`. Store historical backups under `_archive/backups/`.
