# Method Notes

Xu's engineered-feature script used the EasyDesign v0 feature table as input, computed guide-target Hamming distance under direct, complement, reverse, and reverse-complement target representations, and selected the representation with the highest exact agreement against the existing `guide_target_hamming_dist_computed` field. After selecting direct, it generated single-sequence composition, local-GC, k-mer, pairwise mismatch amount, position, and type features, together with orientation comparison, row audit, feature dictionary, and generation report outputs.

The full generated table was reconciled row by row to v0 using `record_id`, row order, sequences, split, and label. The project builder preserved every v0 field and selected 60 interpretable, non-label-leaking, non-exact-duplicate engineered features. Because some targets are shorter than their guide, unaligned position-specific mismatch cells were encoded as missing rather than as matched value zero. All generic-third region features were excluded because biological orientation was not independently confirmed.

The reference prediction file was used only to validate internal consistency of saved results. Metrics were recalculated from row-level `label_normalized` and `predicted_activity`; no model was fitted or trained in this run.
