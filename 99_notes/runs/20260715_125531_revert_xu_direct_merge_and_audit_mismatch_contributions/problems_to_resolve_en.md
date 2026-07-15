# Current Problems To Resolve

This file records questions that still require manual confirmation, grouped by data source.

## EasyDesign_2024

### Resolved
- `30 min`: the PDF methods confirm that the 30-minute fluorescence value was selected as the activity indicator; this round uses it as the primary label for the Table S3 internal baseline.
- `20 min normalized`: the PDF confirms that it is a derived/augmented label from the 20-minute readout normalized to 30 minutes; it is not merged into the primary label.
- `out_logk_measurement`: it belongs to the Table S4 augmented dataset; this round stores it separately as optional augmentation and excludes it from the default baseline.
- `true value`: it belongs to the Table S5 test dataset as the experimental true value; it is retained as an external paper test label, but its numeric scale versus Table S3 still needs confirmation.
- Standalone workbook versus combined source-data workbook: the combined workbook is used as the authoritative source, while standalone tables are treated as duplicate sources.
- Figure source data: retained as evidence or metadata, not used directly as tidy crRNA-target training rows.
- `guide-expected-activities` and model columns: all are classified as predicted scores, not primary training labels.
- PAM: the PDF supports a TTTN PAM; Excel has no separate PAM column, so this round only infers a 5-prime TTTN prefix and marks it as inferred.
- Fig.S3: it is aggregate figure source data about sequence/activity features and is not used as row-level training labels.

### Still Needs Confirmation
- Whether the negative `30 min` labels in Table S3 and the positive `true value` labels in Table S5 can be mapped to one shared scale remains unresolved and needs either user confirmation or a methodological decision.
- Raw Table S3 `guide_target_hamming_dist` agrees with direct counting on the 25-position, `-`-preserving character alignment at 98.232%, but 188 rows representing 28 unique pairs remain inconsistent. The field likely represents an aligned distance for most rows, but anomalies still require row-level review and the field must not be a default training feature.
- Excel has no explicit separate PAM column; the current PAM value is inferred only from the TTTN prefix and should be confirmed before use as a model feature.
- A small number of Table S5 DNA contexts are not 45 nt; those rows use a best-match fallback to locate the target window and should be manually reviewed later.
- Whether Table S4 augmentation should enter the first formal training workflow should be decided after the model plan is selected.
- Table S3 contains only type1/type2 and no exact pathogen names; species-level grouping validation needs an additional mapping.
- Table S3 contains 740 `target_at_guide` rows with `-`. Model input code and paper methods must confirm gap-event direction before gap-aware mismatch features are generated; until then, Xu position features calculated after deleting gaps must not be used.
- Among Lin's Table S2 scan results, 642 crosslinked unique pairs map to multiple templates. Every tied hit needs to be retained with `mapping_status`; the earliest hit must not be treated as the unique source.
- Project standalone `Table S2.xlsx` actually contains Training/Augment/Test sheets, while `Table S3.xlsx` contains DNA/crRNA for four pathogens. Raw files remain unchanged, but catalog descriptions need correction based on actual content.

<!-- BEGIN DeepCas12a_2026 -->
## DeepCas12a_2026

### Confirmed

- DeepCas12a belongs to `editing_activity`, not `diagnostic_activity`.
- `label` is a binary AsCas12a on-target activity label and must not be treated as fluorescence/RFU.
- The 34 bp `sequence` is a target-context sequence containing upstream context, PAM, protospacer, and downstream context.
- The HT methylation/DNase features are standardized model inputs according to the repository documentation and should not be interpreted as true epigenetic states at unknown integration loci.
- All candidate rows have a `TTTN` PAM; 4,500 rows are `TTTT`, which does not satisfy strict `TTTV`, and this round retains and marks them.

### Still Needs Confirmation

- The repository provides model-ready binary labels only; continuous indel frequencies require tracing back to the original Kim et al. values.
- PAM/protospacer can be inferred from the 34 bp target-context sequence, but there is no independent crRNA sequence; crRNA derivation requires strand and complement-rule confirmation.
- HEK in situ A/N epigenetic feature calls should be discussed separately from HT standardized features in downstream model interpretation.
- Whether formal modeling should treat `TTTT` PAMs as non-canonical PAM features, stratify them separately, or retain them as ordinary inputs should be decided after the model plan is selected.
<!-- END DeepCas12a_2026 -->
