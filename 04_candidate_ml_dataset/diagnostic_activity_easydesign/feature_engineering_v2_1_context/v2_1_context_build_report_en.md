# EasyDesign v2.1 Context Feature Table Build Report

## Scope

This layer treats the V2 gap-aware core table as read-only and recomputes 58 sequence-context features row by row from `crRNA_sequence` and `target_ungapped`. It neither recomputes nor overwrites `target_aligned_25` or its mismatch/gap positional features. Labels, splits, provenance fields, and row order are unchanged.

## Results

- Parent table: `/Users/linzibo/Cas12a_ML_Project_Data/04_candidate_ml_dataset/diagnostic_activity_easydesign/EasyDesign_2024_diagnostic_activity_feature_table_v2.csv`
- Output table: `/Users/linzibo/Cas12a_ML_Project_Expr/V2-0_unified_baseline/runs/20260724T010300_V2-0-v2.1-context-build/EasyDesign_2024_diagnostic_activity_feature_table_v2_1_context.csv`
- Rows: 11,992
- Parent columns: 188
- Added context columns: 58
- Total output columns: 246
- Candidate model inputs: 188
- Output SHA-256: `39cda8368c216784507ac002df687b28a4f9cc6f81e2b0e84043e45eddb4c1c0`

## Quality Control

- PASS: `expected_58_context_features`
- PASS: `no_missing_context_values`
- PASS: `all_context_values_finite`
- PASS: `frequency_and_gc_values_in_0_1`
- PASS: `unique_base_count_in_1_4`
- PASS: `dinucleotide_frequencies_sum_to_one`
- PASS: `target_ungapped_contains_no_gap`
- PASS: `record_id_unique`
- PASS: `record_id_and_order_unchanged`
- PASS: `parent_columns_value_exact_after_roundtrip`
- PASS: `no_duplicate_output_columns`
- PASS: `expected_output_shape`
- PASS: `candidate_input_count_188`
- PASS: `label_unchanged`
- PASS: `split_unchanged`
- PASS: `source_table_id_unchanged`

## Usage Boundary

This table is a versioned candidate extension of V2 and does not replace or overwrite it. `sequence_context` passed a single-seed training-only grouped CV, but its formal model-input status still depends on the V2-1 multi-seed block-ablation layer.
