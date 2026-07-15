# Review of EasyDesign Mismatch Processing Contributions

## 1. Purpose

This review compares Xu's and Lin's processing of EasyDesign guide-target mismatch information. It separates reproducible facts, mutually corroborated results, unresolved inferences, and outputs that must not enter the default training table. Mismatch features are inputs or annotations, not fluorescence/RFU activity labels.

## 2. Artifacts Reviewed

### Xu

- Original contributions: `generate_validated_engineered_features.py` and first-run feature importance.
- Former integration commit: `fa8d67b Integrate Xu engineered features`.
- Main processing: compare direct, complement, reverse, and reverse-complement orientations of cleaned `crRNA_sequence` and `target_sequence`; select the orientation most consistent with project field `guide_target_hamming_dist_computed`; then generate Hamming, position, mismatch-type, and sequence-composition features.

### Lin

- Directory: `/Users/linzibo/Downloads/EasyDesign_S2_scanning/`.
- Inputs: `guide_seq.xlsx` and `Table_S2.xlsx`.
- Scripts: `filter_templates_crrna.py` and `integrated_snv_analysis.py`.
- Located output: `/Users/linzibo/Documents/mismatch_wide_table.xlsx`.
- Main processing: deduplicate Table S3 guides, remove the 5-prime TTTN, reverse-complement the 21-nt spacer, and scan the 198 long Table S2 templates for the best window with no more than five differences.

## 3. Confirmed Facts

- The 10,634 `No.` and `guide_seq` rows in Lin's `guide_seq.xlsx` match original Table S3 row by row; they contain 1,357 unique guides.
- The 198 records in Lin's `Table_S2.xlsx` match Table S2 in the original combined supplementary workbook.
- The paper confirms that Table S2 contains 22 original templates, each accompanied by six substitution templates, one insertion template, and one deletion template, for 22 x 9 = 198 records.
- In each Table S2 group, the first seven sequences have equal lengths, the eighth is longer, and the ninth is shorter. The first sequence in all 22 groups equals the majority consensus of the first seven. The paper and data structure therefore support grouping every nine rows and treating the first as the reference.
- Every Table S3 guide is 25 nt and begins with TTTN. The paper defines 21 positions downstream of the PAM, supporting positions 1-4 as PAM and positions 5-25 as spacer.
- Table S3 contains 740 `target_at_guide` rows with `-`. The paper explicitly uses `-` as the fifth encoded character for insertions or deletions.
- Lin's script is reproducible: `mismatch_wide_table.xlsx` has 6,506 rows and 30 columns, and a temporary rerun matched the existing workbook cell by cell.

## 4. Mutually Corroborated and Usable Content

### 4.1 Direct Orientation for Gap-Free Guide-Target Pairs

Lin's output contains 5,078 template-guide mappings that reconstruct to real, gap-free Table S3 guide-target pairs. They represent 3,404 unique pairs and 4,457 Table S3 experimental rows.

Within this subset:

- Lin's `No_mismatch` agrees with the Xu/project direct Hamming count at 100%.
- After reversing the coordinate system, Lin's 21-position spacer vector agrees with Xu's position vector at 100%.
- The coordinate relation is `Lin pos_i = Xu mismatch_pos_(26-i)`; Lin does not represent Xu positions 1-4 in the PAM region.

This provides independent Table S2 source evidence for the direct orientation and mismatch calculation in the gap-free subset. It can confirm computational orientation, but equivalent features from both pipelines must not be entered twice in a model.

### 4.2 PAM and Spacer Boundary

Xu represents the complete 25-nt guide-target pair, while Lin uses the reverse-complemented 21-nt spacer. Together with the universal TTTN prefix and the paper methods, the project should explicitly distinguish:

- `pam_aligned = positions 1-4`
- `spacer_aligned = positions 5-25`
- When `template_window` is on the opposite strand, strand and coordinate transformation must be stored.

### 4.3 Sequence-Composition Features

Xu's length, GC, base fraction, entropy, homopolymer, and k-mer calculations are principled and reproducible when the input is an unambiguous A/C/G/T sequence. They can be recomputed on the corrected sequence layer. Constant, duplicate, and linearly equivalent features should be removed, and one feature-importance run must not automatically define the final feature set.

### 4.4 Improved Understanding of Raw Hamming Anomalies

The raw Table S3 `guide_target_hamming_dist` agrees with direct counting on the 25-position, gap-preserving character alignment for 98.232% of rows. There are 188 inconsistent rows representing 28 unique pairs.

Lin's source scan covers 10 of those anomalous pairs and 90 rows. The template evidence supports direct sequence counts of zero or one rather than the raw values of 1-10. The raw field therefore likely represents an author-provided aligned distance for most rows but contains anomalies or mixed processing; it remains excluded from default training features.

## 5. Limitations and Improper Processing in Xu's Work

### 5.1 Upstream Cleaning Destroyed the Indel Alignment

Existing v0 cleaning removed `-` from Table S3 `target_at_guide`, shortening 740 targets to 17, 18, 23, or 24 nt. Xu's script then left-aligns the shortened target and adds a length-difference penalty. Bases after the first gap shift position, so mismatch position, mismatch type, consecutive-run, and regional mismatch features for these rows cannot be interpreted at their original biological coordinates.

