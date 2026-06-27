# Evidence Trace EasyDesign_2024

## Table S1.xlsx / species

Decision: `metadata_only` with priority `medium`.

Evidence:
- File name: `Table S1.xlsx`
- Sheet name: `species`
- Title/caption: Pathogen
- First columns: A: blank_1, B: Pathogen, C: Type, D: No. of crRNA
- Label candidates: none detected

Reasoning:
- pathogen/species metadata

Remaining uncertainty:
- May duplicate a standalone table or a combined source-data workbook; do not merge automatically.

## Table S1.xlsx / templates

Decision: `metadata_only` with priority `medium`.

Evidence:
- File name: `Table S1.xlsx`
- Sheet name: `templates`
- Title/caption: Template No.
- First columns: A: Template No., B: Sequence
- Label candidates: none detected

Reasoning:
- pathogen/template sequence metadata

Remaining uncertainty:
- May duplicate a standalone table or a combined source-data workbook; do not merge automatically.

## Table S2.xlsx / Training data

Decision: `diagnostic_activity` with priority `high`.

Evidence:
- File name: `Table S2.xlsx`
- Sheet name: `Training data`
- Title/caption: No.
- First columns: A: No., B: guide_seq, C: target_at_guide, D: guide_target_hamming_dist, E: 30 min, F: 20 min normalized, G: type1, H: type2
- Label candidates: 30 min, 20 min normalized

Reasoning:
- measured diagnostic activity table with guide/target sequences

Remaining uncertainty:
- May duplicate a standalone table or a combined source-data workbook; do not merge automatically.

## Table S2.xlsx / Augment data

Decision: `diagnostic_activity` with priority `high`.

Evidence:
- File name: `Table S2.xlsx`
- Sheet name: `Augment data`
- Title/caption: No.
- First columns: A: No., B: guide_seq, C: target_at_guide, D: out_logk_measurement
- Label candidates: out_logk_measurement

Reasoning:
- measured diagnostic activity table with guide/target sequences

Remaining uncertainty:
- May duplicate a standalone table or a combined source-data workbook; do not merge automatically.

## Table S2.xlsx / Test data

Decision: `diagnostic_activity` with priority `high`.

Evidence:
- File name: `Table S2.xlsx`
- Sheet name: `Test data`
- Title/caption: No.
- First columns: A: No., B: DNA, C: crRNA, D: true value, E: CNND, F: CNN12a, G: CNN12ae, H: TransformerD, I: Transformer12a, J: Transformer12ae, K: type
- Label candidates: true value, CNND, CNN12a, CNN12ae, TransformerD, Transformer12a, Transformer12ae

Reasoning:
- measured diagnostic activity table with guide/target sequences

Remaining uncertainty:
- Sheet includes measured-like and prediction/model-score fields; keep them separate. May duplicate a standalone table or a combined source-data workbook; do not merge automatically.

## Table S3.xlsx / DNA templat

Decision: `metadata_only` with priority `medium`.

Evidence:
- File name: `Table S3.xlsx`
- Sheet name: `DNA templat`
- Title/caption: Name
- First columns: A: Name, B: Sequence (5'-3')
- Label candidates: none detected

Reasoning:
- pathogen/template sequence metadata

Remaining uncertainty:
- May duplicate a standalone table or a combined source-data workbook; do not merge automatically.

## Table S3.xlsx / crRNA

Decision: `predicted_library` with priority `medium`.

Evidence:
- File name: `Table S3.xlsx`
- Sheet name: `crRNA`
- Title/caption: crRNA name
- First columns: A: crRNA name, B: Sequence (5'-3')
- Label candidates: none detected

Reasoning:
- candidate crRNA sequence library without measured label

Remaining uncertainty:
- May duplicate a standalone table or a combined source-data workbook; do not merge automatically.

## Table S4.xlsx /  crRNA and RPA primers

Decision: `predicted_library` with priority `medium`.

Evidence:
- File name: `Table S4.xlsx`
- Sheet name: ` crRNA and RPA primers`
- Title/caption: crRNA
- First columns: A: crRNA, B: sequence (5'-3'), C: RPA primer, D: sequence (5'-3')_2
- Label candidates: none detected

