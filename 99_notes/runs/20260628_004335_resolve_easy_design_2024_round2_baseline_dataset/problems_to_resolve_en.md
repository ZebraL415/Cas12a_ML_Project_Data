# Problems To Resolve EasyDesign_2024 Round 2

## Resolved
- `30 min`: the PDF methods confirm that the 30-minute fluorescence value was selected as the activity indicator; this round uses it as the primary label for the Table S3 internal baseline.
- `20 min normalized`: the PDF confirms that it is a derived/augmented label from the 20-minute readout normalized to 30 minutes; it is not merged into the primary label.
- `out_logk_measurement`: it belongs to the Table S4 augmented dataset; this round stores it separately as optional augmentation and excludes it from the default baseline.
- `true value`: it belongs to the Table S5 test dataset as the experimental true value; it is retained as an external paper test label, but its numeric scale versus Table S3 still needs confirmation.
- Standalone workbook versus combined source-data workbook: the combined workbook is used as the authoritative source, while standalone tables are treated as duplicate sources.
- Figure source data: retained as evidence or metadata, not used directly as tidy crRNA-target training rows.
- `guide-expected-activities` and model columns: all are classified as predicted scores, not primary training labels.
- PAM: the PDF supports a TTTN PAM; Excel has no separate PAM column, so this round only infers a 5-prime TTTN prefix and marks it as inferred.
- Fig.S3: it is aggregate figure source data about sequence/activity features and is not used as row-level training labels.

## Still Needs Confirmation
- Whether the negative `30 min` labels in Table S3 and the positive `true value` labels in Table S5 can be mapped to one shared scale remains unresolved and needs either user confirmation or a methodological decision.
- The raw `guide_target_hamming_dist` in Table S3 does not always match the mismatch count computed directly from `guide_seq` and `target_at_guide`; the exact meaning of the raw column still needs confirmation.
- Excel has no explicit separate PAM column; the current PAM value is inferred only from the TTTN prefix and should be confirmed before use as a model feature.
- A small number of Table S5 DNA contexts are not 45 nt; those rows use a best-match fallback to locate the target window and should be manually reviewed later.
- Whether Table S4 augmentation should enter the first formal training workflow should be decided after the model plan is selected.
- Table S3 contains only type1/type2 and no exact pathogen names; species-level grouping validation needs an additional mapping.
