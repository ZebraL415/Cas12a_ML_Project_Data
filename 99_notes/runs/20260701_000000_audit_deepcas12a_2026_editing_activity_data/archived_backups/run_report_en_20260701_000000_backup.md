# Run Report: Audit DeepCas12a 2026 editing activity data

## Scope

Data source: `01_raw/DeepCas12a_2026`; paper PDF: `/Users/linzibo/Downloads/s12864-026-13003-3_reference.pdf`.

## Inputs

- Local DeepCas12a GitHub copy: `01_raw/DeepCas12a_2026`
- Paper PDF: `/Users/linzibo/Downloads/s12864-026-13003-3_reference.pdf`
- Key documentation read: `README.md`, `Dataset/README.md`, `Dataset/Data_Descriptions.txt`, `splits/README.md`, `scripts/README.md`

## Outputs

- `02_extracted_tables/editing_activity/DeepCas12a_2026_HT1_1_train_editing_activity_binary_raw.csv`
- `02_extracted_tables/editing_activity/DeepCas12a_2026_HT1_2_test_editing_activity_binary_raw.csv`
- `02_extracted_tables/editing_activity/DeepCas12a_2026_HT2_test_editing_activity_binary_raw.csv`
- `02_extracted_tables/editing_activity/DeepCas12a_2026_HT3_test_editing_activity_binary_raw.csv`
- `02_extracted_tables/editing_activity/DeepCas12a_2026_HEKplasmid_in_situ_editing_activity_binary_raw.csv`
- `02_extracted_tables/editing_activity/DeepCas12a_2026_HEK_lenti_in_situ_editing_activity_binary_raw.csv`
- `02_extracted_tables/editing_activity/DeepCas12a_2026_train_HT1_1_plus_HEK_in_situ_editing_activity_binary_raw.csv`
- `02_extracted_tables/editing_activity/DeepCas12a_2026_ht1_train_test_split_split_metadata_raw.csv`
- `02_extracted_tables/editing_activity/DeepCas12a_2026_deepcas12a_9fold_partitions_split_metadata_raw.csv`
- `04_candidate_ml_dataset/editing_activity_deepcas12a/DeepCas12a_2026_editing_activity_binary_v0.csv`
- `04_candidate_ml_dataset/editing_activity_deepcas12a/DeepCas12a_2026_editing_activity_feature_table_v0.csv`
- `03_cleaned_minimal/editing_activity_minimal.csv`
- `04_candidate_ml_dataset/editing_activity_deepcas12a/DeepCas12a_2026_9fold_partitions_v0.csv`
- `04_candidate_ml_dataset/editing_activity_deepcas12a/DeepCas12a_2026_ht1_train_test_split_v0.csv`

## Classification Decisions

- path_type: `editing_activity`
- record unit: 34 bp AsCas12a target-context record
- label: `label`, binary high/low AsCas12a on-target activity
- label_status: `measured`, but represented as a binary label thresholded from measured indel frequency
- priority: high

## Data Quality Checks

- candidate v0 rows: 20709
- feature table rows: 20709
- candidate label counts: {"0": 12439, "1": 8270}
- bad sequence length rows: 0
- bad DNA alphabet rows: 0
- bad methylation length rows: 0
- bad DNase length rows: 0
- Rows not matching strict `TTTV` PAM: 4500; all are `TTTT`, still matching `TTTN`, and this round retains and marks them
- duplicate candidate key rows: 0

## Next Recommended Actions

- For a DeepCas12a-route baseline, use only the data inside `editing_activity_deepcas12a/`.
- Do not merge this source with EasyDesign `diagnostic_activity` fluorescence/RFU labels.
- If a continuous editing-efficiency regression label is needed later, trace back to the original Kim et al. indel-frequency data rather than using this repository's thresholded `label`.