Reasoning:
- designed crRNA and/or RPA primer table

Remaining uncertainty:
- May duplicate a standalone table or a combined source-data workbook; do not merge automatically.

## imt2214-sup-0002-tables1-9sourcedata (1).xlsx / Table S1

Decision: `metadata_only` with priority `medium`.

Evidence:
- File name: `imt2214-sup-0002-tables1-9sourcedata (1).xlsx`
- Sheet name: `Table S1`
- Title/caption: Table S1. Information on the types of viral and bacterial species used to build crRNA libraries.
- First columns: A: blank_1, B: Pathogen, C: Type, D: No. of crRNA
- Label candidates: none detected

Reasoning:
- pathogen/species metadata

Remaining uncertainty:
- May duplicate a standalone table or a combined source-data workbook; do not merge automatically.

## imt2214-sup-0002-tables1-9sourcedata (1).xlsx / Table S2

Decision: `metadata_only` with priority `medium`.

Evidence:
- File name: `imt2214-sup-0002-tables1-9sourcedata (1).xlsx`
- Sheet name: `Table S2`
- Title/caption: Table S2. Information on viral and bacterial nucleic acid templates used to build crRNA libraries.
- First columns: A: Template No., B: Sequence
- Label candidates: none detected

Reasoning:
- pathogen/template sequence metadata

Remaining uncertainty:
- May duplicate a standalone table or a combined source-data workbook; do not merge automatically.

## imt2214-sup-0002-tables1-9sourcedata (1).xlsx / Table S3

Decision: `diagnostic_activity` with priority `high`.

Evidence:
- File name: `imt2214-sup-0002-tables1-9sourcedata (1).xlsx`
- Sheet name: `Table S3`
- Title/caption: Table S3. Training data datasets for model development generated based on CRISPR fluorescence reaction.
- First columns: A: No., B: guide_seq, C: target_at_guide, D: guide_target_hamming_dist, E: 30 min, F: 20 min normalized, G: type1, H: type2
- Label candidates: 30 min, 20 min normalized

Reasoning:
- measured diagnostic activity table with guide/target sequences

Remaining uncertainty:
- Sheet includes measured-like and prediction/model-score fields; keep them separate. May duplicate a standalone table or a combined source-data workbook; do not merge automatically.

## imt2214-sup-0002-tables1-9sourcedata (1).xlsx / Table S4

Decision: `diagnostic_activity` with priority `high`.

Evidence:
- File name: `imt2214-sup-0002-tables1-9sourcedata (1).xlsx`
- Sheet name: `Table S4`
- Title/caption: Table S4. Augment datasets for model development generated based on CRISPR fluorescence reaction.
- First columns: A: No., B: guide_seq, C: target_at_guide, D: out_logk_measurement
- Label candidates: out_logk_measurement

Reasoning:
- measured diagnostic activity table with guide/target sequences

Remaining uncertainty:
- Sheet includes measured-like and prediction/model-score fields; keep them separate. May duplicate a standalone table or a combined source-data workbook; do not merge automatically.

## imt2214-sup-0002-tables1-9sourcedata (1).xlsx / Table S5

Decision: `diagnostic_activity` with priority `high`.

Evidence:
- File name: `imt2214-sup-0002-tables1-9sourcedata (1).xlsx`
- Sheet name: `Table S5`
- Title/caption: Table S5. Test datasets for model development generated based on CRISPR fluorescence reaction.
- First columns: A: No., B: DNA, C: crRNA, D: true value, E: CNND, F: CNN12a, G: CNN12ae, H: TransformerD, I: Transformer12a, J: Transformer12ae, K: type
- Label candidates: true value, CNND, CNN12a, CNN12ae, TransformerD, Transformer12a, Transformer12ae

Reasoning:
- measured diagnostic activity table with guide/target sequences

Remaining uncertainty:
- Sheet includes measured-like and prediction/model-score fields; keep them separate. May duplicate a standalone table or a combined source-data workbook; do not merge automatically.

