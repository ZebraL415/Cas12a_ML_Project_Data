# Run Report

## Scope

Integrate Xu's EasyDesign engineered-feature script and first-run importance result, audit the designated improved outputs, and build and document EasyDesign diagnostic-activity feature table v1.

## Inputs Scanned

- `EasyDesign_2024_diagnostic_activity_feature_table_v0.csv`
- `/Users/linzibo/Documents/generate_validated_engineered_features.py`
- `/Users/linzibo/Documents/first_run_feature_importance_top30.csv`
- Six result files under `/Users/linzibo/Desktop/MLRS/improved_feature_outputs/`
- `/Users/linzibo/Documents/mismatch_wide_table.xlsx`: checked only as a possible unspecified third file and skipped after confirming it does not belong to this pipeline

## Outputs Generated

- Recommended data: `EasyDesign_2024_diagnostic_activity_feature_table_v1.csv`
- Full features and QC under `feature_engineering/`
- Collaborator and reference results under `evaluation/`
- Reproducible scripts: `scripts/build_easydesign_feature_table_v1.py` and `scripts/verify_easydesign_feature_results.py`
- Preserved contribution: `scripts/contributions/xu/generate_validated_engineered_features.py`
- Bilingual audit, evidence, method, selection, and run-report files in this run directory

## Classification Decisions

- All new tables remain `diagnostic_activity`; the label remains the experimentally measured Table S3 30-minute activity.
- Feature importance, predictions, and metrics are evaluation artifacts, not labels.
- Table S4 augmentation and Table S5 scale-unconfirmed statuses remain unchanged.

## Data Quality Checks

- v1 has 11,992 rows, 89 columns, no duplicate `record_id`, and split counts identical to v0.
- It adds 60 engineered features and changes 827 unaligned positional cells to missing.
- Computed Hamming agreement is 100%; labels and splits are unchanged.
- All 2,217 reference predictions belong to validation. Metric differences are below `3.1e-9`; maximum residual rounding difference is `1.19e-7`.

## Evidence Boundary

Confirmed facts come from file structure, column values, script execution, and row-level recomputation. Biological-region interpretation, training procedure, and causes of performance improvement remain preliminary because independent orientation evidence and improved-run training code are absent.

## Next Recommended Actions

- Run a five-feature v0 control and a v1 engineered-feature comparison with the same split and fully saved training configuration.
- Remove redundant features in the reference pipeline and reassess importance stability.
- Manually confirm the source convention for 740 short targets and the biological guide/target/PAM orientation.
- Do not report Table S5 external-test performance until label-scale mapping is confirmed.
