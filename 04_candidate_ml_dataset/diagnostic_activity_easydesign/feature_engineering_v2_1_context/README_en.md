# EasyDesign Feature Engineering v2.1 Context

This directory stores a versioned context extension without overwriting V2. Its parent is `EasyDesign_2024_diagnostic_activity_feature_table_v2.csv`.

## Files

- `EasyDesign_2024_diagnostic_activity_feature_table_v2_1_context.csv`: 11,992 rows × 246 columns; 188 parent columns plus 58 context features.
- `EasyDesign_2024_feature_dictionary_v2_1_context.csv`: complete feature and formula dictionary.
- `EasyDesign_2024_sequence_context_feature_dictionary_v2_1.csv`: dictionary for only the 58 new columns.
- `v2_1_final_feature_manifest.csv`: 188 nominal V2-1 model inputs and constant-filter status.
- `v2_1_context_build_qc.json` and `v2_1_context_independent_verification.json`: build and independent QC.
- `v2_1_context_build_report_zh.md` / `_en.md`: bilingual build reports.

## Usage

Use `v2_1_final_feature_manifest.csv` to define model inputs. Within each training fold, fit medians on training records only, fill residual missing values with zero, then remove columns constant in that training fold. Positional mismatch/gap features continue to use `target_aligned_25`; `sequence_context` uses only `crRNA_sequence` and `target_ungapped`.

V2-1 experimental evidence is in `/Users/linzibo/Cas12a_ML_Project_Expr/V2-1_feature_block_ablation/`. Do not merge this diagnostic-activity table with DeepCas12a `editing_activity`.

Chinese version: `README.md`.
