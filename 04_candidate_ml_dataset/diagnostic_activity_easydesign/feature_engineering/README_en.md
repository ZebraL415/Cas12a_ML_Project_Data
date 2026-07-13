# EasyDesign Feature Engineering

This directory stores complete EasyDesign feature-engineering outputs and feature-selection records.

- `EasyDesign_2024_feature_selection_manifest_v1.csv`: per-feature inclusion status, reference importance, and inclusion or exclusion rationale.
- `EasyDesign_2024_feature_table_v1_qc.json`: row, column, split, duplicate, and positional-missing checks for v1.
- `full_generated/`: the unmodified Xu generator rerun, including all 139 features, orientation comparison, row audit, feature dictionary, and generation report.

The default training entry point remains the parent-directory `EasyDesign_2024_diagnostic_activity_feature_table_v1.csv`. More columns do not automatically make the full generated table a better model input.