## imt2214-sup-0002-tables1-9sourcedata (1).xlsx / Table S6

Decision: `metadata_only` with priority `low`.

Evidence:
- File name: `imt2214-sup-0002-tables1-9sourcedata (1).xlsx`
- Sheet name: `Table S6`
- Title/caption: Table S6. Model performance evaluation by k-fold cross-validation.
- First columns: A: Fold 1, B: 0.8038
- Label candidates: none detected

Reasoning:
- model performance or figure summary metadata

Remaining uncertainty:
- May duplicate a standalone table or a combined source-data workbook; do not merge automatically.

## imt2214-sup-0002-tables1-9sourcedata (1).xlsx / Table S7

Decision: `metadata_only` with priority `medium`.

Evidence:
- File name: `imt2214-sup-0002-tables1-9sourcedata (1).xlsx`
- Sheet name: `Table S7`
- Title/caption: Table S7. The DNA templates of four pathogens (MPXV, EV71, CV-A16 and L. monocytogenes) used in the experimental activity testing.
- First columns: A: Name, B: Sequence (5'-3')
- Label candidates: none detected

Reasoning:
- pathogen/template sequence metadata

Remaining uncertainty:
- May duplicate a standalone table or a combined source-data workbook; do not merge automatically.

## imt2214-sup-0002-tables1-9sourcedata (1).xlsx / Table S8

Decision: `predicted_library` with priority `medium`.

Evidence:
- File name: `imt2214-sup-0002-tables1-9sourcedata (1).xlsx`
- Sheet name: `Table S8`
- Title/caption: Table S8. The crRNAs of four pathogens (MPXV, EV71, CV-A16 and L. monocytogenes) used in the experimental activity testing.
- First columns: A: crRNA name, B: Sequence (5'-3')
- Label candidates: none detected

Reasoning:
- candidate crRNA sequence library without measured label

Remaining uncertainty:
- May duplicate a standalone table or a combined source-data workbook; do not merge automatically.

## imt2214-sup-0002-tables1-9sourcedata (1).xlsx / Table S9

Decision: `predicted_library` with priority `medium`.

Evidence:
- File name: `imt2214-sup-0002-tables1-9sourcedata (1).xlsx`
- Sheet name: `Table S9`
- Title/caption: Table S9. Optimal HPV crRNAs and RPA primers generated from the one-stop web platform of EasyDesign.
- First columns: A: crRNA, B: sequence (5'-3'), C: RPA primer, D: sequence (5'-3')_2
- Label candidates: none detected

Reasoning:
- designed crRNA and/or RPA primer table

Remaining uncertainty:
- May duplicate a standalone table or a combined source-data workbook; do not merge automatically.

## imt2214-sup-0002-tables1-9sourcedata (1).xlsx / Fig.1

Decision: `metadata_only` with priority `medium`.

Evidence:
- File name: `imt2214-sup-0002-tables1-9sourcedata (1).xlsx`
- Sheet name: `Fig.1`
- Title/caption: Source Data Figure1. Preparation and Evaluation of the Cas12a-based crRNA dataset for deep learning models training.
- First columns: A: No., B: type1, C: type2, D: blank_4, E: Mismatch number, F: total, G: blank_7, H: blank_8, I: A, J: T, K: C, L: G, M: blank_13, N: blank_14, O: A_2, P: T_2, Q: C_2, R: G_2, S: blank_19, T: blank_20
- Label candidates: none detected

Reasoning:
- pathogen/species metadata

Remaining uncertainty:
- May duplicate a standalone table or a combined source-data workbook; do not merge automatically.

## imt2214-sup-0002-tables1-9sourcedata (1).xlsx / Fig.2

Decision: `metadata_only` with priority `low`.

Evidence:
- File name: `imt2214-sup-0002-tables1-9sourcedata (1).xlsx`
- Sheet name: `Fig.2`
- Title/caption: Source Data Figure2. Development and evaluation of a deep learning model suitable for Cas12a diagnostic design.
- First columns: A: Models, B: Coefficient, C: blank_3, D: blank_4, E: Control, F: Sample
- Label candidates: Coefficient

