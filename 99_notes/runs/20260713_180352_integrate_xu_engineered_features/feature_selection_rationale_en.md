# v1 Feature Selection Rationale

## Inclusion Principle

v1 is a model-agnostic candidate feature table rather than a mechanical top-N cut from one XGBoost run. A feature must be deterministically recomputable from sequence, independent of predictions and label-derived values, interpretable, not exactly duplicated by an existing field, and supported by reference importance or complete feature-family logic.

## The 60 Included Engineered Features

- Seven pairwise features: shared-position mismatch count/fraction, first/last mismatch positions, longest match/mismatch runs, and GC difference.
- Twenty-five positional features: `mismatch_pos_1` through `mismatch_pos_25`, retained as a complete family instead of selecting only positions 2 and 4 from one run.
- Twelve mismatch-type counts: every directional non-identical A/C/G/T pair.
- Sixteen sequence features: guide/target entropy, homopolymer length, local GC, and TTT, AAA, GA, GT, and AG k-mers supported by the reference top 30.

## Main Exclusions

- `mismatch_count_validated`: 100% duplicate of `guide_target_hamming_dist_computed`.
- `match_fraction_shared_positions`: exact complement of mismatch fraction.
- Engineered length/GC: duplicate of v0 length and GC fields.
- `aligned_length` exactly equals `target_length`, while `length_difference` is exactly derivable from existing lengths.
- Generic thirds: cannot be renamed as biological proximal/middle/distal regions under current evidence.
- Positions 26 through 30: exceed the dataset's maximum 25-nt alignment.
- The remaining full k-mer set: recomputable but substantially expands table width without enough current reference importance to justify inclusion in compact v1.
- `guide_target_hamming_dist_raw`: retained for traceability but excluded from default modeling because its source meaning remains unresolved.

See `04_candidate_ml_dataset/diagnostic_activity_easydesign/feature_engineering/EasyDesign_2024_feature_selection_manifest_v1.csv` for per-column decisions.
