# Current Paper Data Notes

## EasyDesign_2024

- Paper: Huang et al., *Deep learning enhancing guide RNA design for CRISPR Cas12a-based diagnostics*, iMeta 2024, DOI `10.1002/imt2.214`.
- Data path: `diagnostic_activity`; the primary experimental label is Table S3 `30 min` fluorescence activity.
- The methods describe 22 original DNA templates, each with six substitution, one insertion, and one deletion variant, for 198 Table S2 templates.
- Insertions/deletions use `-` as an alignment placeholder in target DNA or crRNA, forming a five-state one-hot encoding with A/C/T/G; target+guide at each position is 10-dimensional.
- Public repository: `https://github.com/scRNA-Compt/EasyDesign`; main/dev/visible history at commit `5c06a30d0a43be28a958831587f6ab706c2d4876` was inspected, and no training preprocessing generator for `target_at_guide` or `guide_target_hamming_dist` was found.
- The paper documents two negative wells, two duplicate positive wells, and normalization per 96-well plate, but publishes no row-level plate/well/template/replicate map.
- v2 preserves the 25-position alignment for 10,634 Table S3 records, including 740 target-channel gap rows; the first baseline is recommended on 9,894 no-gap rows.
- Table S2 sequence-evidence mapping covers 10,633 rows, but mapping is audit metadata, not an experimental label or default model input.

## DeepCas12a_2026

- Data path: `editing_activity`.
- The label is binary AsCas12a editing activity, not fluorescence/RFU, and is not merged with EasyDesign.
