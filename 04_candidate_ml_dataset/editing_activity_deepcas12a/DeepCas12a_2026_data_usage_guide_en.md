# DeepCas12a_2026 Data Usage Guide

## Recommended Entry Point

For the first DeepCas12a editing activity baseline, use:

`DeepCas12a_2026_editing_activity_feature_table_v0.csv`

## Default Task

- path_type: `editing_activity`
- task type: binary classification
- label column: `label_normalized`
- positive class: `1`, high AsCas12a on-target activity
- negative class: `0`, low AsCas12a on-target activity
- main input sequence: `target_context_sequence`
- PAM: `pam_sequence`, inferred from positions 5-8 of the 34 bp sequence
- protospacer: `protospacer_sequence`, inferred from positions 9-31

## PAM Note

All candidate rows have a `TTTN` `pam_sequence`. Among them, 4,500 rows are `TTTT`, which does not satisfy strict `TTTV`; this round does not remove those rows and marks them with `pam_matches_TTTV` in the feature table.

## Recommended Split

- Training: `default_split == baseline_train`
- HT1 holdout test: `default_split == holdout_test_HT1-2`
- Independent tests: `default_split == independent_test_HT2` and `default_split == independent_test_HT3`
- Internal 9-fold validation: use `DeepCas12a_2026_9fold_partitions_v0.csv`

## Do Not

- Do not merge with EasyDesign fluorescence/RFU diagnostic activity labels.
- Do not treat `label` as a continuous indel frequency.
- Do not interpret HT standardized epigenetic features as true methylation/DNase states at unknown integration loci.
- Do not filter `TTTT` PAM rows before making an explicit methodological decision.