Reasoning:
- model performance or figure summary metadata

Remaining uncertainty:
- May duplicate a standalone table or a combined source-data workbook; do not merge automatically.

## imt2214-sup-0002-tables1-9sourcedata (1).xlsx / Fig.3

Decision: `diagnostic_activity` with priority `medium`.

Evidence:
- File name: `imt2214-sup-0002-tables1-9sourcedata (1).xlsx`
- Sheet name: `Fig.3`
- Title/caption: Source Data Figure3. Validation of EasyDesign performance across four pathogens.
- First columns: A: pathogens, B: True, C: Predicted in true tops, D: blank_4, E: MPXV, F: Normalized fluoresence, G: blank_7, H: blank_8, I: 10^8, J: Normalized fluoresence_2, K: blank_11, L: blank_12, M: blank_13, N: blank_14, O: blank_15, P: blank_16, Q: blank_17, R: blank_18, S: blank_19, T: blank_20
- Label candidates: Predicted in true tops, Normalized fluoresence, Normalized fluoresence_2, Normalized fluoresence_3, Normalized fluoresence_4, Normalized fluoresence_5, Normalized fluoresence_6, Normalized fluoresence_7, Normalized fluoresence_8

Reasoning:
- figure source data containing fluorescence/activity-like measurements

Remaining uncertainty:
- Contains measurement-like fields but lacks a tidy crRNA-target pair structure. Sheet includes measured-like and prediction/model-score fields; keep them separate. May duplicate a standalone table or a combined source-data workbook; do not merge automatically.

## imt2214-sup-0002-tables1-9sourcedata (1).xlsx / Fig.4

Decision: `diagnostic_activity` with priority `medium`.

Evidence:
- File name: `imt2214-sup-0002-tables1-9sourcedata (1).xlsx`
- Sheet name: `Fig.4`
- Title/caption: Source Data Figure4. HPV clinical sample testing design via EasyDesign web server.
- First columns: A: min, B: fluorescence unit (HPV6), C: blank_3, D: blank_4, E: blank_5, F: blank_6, G: blank_7, H: blank_8, I: min_2, J: fluorescence unit (HPV11), K: blank_11, L: blank_12, M: blank_13, N: blank_14, O: blank_15, P: blank_16, Q: min_3, R: fluorescence unit (HPV16), S: blank_19, T: blank_20
- Label candidates: fluorescence unit (HPV6), fluorescence unit (HPV11), fluorescence unit (HPV16), fluorescence unit (HPV18), fluorescence unit (HPV31), fluorescence unit (HPV33)

Reasoning:
- figure source data containing fluorescence/activity-like measurements

Remaining uncertainty:
- Contains measurement-like fields but lacks a tidy crRNA-target pair structure. May duplicate a standalone table or a combined source-data workbook; do not merge automatically.

## imt2214-sup-0002-tables1-9sourcedata (1).xlsx / Fig.S1

Decision: `metadata_only` with priority `medium`.

Evidence:
- File name: `imt2214-sup-0002-tables1-9sourcedata (1).xlsx`
- Sheet name: `Fig.S1`
- Title/caption: Source Data Figure S1. Distribution of base types at different positions in the crRNAs set.
- First columns: A: position, B: number, C: blank_3, D: blank_4, E: blank_5
- Label candidates: none detected

Reasoning:
- pathogen/species metadata

Remaining uncertainty:
- May duplicate a standalone table or a combined source-data workbook; do not merge automatically.

## imt2214-sup-0002-tables1-9sourcedata (1).xlsx / Fig.S2

Decision: `diagnostic_activity` with priority `medium`.

Evidence:
- File name: `imt2214-sup-0002-tables1-9sourcedata (1).xlsx`
- Sheet name: `Fig.S2`
- Title/caption: Source Data Figure S2. Fluorescence kinetic curves for high mismatch guide–target pairs.
- First columns: A: min, B: Fluoresence value, C: blank_3, D: blank_4, E: min_2, F: Fluoresence value_2, G: blank_7, H: blank_8, I: min_3, J: Fluoresence value_3, K: blank_11, L: blank_12, M: min_4, N: Fluoresence value_4, O: blank_15, P: blank_16, Q: min_5, R: Fluoresence value_5, S: blank_19, T: blank_20
- Label candidates: Fluoresence value, Fluoresence value_2, Fluoresence value_3, Fluoresence value_4, Fluoresence value_5, Fluoresence value_6