### 5.2 Orientation Validation Was Not Independent Biological Validation

Xu selected direct orientation because it exactly matched project field `guide_target_hamming_dist_computed`, which was calculated from the same cleaned sequences under the same definition. This proves internal consistency, but the reference and tested result share inputs and logic. Lin's Table S2 crosswalk for 3,404 unique gap-free pairs supplies partial independent support.

### 5.3 Absent Positions Were Encoded as Ordinary Values

Xu's full generator writes zero beyond the aligned length, conflating "position absent" with "position present and matched." Even where the later v1 builder changed these values to missing, the coordinate shift after a gap remained unresolved.

### 5.4 Feature-Importance Evidence Boundary

The first-run feature importance and reference improved outputs lack complete training code, model parameters, a dependency lock, random seeds, and reproducible split evidence. They are candidate-feature clues only and do not establish stable causal or cross-model value.

### 5.5 Direct Integration Was Premature

Directly merging Xu features into default v1 while 740 indel rows and raw Hamming semantics remained unresolved packaged known alignment defects as model-ready data. This run reverses that default integration with Git revert.

## 6. Limitations and Improper Processing in Lin's Work

### 6.1 Experimental Record Keys and Labels Were Lost

The script retains and deduplicates only guides, discarding Table S3 `No.`, `target_at_guide`, `30 min`, repeated experiments, and original splits. It then performs a 1,357 x 198 candidate scan, so the output is not a row-level Table S3 validation table.

### 6.2 Unlabeled Additional Combinations Were Generated

Only 5,078 of 6,506 output rows map back to Table S3 pairs. The remaining 1,428 are not original experimental records. Every output with three to five mismatches belongs to this subset. They have no fluorescence label and must not enter the diagnostic-activity training set.

### 6.3 Fixed Hamming Cannot Handle Indels

The script fixes the spacer at 21 nt and uses equal-length sliding-window Hamming distance. It neither reads nor preserves the Table S3 `-` alignment and therefore does not resolve the 740 indel records that most need correction.

### 6.4 Threshold and Naming Lack Evidence

`MAX_MISMATCH = 5` has no support from the paper, README, or data distribution. The `snv` name is also inaccurate because the output contains zero to five differences and is not restricted to single-nucleotide variants.

### 6.5 Best-Window and Template Ambiguity Were Not Reported

Of 3,404 crosslinked unique pairs, 2,762 map to one template and 642 map to multiple templates, with a maximum of nine. The script retains only the earliest best window, stops early on a zero-mismatch hit, and does not record all tied hits or an ambiguity status.

### 6.6 Input Characters Were Not Normalized Safely

Seventeen Table S2 rows contain a BOM, whitespace, or `R`. The script only uppercases input. After normalization, four output rows change their best window or mismatch count. BOM and whitespace are formatting characters, while `R` must be flagged as an IUPAC ambiguity rather than silently deleted or treated as an ordinary mismatch.

### 6.7 The Reference Template Was Not Used in the Calculation

The 22 x 9 grouping and first-row reference are credible, but `Reference_Template` is only copied into the output. The script does not calculate changes in a mutated template relative to its reference or use within-group homology to constrain guide provenance.

## 7. Current Adoption Decision

| Content | Status | Use |
|---|---|---|
| EasyDesign v0 experimental labels, provenance, and split | Retain | Current default candidate data |
| Xu gap-free sequence-composition features | Adopt after recomputation | v2 candidate inputs |
| Xu direct mismatch features for gap-free rows | Conditionally adopt | Only rows passing 25-nt A/C/G/T alignment QC |
| Existing Xu mismatch features for 740 indel rows | Hold | Regenerate while preserving `-` |
| Xu feature importance | Reference only | Candidate priority, not final selection evidence |
| Lin 22 x 9 grouping and first-row reference | Adopt | Source-mapping metadata |
| Lin unique hits crosslinked to Table S3 | Adopt after correction | `source_mapping` annotation, not a label |
| Lin multi-template hits | Retain with ambiguity flag | Group validation or manual review |
| Lin 1,428 non-Table S3 candidates | Exclude from training | Unlabeled candidate library or hold |
| Lin current `pos_1..pos_21` | Do not merge directly | Convert to unified 25-position direct coordinates |
| Raw `guide_target_hamming_dist` | Hold | Preserve value and anomaly flag for audit |

## 8. Remaining Unresolved Questions

- Rows among the 188 raw Hamming anomalies not explained by a unique Table S2 mapping still require row-level investigation or author clarification.
- Before naming biological event types, model input code and supplementary methods must clarify whether `-` in each Table S3 row represents a deletion in the guide relative to target, a deletion in target relative to guide, or a common encoding-layer gap.
- Before constructing a template-level split, decide whether multi-template identical-sequence hits represent homologous provenance, technical repeats, or indistinguishable mappings.
- The project standalone `Table S2.xlsx` actually contains Training/Augment/Test sheets, while `Table S3.xlsx` contains DNA/crRNA for four pathogens. Raw files must remain unchanged, but catalog descriptions need correction based on content.
