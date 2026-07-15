# EasyDesign 2024 v2 Data Usage Guide

## 1. Scope

This guide supports a baseline workflow before the model family is selected. The data belong to `diagnostic_activity`; the label is experimentally measured Cas12a fluorescence activity and must not be merged with DeepCas12a binary `editing_activity`.

Main file: `EasyDesign_2024_diagnostic_activity_feature_table_v2.csv`. It has 11,992 rows and 188 columns: 10,634 Table S3 rows and 1,358 Table S5 rows. v2 adds, removes, or rewrites no labels and does not change the v0 `baseline_split`.

## 2. Recommended First Baseline

Select only these records:

```text
default_training_eligibility == eligible_core_v2
baseline_split in {baseline_train, baseline_validation}
label_is_primary_baseline == yes
```

This yields 9,894 no-gap Table S3 records: 7,832 training rows and 2,062 validation rows. Use `label_normalized` as the label. Identical `guide_target_pair_id` values do not cross the training/validation boundary.

For the first run, select numeric columns marked `default_model_role == candidate_input` in the feature dictionary. To remain model-agnostic, begin with:

- Pair level: `aligned_difference_count`, `substitution_count`, PAM/spacer difference counts, first/last difference positions, and longest consecutive match/substitution runs.
- Position level: `difference_pos_01..25` and `substitution_pos_01..25`.
- Composition: GC content, base fractions, Shannon entropy, and longest homopolymer for guide, target, guide spacer, and target spacer.

Do not use `label_*`, `paper_prediction_*`, `mapping_*`, `source_*`, `record_id`, `guide_target_hamming_dist_raw`, or `guide_target_hamming_dist_computed_v0_legacy` as default inputs.

## 3. Gap-Aware Second Stage

After the no-gap baseline runs successfully, add this stratum separately:

```text
default_training_eligibility == conditional_gap_aware_v2
```

This layer contains 740 records: 585 training rows and 155 validation rows. The model must explicitly support `target_gap_pos_01..25`; it must not use old position features shifted after deleting `-`. Report no-gap and gap performance separately and compare a no-gap-only run against a gap-inclusive ablation.

`gap_in_target` is an alignment-channel name, not a confirmed biological deletion direction. Preserve this limitation when interpreting indel types.

## 4. Table S5 External Test

The 1,358 rows with `default_training_eligibility == external_test_only_scale_unconfirmed` come from Table S5. They are paper external-test candidates only and must not enter training. The scale relationship between Table S5 `true value` and Table S3 `30 min` remains unresolved, so cross-table comparisons require a separate scaling decision.

## 5. Using Source Mapping

- `mapping_confidence == high`: 7,421 Table S3 records have a unique exact template window.
- `mapping_confidence == medium`: 3,146 records have multiple template hits within one template group.
- `mapping_confidence == review`: 67 records involve multiple groups, IUPAC-compatible matching, or no mapping.

Mapping fields are appropriate for source audit, template-group validation, and sensitivity analysis, but not as default model inputs. For the strictest source subset, additionally filter `mapping_confidence == high` and report the resulting sample-size change.

## 6. Minimal Loading Example

```python
import pandas as pd

data = pd.read_csv(
    "EasyDesign_2024_diagnostic_activity_feature_table_v2.csv",
    low_memory=False,
)
dictionary = pd.read_csv(
    "feature_engineering_v2/EasyDesign_2024_feature_dictionary_v2.csv"
)

core = data.query("default_training_eligibility == 'eligible_core_v2'")
train = core.query("baseline_split == 'baseline_train'")
valid = core.query("baseline_split == 'baseline_validation'")

feature_names = dictionary.loc[
    dictionary["default_model_role"].eq("candidate_input"), "feature_name"
].tolist()
feature_names = [name for name in feature_names if name in data.columns]

X_train = train[feature_names]
y_train = train["label_normalized"]
X_valid = valid[feature_names]
y_valid = valid["label_normalized"]
```

This example performs safe data selection only. It does not define missing-value handling, scaling, model selection, tuning, or training.

## 7. Reporting Requirements

For each modeling run, record the data-file SHA-256, filters, feature list, training/validation row counts, random seed, and software versions. Report no-gap, gap, and high/medium/review mapping strata separately so source ambiguity and indel-handling differences are not hidden in aggregate metrics.
