# EasyDesign v2 Evidence Trace

## Decision 1: No Public Author Training-Preprocessing Script Was Found

**Confirmed facts**

- The main, dev, and visible commit history of the official repository at `https://github.com/scRNA-Compt/EasyDesign` were inspected; the recorded HEAD is `5c06a30d0a43be28a958831587f6ab706c2d4876`.
- Repository files and history were searched for `target_at_guide` and `guide_target_hamming_dist`; no script generating these fields was found.
- Commit `b6420fc` added only four xlsx data files; the paper Data Availability section points to the same repository and README.

**Decision**

No author training-preprocessing code generating these two fields was found in the inspected public branches and history. This does not prove that unpublished code never existed.

## Decision 2: `-` Is an Alignment Placeholder in the Five-State Encoding

**Confirmed facts**

- The paper's one-hot encoding method states that, for insertions/deletions, `-` is used in target DNA or crRNA and forms five states with A/C/T/G; target and guide are concatenated into a 10-dimensional vector at each position.
- Official `easyDesign/utils/predict_activity.py` assigns the fifth one-hot index with `onehot_idx['-'] = 4` and uses `ACT-ACTG` as an insertion/deletion example.

**Decision**

`-` is confirmed as a general alignment-gap symbol. A `-` in `target_at_guide` alone cannot establish whether the biological event is a target deletion, a guide deletion, or an insertion relative to the other channel. v2 therefore uses the representational name `gap_in_target` and does not rewrite it as a biological deletion label.

**Remaining uncertainty**

The public predictor defines `-` in `onehot_idx`, but the `FASTA_CODES` lookup used first by `onehot()` does not contain `-`; the static direct-call path is inconsistent. This runtime code cannot replace the missing training preprocessing implementation.

## Decision 3: Table S2 Supports a 22 x 9 Template Structure

**Confirmed facts**

- The methods describe 22 original templates, each with eight variants: six substitutions, one deletion, and one insertion, for 198 templates total.
- Grouping consecutive Table S2 rows into sets of nine yields 22 groups; members 1-7 have equal lengths, member 8 is longer, and member 9 is shorter in every group. All 198 rows pass structural QC.

**Decision**

Within each group, member 1 can be marked as the original reference, members 2-7 as substitution templates, member 8 as the insertion template, and member 9 as the deletion template. These roles follow the paper order and length pattern; they do not create an author-provided Template No. key for each Table S3 row.

## Decision 4: Public Materials Provide No Row-Level Plate/Template/Replicate Map

**Confirmed facts**

- The paper states that each 96-well plate contained two no-template negative wells and two duplicate high-fluorescence positive wells, which were used for normalization.
- No row-level plate ID, well, template ID, replicate, or crRNA-template pairing table was found in the paper, supplementary workbook, or official repository.

**Decision**

v2 does not invent plate or replicate metadata. `replicate_index_within_aligned_pair` records only the occurrence order of identical guide-target pairs in Table S3; it is not an experimental plate replicate ID.

## Decision 5: Table S2 Source Mapping Uses Only Reproducible Sequence Evidence

**Method evidence**

- The 25-position Table S3 `target_at_guide` alignment is preserved, while `target_ungapped` is generated only for sequence search.
- Forward and reverse-complement windows are searched across all 198 Table S2 templates, retaining every positional and template hit.
- A/C/G/T exact matching is attempted first; IUPAC-compatible matching is used only when no exact hit exists. No arbitrary mismatch threshold or first-hit selection is used.

**Results**

- 10,633/10,634 records have candidates: 7,421 unique exact, 3,146 single-group ambiguous, 50 multi-group ambiguous, 16 IUPAC-compatible, and 1 unmapped.
- The unmapped record is `EasyDesign_2024_TableS3_09121`.

**Decision**

Mapping supports source audit and grouped sensitivity analysis. It is not a label and is not a default model input.

## Decision 6: The Default v2 Training Entry Starts with No-Gap Table S3 Rows

**Confirmed facts**

- Table S3 contains 9,894 no-gap and 740 gap records.
- New and legacy mismatch calculations agree for 9,894/9,894 no-gap rows but only 33/740 gap rows.
- v2 matches v0 labels, source tables, and splits row by row; pair-level split leakage is zero.

**Decision**

The first baseline uses the 9,894 `eligible_core_v2` records. The 740 `conditional_gap_aware_v2` records enter only as a second-stage extension when the model explicitly supports a gap channel.

## Primary Evidence Sources

- Paper: `https://onlinelibrary.wiley.com/doi/10.1002/imt2.214`
- Official repository: `https://github.com/scRNA-Compt/EasyDesign`
- Combined workbook: `01_raw/EasyDesign_2024/data/imt2214-sup-0002-tables1-9sourcedata (1).xlsx`
- Local mirror of official code: `01_raw/EasyDesign_2024/easyDesign/utils/predict_activity.py`
