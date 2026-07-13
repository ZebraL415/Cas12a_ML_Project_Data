# Baseline Data Usage Guide

## Recommended Entry Point

- Default file: `EasyDesign_2024_diagnostic_activity_feature_table_v1.csv`, with 11,992 rows and 89 columns.
- Basic comparison file: `EasyDesign_2024_diagnostic_activity_feature_table_v0.csv`.
- v1 preserves every v0 provenance, sequence, label, and split field and adds 60 audited engineered features.
- The full 139-feature output is under `feature_engineering/full_generated/`. It is retained for tracing, recomputation, and further research, not as the default training table.

## Training And Validation Scope

- Use only rows with `label_is_primary_baseline == yes` and `label_scale_group == table_s3_log_or_transformed_30min_activity`.
- Training set: `baseline_split == baseline_train`, 8,417 rows.
- Validation set: `baseline_split == baseline_validation`, 2,217 rows.
- Label: `label_normalized`, representing the experimentally measured Table S3 30-minute diagnostic-activity readout.
- Do not redraw the current split. The hash rule already assigns every shared target sequence to one split.

## Default Model Inputs

Candidate numeric model features include:

- v0 basic features: `crRNA_length`, `target_length`, `crRNA_GC_content`, `target_GC_content`, and `guide_target_hamming_dist_computed`.
- v1 pairwise features: `mismatch_count_shared_positions`, `mismatch_fraction_shared_positions`, first/last mismatch positions, longest match/mismatch runs, and GC difference.
- v1 positional features: `mismatch_pos_1` through `mismatch_pos_25`.
- v1 mismatch types: all 12 `mismatch_type_*` counts.
- v1 sequence features: entropy, homopolymer length, local GC, and a small importance-supported k-mer subset.

See `feature_engineering/EasyDesign_2024_feature_selection_manifest_v1.csv` for the full selection evidence.

## Fields That Must Be Excluded

Do not pass these fields to a model:

- Identifiers and provenance: `dataset_id`, `feature_table_version`, `source_id`, `source_table_id`, `record_id`, `paper_split`, `baseline_split`, and `data_role`.
- Raw sequences and notes: `crRNA_sequence`, `target_sequence`, `target_context_sequence`, and `notes`; process sequences separately only when using a dedicated sequence encoder.
- All label fields and label metadata: `label_raw_name`, `label_raw_value`, `label_normalized`, `label_scale_group`, and `label_is_primary_baseline`.
- `guide_target_hamming_dist_raw`: its source meaning remains unresolved, so it must not be a default input even though the first-run importance was high.
- `pam` and `pam_type`: PAM is currently inferred from a 5-prime TTTN prefix rather than an independent raw column; exclude it until the sequence convention is confirmed.
- `has_valid_DNA_alphabet` and `contains_ambiguous_base`: these are constant QC fields in the primary baseline and carry no useful variation.

## Missing Values And Orientation Boundary

- In Table S3, 740 targets are shorter than 25 nt. v1 writes unaligned `mismatch_pos_*` cells as missing; missing must not be interpreted as a match.
- Models with native missing-value support may keep these cells missing. Other models should use a distinct state such as `-1` while retaining `target_length`, or add explicit alignment indicators.
- The `direct` orientation computationally reproduces the existing Hamming column but is not independently confirmed biologically. Do not rename generic thirds as PAM-proximal, seed, or distal regions.

## Not Used By Default

- `baseline_split == external_test_scale_unconfirmed`: 1,358 Table S5 rows whose label scale is not yet aligned with Table S3.
- `EasyDesign_2024_diagnostic_activity_augmented_optional_v0.csv`: Table S4 augmentation, used only when explicitly enabled.
- `paper_prediction_*`: paper-model predictions, not experimental labels.
- Predictions and importance files under `evaluation/`: audit and method references only; they do not replace reproducible training code.

## Recommended First Comparison

1. Run a control with the five v0 basic numeric features.
2. Run an enhanced comparison with the selected v1 engineered features while keeping the same split and metrics.
3. Report at least Spearman, Pearson, MAE, RMSE, and R2, and save row-level predictions.
4. Do not present the reference improved result as final project performance until its training code has been independently reproduced.
