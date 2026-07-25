# Current Problems To Resolve

This file records questions that still require manual confirmation, grouped by data source.

## EasyDesign_2024

### Resolved

- `30 min`: the methods confirm that 30-minute fluorescence was used for activity assessment; it is the primary Table S3 internal-baseline label.
- `20 min normalized`: the paper confirms that it is a derived label from the 20-minute readout normalized to 30 minutes; it is not merged into the primary label.
- `out_logk_measurement`: it belongs to Table S4 augmentation; it is stored separately and excluded from the default baseline.
- `true value`: it is the Table S5 experimental truth; it remains an external paper test label with an unresolved scale.
- PAM: the paper supports TTTN; Excel has no separate PAM column, so PAM is inferred only from the 5-prime TTTN prefix and marked as inferred.
- The actual sheet contents of standalone workbooks and the combined workbook are indexed; the combined workbook remains authoritative.
- The 198 Table S2 templates can be rebuilt into a paper- and length-supported 22 x 9 structure: original, six substitutions, one insertion, and one deletion.
- `-` is confirmed as the common alignment-gap placeholder in the five-state target/crRNA one-hot encoding; it must not be deleted before calculating position features.
- A Table S2 source mapping retaining every tied hit now exists: 10,633/10,634 records have candidates and are tiered as high/medium/review.
- A gap-aware feature table v2 now exists; v0 labels, source tables, and splits are unchanged, and the no-gap subset supports the first baseline.

### Still Needs Confirmation

- Whether Table S3 `30 min` and Table S5 `true value` have a reproducible transformation onto one scale.
- Raw `guide_target_hamming_dist` disagrees with direct 25-position aligned counting in 188 rows; this source column must not be a default training feature.
- No training preprocessing code generating `target_at_guide`/`guide_target_hamming_dist` was found in the official public main, dev, or visible history; an unpublished author version or written explanation is still needed.
- No authoritative mapping from Table S3 `No.` to Table S2 `Template No.`, plate/well, experimental replicate, or crRNA-template pairing was found.
- The alignment meaning of `-` is confirmed, but the biological insertion/deletion direction of each record cannot be established from a target-channel `-` alone; v2 `gap_in_target` denotes only alignment state.
- The official predictor assigns a one-hot index to `-`, but `FASTA_CODES`, which is queried by `onehot()`, does not contain `-`; the actual training/runtime version needs author confirmation.
- Sixty-seven mappings are in review: 50 cross multiple template groups, 16 are IUPAC-compatible only, and `EasyDesign_2024_TableS3_09121` is unmapped.
- A few Table S5 DNA contexts are not 45 nt; their target windows still need manual review.
- Whether Table S4 augmentation enters formal training should be decided after the model plan is selected.
- Table S3 has type1/type2 but no exact pathogen names; species-group validation needs an additional authoritative mapping.

### Feature Table V3 / Package1 Remaining Questions

- The source data lack the complete crRNA direct repeat; `thermo_guide_spacer_unfolding_ensemble_rna_proxy_kcal_mol` can represent only a local 21-nt spacer-unfolding proxy.
- Each Table S3 record is not yet uniquely mapped to its full DNA template and RPA-product context; the local dsDNA-separation proxy cannot replace experimental template free energy.
- ViennaRNA `RNAduplex` full/seed hybrid columns are RNA-RNA proxies and omit RNA-DNA-specific parameters, Cas12a protein effects, and R-loop conformational changes.
- In P1-1, the thermodynamic block adds only `+0.000732` mean OOF Spearman and is positive in 3/5 seeds, failing formal promotion; further optimization requires a separate controlled experiment.
- Removing the 75-dimensional pair-position block slightly improves Spearman but slightly worsens MAE; a compact position encoding must be compared under fixed P1-0 conditions.

<!-- BEGIN DeepCas12a_2026 -->
## DeepCas12a_2026

### Confirmed

- DeepCas12a belongs to `editing_activity`, not `diagnostic_activity`.
- `label` is a binary AsCas12a on-target activity label and must not be treated as fluorescence/RFU.
- The 34 bp `sequence` is a target-context sequence containing upstream context, PAM, protospacer, and downstream context.
- HT methylation/DNase features are standardized model inputs according to the repository and should not be interpreted as true epigenetic states at unknown integration loci.
- All candidate PAMs are `TTTN`; 4,500 rows are `TTTT`, which does not satisfy strict `TTTV`, and they are retained and marked.

### Still Needs Confirmation

- The repository provides model-ready binary labels only; continuous indel frequencies require tracing back to original Kim et al. values.
- PAM/protospacer can be inferred from the 34 bp context, but there is no independent crRNA sequence; crRNA generation needs strand and complement-rule confirmation.
- HEK in situ A/N epigenetic feature calls should be interpreted separately from HT standardized features.
- Formal handling of `TTTT` PAMs should be decided after the model plan is selected.
<!-- END DeepCas12a_2026 -->
