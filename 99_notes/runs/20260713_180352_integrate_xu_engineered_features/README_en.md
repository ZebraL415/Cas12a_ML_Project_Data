# Integrate Xu Engineered Features

This run integrates Xu's first-run feature-importance CSV and engineered-feature script, reruns the script against the EasyDesign v0 feature table, audits the reference improved outputs, and builds the recommended `EasyDesign_2024_diagnostic_activity_feature_table_v1.csv`.

The run performs audit, recomputation, feature selection, and data organization only. It does not train a model and does not merge EasyDesign diagnostic activity with DeepCas12a editing activity.

Main records:

- `data_audit_zh.md` / `data_audit_en.md`
- `evidence_trace_zh.md` / `evidence_trace_en.md`
- `feature_selection_rationale_zh.md` / `feature_selection_rationale_en.md`
- `method_notes_zh.md` / `method_notes_en.md`
- `run_report_zh.md` / `run_report_en.md`
- `verification_results.json`
- `input_manifest.csv`
