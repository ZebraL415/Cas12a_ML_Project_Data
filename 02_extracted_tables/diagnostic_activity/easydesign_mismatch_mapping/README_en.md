# EasyDesign Mismatch Source-Mapping Intermediate Tables

This directory stores traceable intermediate tables extracted from the EasyDesign combined supplementary workbook. They are not final training datasets.

- `EasyDesign_2024_TableS3_alignment_preserved_raw.csv`: original Table S3 training rows with `-` preserved in `target_at_guide`.
- `EasyDesign_2024_TableS2_template_groups_raw.csv`: 198 Table S2 templates with the 22 x 9 grouping, within-group roles, and length QC.
- `EasyDesign_2024_TableS2_TableS3_mapping_hits_raw.csv`: all exact or IUPAC-compatible Table S3-to-Table S2 window hits; tied hits are retained.

These mappings are for source traceability, grouping, and review only. They are not experimental labels and should not be default model features. Row-level cleaned outputs are stored in `03_cleaned_minimal/easydesign_mismatch/`.
