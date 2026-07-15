# Problems Remaining at the End of This Run

1. No training-preprocessing code generating `target_at_guide` and `guide_target_hamming_dist` was found in the official public repository main, dev, or visible history; any unpublished author script still needs to be obtained.
2. No authoritative mapping from Table S3 `No.` to Table S2 `Template No.`, plate/well, experimental replicate, or synthesized-template ID was found.
3. `-` is confirmed as an alignment gap in the five-state target/crRNA encoding, but row-level biological insertion/deletion direction cannot be established from Table S3 alone.
4. The official predictor assigns a one-hot index to `-`, but `FASTA_CODES`, which is queried by `onehot()`, does not include `-`; the actual runtime or training version needs author confirmation.
5. Raw Hamming disagrees with direct aligned counting in 188 rows and must not be a default feature.
6. Sixty-seven source mappings are in review; `EasyDesign_2024_TableS3_09121` has no exact or IUPAC-compatible hit.
7. The scale conversion between Table S3 `30 min` and Table S5 `true value` remains unresolved.
8. A few Table S5 DNA contexts are not 45 nt; their target windows still need manual review.
9. Whether Table S4 augmentation enters formal training should be decided after the model plan is selected.
10. Table S3 lacks exact pathogen names; species-group validation needs an additional authoritative mapping.
