# EasyDesign 2024 Feature Table v2 Build Report

## Inputs and Boundaries

v2 uses Table S2/Table S3 from the combined supplementary workbook, the existing feature table v0, the original paper PDF, and the official GitHub repository as input evidence. `01_raw/` was not modified; no model was trained, Table S4 augmentation was not included, and Table S5 and Table S3 labels were not forced onto one scale.

## Build Results

- v2 main table: 11,992 rows and 188 columns.
- Table S3: 10,634 rows, including 9,894 no-gap rows and 740 rows with target-channel gaps.
- Table S5: 1,358 rows retained only as scale-unconfirmed external-test candidates.
- Labels, `source_table_id`, and `baseline_split` match v0 row by row.
- Feature dictionary: 145 rows.
- Table S2: 198 templates fully grouped into the paper-supported 22 x 9 structure; every group's length pattern passes automated QC.
- Source mapping: 10,633/10,634 Table S3 records have exact or IUPAC-compatible candidates, with 7,421 high, 3,146 medium, and 67 review records.

## Relationship to v0

v0 remains as a compatibility version. v2 adds `target_aligned_25` with `-` preserved, retains the old Hamming value as `guide_target_hamming_dist_computed_v0_legacy`, and recomputes `guide_target_hamming_dist_computed` using the direct 25-position alignment. All 9,894 no-gap rows agree between old and new calculations; only 33 of 740 gap rows agree, so v0 gap-position features must not be used for default training.

## Row Handling

No v0 row was deleted. Table S3 rows are divided into 9,894 `eligible_core_v2` and 740 `conditional_gap_aware_v2` records; Table S5 rows are marked as 1,358 `external_test_only_scale_unconfirmed` records. No unlabeled Table S2 scan result was added to experimental training data.

## Remaining Limitations

The public author materials provide no authoritative Table S3-row-to-Template No./plate/replicate correspondence, and no training preprocessing script generating `target_at_guide` or `guide_target_hamming_dist` was found. The v2 Table S2 mapping is therefore sequence-evidence mapping, not an author-provided experimental key. `gap_in_target` is also a representational event and cannot by itself establish the biological insertion/deletion direction.
