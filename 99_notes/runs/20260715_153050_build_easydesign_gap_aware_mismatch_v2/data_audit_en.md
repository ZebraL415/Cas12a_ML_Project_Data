# EasyDesign Gap-Aware v2 Data Audit

## Scope

This run processes only EasyDesign_2024 `diagnostic_activity`. It reads the original paper, official repository, combined supplementary workbook, existing v0, and prior audit records. It does not modify `01_raw/`, train a model, or merge another label system.

## Confirmed Facts

- Combined-workbook Table S2 contains 198 templates that form 22 nine-template groups.
- Table S3 contains 10,634 experimentally measured records with no missing `30 min` labels.
- Every guide and `target_at_guide` alignment representation has length 25.
- 9,894 targets contain no `-`; 740 contain `-`, with ungapped lengths of 17, 18, 23, or 24.
- In all 740 gap records, the alignment representation places gaps in the target channel; no `-` occurs in the guide channel.
- Raw `guide_target_hamming_dist` agrees with the 25-position aligned difference count in 10,446 rows and disagrees in 188 rows.
- Public-repository `predict_activity.py` has the same SHA-256 as the local raw mirror.

## Preliminary Inferences

- Table S2 group members 8/9 can be interpreted as insertion/deletion templates based on the paper order and length pattern; this is a structural inference, not a Table S3 row-level experimental ID.
- Exact/IUPAC-compatible windows for 10,633 Table S3 records can provide source-mapping candidates; multiple-template or multiple-group hits cannot be promoted automatically to unique truth.
- The 188 raw-Hamming anomalies make that field unsuitable as a default training feature. It may reflect unpublished preprocessing logic, but current evidence is insufficient.

## Data-Quality Tiers

- `eligible_core_v2`: 9,894 no-gap Table S3 rows.
- `conditional_gap_aware_v2`: 740 gap-preserving Table S3 rows.
- `external_test_only_scale_unconfirmed`: 1,358 Table S5 rows.
- Mapping high/medium/review: 7,421 / 3,146 / 67.
- The only record without an exact or IUPAC-compatible mapping is `EasyDesign_2024_TableS3_09121`.

## Highest-Priority Follow-Up Records

- The 188 raw-Hamming disagreement records.
- The 67 mapping-review records, including 50 multiple-group, 16 IUPAC-compatible, and 1 unmapped record.
- The 740 gap records, especially the six multi-gap records with ungapped lengths 17/18.
- Non-45-nt Table S5 contexts and the Table S3/Table S5 label-scale issue.
