# EasyDesign_2024 Round-2 Data Audit

## Scope
This round only processed `EasyDesign_2024`. `01_raw` was not modified; no model was trained; different label systems were not merged.

## PDF Evidence
| source | page | fact |
| --- | --- | --- |
| /Users/linzibo/Downloads/iMeta - 2024 - Huang - Deep learning enhancing guide RNA design for CRISPR Cas12a‐based diagnostics.pdf | 1 | The paper reports 11,496 experimentally validated Cas12a-based detection cases. |
| /Users/linzibo/Downloads/iMeta - 2024 - Huang - Deep learning enhancing guide RNA design for CRISPR Cas12a‐based diagnostics.pdf |  | The methods state that the fluorescence value at 30 minutes was selected as the activity indicator. |
| /Users/linzibo/Downloads/iMeta - 2024 - Huang - Deep learning enhancing guide RNA design for CRISPR Cas12a‐based diagnostics.pdf |  | Plate readings were normalized using negative controls and positive controls in the same plate. |
| /Users/linzibo/Downloads/iMeta - 2024 - Huang - Deep learning enhancing guide RNA design for CRISPR Cas12a‐based diagnostics.pdf | 10 | Data augmentation used two label values for each pair: the 30-minute fluorescence and a 20-minute readout normalized to 30 minutes. |
| /Users/linzibo/Downloads/iMeta - 2024 - Huang - Deep learning enhancing guide RNA design for CRISPR Cas12a‐based diagnostics.pdf | 6 | The augmented dataset is described as containing 31,993 guide-to-target pairs. |
| /Users/linzibo/Downloads/iMeta - 2024 - Huang - Deep learning enhancing guide RNA design for CRISPR Cas12a‐based diagnostics.pdf |  | The methods describe 10,634 training pairs and 1,358 testing pairs. |
| /Users/linzibo/Downloads/iMeta - 2024 - Huang - Deep learning enhancing guide RNA design for CRISPR Cas12a‐based diagnostics.pdf |  | The methods describe a 21-nt sequence downstream of the PAM plus 10-nt flanks, producing a 45-nt target context. |
| /Users/linzibo/Downloads/iMeta - 2024 - Huang - Deep learning enhancing guide RNA design for CRISPR Cas12a‐based diagnostics.pdf | 3 | The paper discusses a TTTN PAM for the Cas12a guide-target sequence pairs. |
| /Users/linzibo/Downloads/iMeta - 2024 - Huang - Deep learning enhancing guide RNA design for CRISPR Cas12a‐based diagnostics.pdf | 15 | The supporting information list describes Tables S3-S5 as model-development datasets based on CRISPR fluorescence reaction. |

## Screenshot / Supporting-Information Evidence
| source | table | fact |
| --- | --- | --- |
| /var/folders/c9/xvbkv1hs5kz09g_fbjx8txd40000gn/T/codex-clipboard-e3e49006-b253-48c9-80e1-98d4742dde7b.png | Table S1 | Information on the types of viral and bacterial species used to build crRNA libraries. |
| /var/folders/c9/xvbkv1hs5kz09g_fbjx8txd40000gn/T/codex-clipboard-e3e49006-b253-48c9-80e1-98d4742dde7b.png | Table S2 | Information on viral and bacterial nucleic acid templates used to build crRNA libraries. |
| /var/folders/c9/xvbkv1hs5kz09g_fbjx8txd40000gn/T/codex-clipboard-e3e49006-b253-48c9-80e1-98d4742dde7b.png | Table S3 | Training data datasets for model development generated based on CRISPR fluorescence reaction. |
| /var/folders/c9/xvbkv1hs5kz09g_fbjx8txd40000gn/T/codex-clipboard-e3e49006-b253-48c9-80e1-98d4742dde7b.png | Table S4 | Augment datasets for model development generated based on CRISPR fluorescence reaction. |
| /var/folders/c9/xvbkv1hs5kz09g_fbjx8txd40000gn/T/codex-clipboard-e3e49006-b253-48c9-80e1-98d4742dde7b.png | Table S5 | Test datasets for model development generated based on CRISPR fluorescence reaction. |
| /var/folders/c9/xvbkv1hs5kz09g_fbjx8txd40000gn/T/codex-clipboard-e3e49006-b253-48c9-80e1-98d4742dde7b.png | Table S6 | Model performance evaluation by k-fold cross-validation. |
| /var/folders/c9/xvbkv1hs5kz09g_fbjx8txd40000gn/T/codex-clipboard-e3e49006-b253-48c9-80e1-98d4742dde7b.png | Table S7 | The DNA templates of four pathogens (MPXV, EV71, CV-A16, and L. monocytogenes) were used in the experimental activity testing. |
| /var/folders/c9/xvbkv1hs5kz09g_fbjx8txd40000gn/T/codex-clipboard-e3e49006-b253-48c9-80e1-98d4742dde7b.png | Table S8 | The crRNAs of four pathogens (MPXV, EV71, CV-A16, and L. monocytogenes) were used in the experimental activity testing. |
| /var/folders/c9/xvbkv1hs5kz09g_fbjx8txd40000gn/T/codex-clipboard-e3e49006-b253-48c9-80e1-98d4742dde7b.png | Table S9 | Optimal HPV crRNAs and RPA primers generated from the one-stop web platform of EasyDesign. |

## Resolved Questions
- `30 min`: the PDF methods confirm that the 30-minute fluorescence value was selected as the activity indicator; this round uses it as the primary label for the Table S3 internal baseline.
- `20 min normalized`: the PDF confirms that it is a derived/augmented label from the 20-minute readout normalized to 30 minutes; it is not merged into the primary label.
- `out_logk_measurement`: it belongs to the Table S4 augmented dataset; this round stores it separately as optional augmentation and excludes it from the default baseline.
- `true value`: it belongs to the Table S5 test dataset as the experimental true value; it is retained as an external paper test label, but its numeric scale versus Table S3 still needs confirmation.
- Standalone workbook versus combined source-data workbook: the combined workbook is used as the authoritative source, while standalone tables are treated as duplicate sources.
- Figure source data: retained as evidence or metadata, not used directly as tidy crRNA-target training rows.
- `guide-expected-activities` and model columns: all are classified as predicted scores, not primary training labels.
- PAM: the PDF supports a TTTN PAM; Excel has no separate PAM column, so this round only infers a 5-prime TTTN prefix and marks it as inferred.
- Fig.S3: it is aggregate figure source data about sequence/activity features and is not used as row-level training labels.

## Remaining Questions
- Whether the negative `30 min` labels in Table S3 and the positive `true value` labels in Table S5 can be mapped to one shared scale remains unresolved and needs either user confirmation or a methodological decision.
- The raw `guide_target_hamming_dist` in Table S3 does not always match the mismatch count computed directly from `guide_seq` and `target_at_guide`; the exact meaning of the raw column still needs confirmation.
- Excel has no explicit separate PAM column; the current PAM value is inferred only from the TTTN prefix and should be confirmed before use as a model feature.
- Whether Table S4 augmentation should enter the first formal training workflow should be decided after the model plan is selected.
- Table S3 contains only type1/type2 and no exact pathogen names; species-level grouping validation needs an additional mapping.

## Round-2 Data Organization Conclusions
- Table S3 is used for the primary internal baseline split: baseline_train=8417, baseline_validation=2217.
- Table S5 is retained as the external paper test: 1358 rows, marked as scale_unconfirmed.
- Table S4 is optional augmentation: 31993 rows, excluded from the default baseline.
