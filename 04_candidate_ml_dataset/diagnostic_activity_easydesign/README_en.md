# diagnostic_activity_easydesign

This directory stores EasyDesign_2024 `diagnostic_activity` candidate data. The labels represent experimental Cas12a diagnostic fluorescence activity and must not be merged with DeepCas12a binary `editing_activity`.

## Version Entry Points

- `EasyDesign_2024_diagnostic_activity_feature_table_v2.csv`: immutable V2 gap-aware core parent, 11,992 rows × 188 columns, with 130 core candidate inputs.
- `feature_engineering_v2/`: V2 dictionary and QC.
- `feature_engineering_v2_1_context/`: non-overwriting context extension, 11,992 rows × 246 columns, with a frozen manifest of 188 nominal inputs.
- `feature_engineering_v3_package1/`: the current Package1 data entry point, 11,992 rows × 250 columns, fully inheriting V2.1 and adding four audited thermodynamic proxies for 192 nominal inputs.
- `EasyDesign_2024_v2_data_usage_guide_zh.md` / `_en.md`: provenance, labels, splits, and gap-aware usage boundaries.

## Current Recommended Workflow

Use V2 core to reproduce the earlier baseline. Package1 and subsequent Horizontal experiments should define inputs with `feature_engineering_v3_package1/EasyDesign_2024_feature_block_manifest_v3.csv` and use P1-0 as the unified baseline. The 10,634 Table S3 records form development data; target-grouped CV selects features only within the 8,417 `baseline_train` records. The 1,358 Table S5 records are reserved for external ranking validation and must not enter feature selection or training.

The V3 `nonpositional4_candidate` table retains only alignment, substitution, context, and thermodynamic blocks. Its name does not mean that all four are proven high-impact. P1-1 supports context, substitution, and alignment most strongly; thermodynamics did not pass its formal promotion threshold.

Within each training fold, fit medians on training records only, fill residual missing values with zero, then remove columns constant in that fold. `mapping_*` fields are provenance metadata, not labels or default model inputs.

## Historical Compatibility

The v0 feature, diagnostic-activity, and augmentation files are for historical reproduction or explicit optional experiments only. Historical backups belong in `_archive/backups/`, separate from current target files.

Chinese version: `README.md`.
