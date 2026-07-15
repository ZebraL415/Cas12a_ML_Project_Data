# EasyDesign Gap-Aware Minimally Cleaned Tables

This directory stores the EasyDesign Table S3 alignment and source mapping rebuilt from the authoritative combined workbook.

- `EasyDesign_2024_guide_target_alignment_v2.csv`: 10,634 Table S3 experimental records with the 25-position `target_aligned_25`, ungapped `target_ungapped`, position events, and source labels.
- `EasyDesign_2024_source_mapping_v1.csv`: source-mapping status, confidence tier, and candidate-template summary for each record.
- `EasyDesign_2024_mismatch_qc_v2.csv`: review queue for gap rows, raw Hamming disagreements, or non-high source mappings.

`gap_in_target` only means that the target channel contains `-` at that Table S3 alignment position; it does not establish the biological deletion direction. The default baseline uses `alignment_qc_status == pass_no_gap`; gap rows may enter only a gap-aware workflow conditionally.
