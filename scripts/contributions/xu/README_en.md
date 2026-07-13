# Xu Contribution Files

This directory preserves the original engineered-feature generator supplied by Xu. The received file content is unchanged.

- `generate_validated_engineered_features.py`
- Original received path: `/Users/linzibo/Documents/generate_validated_engineered_features.py`
- SHA-256: `cf8cd2f62eb8759e8fa311892bb8791425d2dec5c1b90e3df94d48e95e1a1830`

The script reads the EasyDesign feature table, compares direct, complement, reverse, and reverse-complement representations, selects the mode that best reproduces the existing computed Hamming column, and produces 139 engineered features plus QC files.

Boundary: this validates consistency with an existing project-derived column, not biological strand orientation independently. The script encodes unaligned positions as `0`; the final v1 builder changes those cells to missing and applies redundancy-aware selection. Do not edit the contributor original in place. Put project-side improvements in a separate script.
