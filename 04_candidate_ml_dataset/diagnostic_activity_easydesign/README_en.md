# diagnostic_activity_easydesign

This directory stores EasyDesign_2024 `diagnostic_activity` candidates. The label is experimentally measured Cas12a diagnostic fluorescence activity and must not be merged with DeepCas12a binary `editing_activity`.

## Recommended Entry

- `EasyDesign_2024_diagnostic_activity_feature_table_v2.csv`: current recommended gap-aware baseline input with 11,992 rows and 188 columns.
- `EasyDesign_2024_v2_data_usage_guide_zh.md` / `_en.md`: required reading before running any model.
- `EasyDesign_2024_dataset_build_report_v2_zh.md` / `_en.md`: v2 sources, row counts, corrections, and limitations.
- `feature_engineering_v2/`: 145-row feature dictionary and automated QC.

For the first baseline, use only `default_training_eligibility == eligible_core_v2`, then apply the existing `baseline_split` for training/validation. This gives 9,894 no-gap Table S3 records. The 740 `conditional_gap_aware_v2` rows may enter only when the model explicitly supports gaps; the 1,358 Table S5 external-test records must not enter training.

## Compatibility and Optional Files

- `EasyDesign_2024_diagnostic_activity_feature_table_v0.csv`: retained for historical reproduction; its old position features after gap deletion are unsuitable for the 740 indel rows.
- `EasyDesign_2024_diagnostic_activity_v0.csv`: v0 candidate main table.
- `EasyDesign_2024_diagnostic_activity_augmented_optional_v0.csv`: Table S4 augmentation, excluded by default.
- Original v0 usage guide, split plan, and build report: for old-version reproduction only.

`mapping_*` fields are source-audit metadata, not labels or default numeric model inputs. Store historical backups under `_archive/backups/`.
