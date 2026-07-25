# Reproducible Scripts

This directory stores data-audit, extraction, cleaning, candidate-table build, and verification code. Scripts may read `01_raw/` but must never modify, rename, or overwrite raw files.

## EasyDesign

- `inspect_easy_design.py`: first-round workbook/sheet audit.
- `resolve_easy_design_round2.py`: paper-informed baseline v0 build.
- `build_easydesign_alignment_v2.py`: gap-preserving alignment and Table S2 provenance mapping.
- `build_easydesign_feature_table_v2.py`: gap-aware feature table v2, dictionary, and QC.
- `verify_easydesign_v2.py`: independent V2 verification.
- `build_v2_1_context_feature_table.py`: builds 58 v2.1 context features only from `crRNA_sequence` and `target_ungapped`, without overwriting V2.
- `verify_v2_1_context_feature_table.py`: independently checks v2.1 dimensions, parent preservation, gap/label/split integrity, and numeric ranges.
- `audit_vertical3_delta_g.py`: independently reproduces and audits the submitted Vertical3 columns with ViennaRNA 2.7.2.
- `build_easy_design_feature_table_v3.py`: builds the four corrected thermodynamic proxies, V3 table, dictionary, block manifests, and QC from canonical V2.1.

The frozen V2.1 configuration and complete build run are in `/Users/linzibo/Cas12a_ML_Project_Expr/V2-0_unified_baseline/`; complete V3 Package1 experiment code and results are in `/Users/linzibo/Cas12a_ML_Project/`. Every execution should use a new timestamped directory and record input, configuration, fold, and script SHA-256 values.

Chinese version: `README.md`.
