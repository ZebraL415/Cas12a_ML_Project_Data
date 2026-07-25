# Feature Table V3

This directory contains the canonical V3 candidate features for EasyDesign diagnostic activity.

- `EasyDesign_2024_diagnostic_activity_feature_table_v3.csv`: 11,992 x 250; inherits V2.1 and adds four thermodynamic proxies. The formal 192 features are listed in the block manifest.
- `EasyDesign_2024_diagnostic_activity_feature_table_v3_nonpositional4_candidate.csv`: retains metadata/labels and the alignment, substitution, context, and thermodynamic blocks, giving 85 candidate features.
- `EasyDesign_2024_feature_dictionary_v3.csv`: definitions, formulas, input sequences, and limitations.
- `EasyDesign_2024_feature_block_manifest_v3.csv`: formal six-block candidate list; modeling code must select features from this file.
- `EasyDesign_2024_nonpositional4_feature_manifest_v3.csv`: non-position four-block candidate list.
- `EasyDesign_2024_feature_table_v3_qc.json`: inheritance, missingness, uniqueness, and summary checks.
- `v3_output_manifest.json`: output paths, sizes, and SHA-256 hashes.

`nonpositional4` describes table structure only. It does not mean that all four blocks are high-impact; the thermodynamic block has not been formally promoted.