Reasoning:
- figure source data containing fluorescence/activity-like measurements

Remaining uncertainty:
- Contains measurement-like fields but lacks a tidy crRNA-target pair structure. May duplicate a standalone table or a combined source-data workbook; do not merge automatically.

## imt2214-sup-0002-tables1-9sourcedata (1).xlsx / Fig.S3

Decision: `unclear` with priority `low`.

Evidence:
- File name: `imt2214-sup-0002-tables1-9sourcedata (1).xlsx`
- Sheet name: `Fig.S3`
- Title/caption: Source Data FigureS3. Correlation analysis of characteristics and activity of guide-to-target pairs.
- First columns: A: "N1N2" of "TTTN1N2", B: Active pairs (fraction), C: blank_3, D: activity in mismatch, E: blank_5, F: blank_6, G: blank_7, H: activity in different mutation scenarios, I: blank_9, J: blank_10, K: blank_11, L: blank_12
- Label candidates: activity in mismatch, activity in different mutation scenarios

Reasoning:
- unclear sheet content

Remaining uncertainty:
- May duplicate a standalone table or a combined source-data workbook; do not merge automatically.

## imt2214-sup-0002-tables1-9sourcedata (1).xlsx / Fig.S7

Decision: `diagnostic_activity` with priority `medium`.

Evidence:
- File name: `imt2214-sup-0002-tables1-9sourcedata (1).xlsx`
- Sheet name: `Fig.S7`
- Title/caption: Source Data FigureS7. CRISPR fluorescence results at different DNA template concentrations.
- First columns: A: blank_1, B: 10^10, C: 10^9, D: 10^8, E: blank_5, F: blank_6, G: T1, H: T2, I: T3, J: T4, K: T5, L: T6, M: T7, N: T8, O: T9, P: T10, Q: blank_17, R: blank_18, S: 10^10_2, T: 10^9_2
- Label candidates: none detected

Reasoning:
- figure source data containing fluorescence/activity-like measurements

Remaining uncertainty:
- Contains measurement-like fields but lacks a tidy crRNA-target pair structure. May duplicate a standalone table or a combined source-data workbook; do not merge automatically.

## imt2214-sup-0002-tables1-9sourcedata (1).xlsx / Fig.S8

Decision: `diagnostic_activity` with priority `medium`.

Evidence:
- File name: `imt2214-sup-0002-tables1-9sourcedata (1).xlsx`
- Sheet name: `Fig.S8`
- Title/caption: Source Data FigureS8. The fluorescence kinetic curve of the Cas12a reaction in the detection of HPV clinical samples.
- First columns: A: min, B: fluorescence unit (HPV6 #1), C: blank_3, D: blank_4, E: blank_5, F: blank_6, G: blank_7, H: blank_8, I: min_2, J: fluorescence unit (HPV6 #2), K: blank_11, L: blank_12, M: blank_13, N: blank_14, O: blank_15, P: blank_16, Q: min_3, R: fluorescence unit (HPV6 #3), S: blank_19, T: blank_20
- Label candidates: fluorescence unit (HPV6 #1), fluorescence unit (HPV6 #2), fluorescence unit (HPV6 #3), fluorescence unit (HPV11 #4), fluorescence unit (HPV11 #5), fluorescence unit (HPV11 #6), fluorescence unit (HPV16 #7), fluorescence unit (HPV16 #8), fluorescence unit (HPV16 #9), fluorescence unit (HPV16 #10)

Reasoning:
- figure source data containing fluorescence/activity-like measurements

Remaining uncertainty:
- Contains measurement-like fields but lacks a tidy crRNA-target pair structure. May duplicate a standalone table or a combined source-data workbook; do not merge automatically.
