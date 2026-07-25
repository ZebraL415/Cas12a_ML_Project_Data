# V2-1 Final Three-Layer Experiment Summary

## Executive Conclusion

The final decision is to **promote `sequence_context` and freeze all five blocks, totaling 188 nominal inputs; fold-local constant removal leaves 183 active inputs in this run.** This decision is supported by both multi-seed target-grouped internal evidence and Table S5 external ranking evidence. The V2 gap-aware core remains an immutable parent version and comparator.

## Layer 1: Versioned Feature Table

- Built a `v2.1_context` candidate table with 11,992 rows and 246 columns.
- Added 58 `sequence_context` features, increasing candidate inputs from 130 to 188.
- New values use only `crRNA_sequence` and `target_ungapped`.
- `target_aligned_25`, positional mismatch/gap features, labels, provenance, splits, and row order were unchanged.
- Both QC passes succeeded, including exact preservation of all parent columns.

## Layer 2: Five-Block V2-1 Ablation

The experiment reused frozen five-fold target groups on 8,417 `baseline_train` records, with seeds 7, 21, 42, 84, and 2024, for 150 model fits. Neither the fixed validation split nor Table S5 was used for selection.

- Full 188-feature OOF Spearman: 0.736887 ± 0.000842.
- V2 core 130-feature OOF Spearman: 0.671385 ± 0.000752.
- Mean `sequence_context` gain: 0.065502; positive in 5/5 seeds.
- MAE improvement: 0.034527; RMSE improvement: 0.044689.

| Block                |   Removed |   Spearman loss |   MAE worsening | Rule result        |
|:---------------------|----------:|----------------:|----------------:|:-------------------|
| pair_alignment       |        11 |        0.010705 |        0.012050 | retained_important |
| pair_position        |        75 |        0.000415 |        0.000570 | retained_important |
| substitution_type    |        12 |        0.013076 |        0.006624 | retained_important |
| sequence_composition |        32 |        0.002152 |        0.000772 | retained_important |
| sequence_context     |        58 |        0.065502 |        0.034527 | retained_important |

`sequence_context` is the largest contributor; `pair_alignment` and `substitution_type` make moderate, stable contributions. `pair_position` and `sequence_composition` are retained by the preregistered rule, but their Spearman losses are only 0.000415 and 0.002152; these are marginal signals, not strong biological evidence. Block sizes differ substantially, so ablation deltas cannot be interpreted directly as per-feature importance.

## Layer 3: Table S5 External Validation

After feature freezing, models were trained on all 10,634 Table S3 development records and evaluated only on the 1,358 Table S5 records. Because label scales are not confirmed to match, only Spearman and Pearson are reported; cross-scale errors are omitted.

| variant       |   n_features |    n |   spearman_rho |   pearson_r |
|:--------------|-------------:|-----:|---------------:|------------:|
| core_v2       |          130 | 1358 |       0.401283 |    0.454384 |
| full_v2_1     |          188 | 1358 |       0.440410 |    0.505258 |
| selected_v2_1 |          188 | 1358 |       0.440410 |    0.505258 |

- Five-seed ensemble Spearman gain of full v2.1 over core v2: 0.039127.
- Positive in 5/5 seeds; mean per-seed gain: 0.038455.
- Full v2.1 Spearman is 0.571260 for virus and 0.264193 for bacteria, indicating uneven cross-type generalization.
- The 21 non-45-nt contexts are descriptive only and too small for a stable conclusion.

After V2 normalization, 10 Table S5 records share a 25-nt `target_ungapped` guide-local window with Table S3, representing four unique windows. This is not equivalent to overlap of the paper's full DNA template/target definition. Excluding these 10 records leaves a full-versus-core Spearman gain of 0.039263, so the promotion decision does not depend on them.

## Relation to Published Table S5 Prediction Columns

| published_prediction_column   |   n_missing_or_dash |    n |   spearman_rho |   pearson_r |
|:------------------------------|--------------------:|-----:|---------------:|------------:|
| CNND                          |                 499 |  859 |       0.620642 |    0.554645 |
| CNN12a                        |                 496 |  862 |       0.656868 |    0.600012 |
| CNN12ae                       |                   0 | 1358 |       0.812438 |    0.716092 |
| TransformerD                  |                 496 |  862 |       0.532478 |    0.476383 |
| Transformer12a                |                 496 |  862 |       0.541746 |    0.440071 |
| Transformer12ae               |                 496 |  862 |       0.467465 |    0.416919 |

The recomputed values align with the paper's evaluation layers: `CNN12a` is about 0.657 on its 862 nonmissing records, while `CNN12ae` is about 0.812 on all 1,358 augmented-test records. The current full v2.1 result of 0.440 improves its own core comparator but remains well below the authors' augmented system. Training augmentation, encoding/features, and evaluation coverage differ, so this is a gap reference rather than a like-for-like competition.

## Final Usage Rules

1. Use the 188 nominal inputs in `v2_1_final_feature_manifest.csv` for `selected_v2_1`; do not reselect them from Table S5 results.
2. Within each training fold, compute medians from training records only, fill residual missing values with zero, then remove features constant in that fold.
3. Positional mismatch/gap features must continue to use `target_aligned_25`; composition and context use ungapped sequences. Do not interchange these inputs.
4. Future model comparisons should keep target-grouped splits and report overall, virus/bacteria, and non-45-nt sensitivity results separately.

## Limitations

This experiment establishes stable predictive value for `sequence_context` under the frozen XGBoost workflow, not a causal role for any k-mer or GC feature. Lower bacteria performance, guide-local window overlap, and the Table S3/Table S5 scale difference remain subjects for future external validation.
