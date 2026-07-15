# Integrated Processing Roadmap for EasyDesign Mismatch Data

## 1. Objective and Boundaries

The objective is to produce a traceable EasyDesign mismatch v2 with preserved indel alignment, unified coordinates, and validated source mapping. v2 will coexist with v0 and will not overwrite it. This work will not modify `01_raw/`, train a model, or merge with DeepCas12a `editing_activity` labels.

## 2. Recommended Directories and Artifacts

### Contributor Snapshots

- Restore Xu's original script under `scripts/contributions/xu/` as a contribution snapshot only, not as a direct producer of the default training table.
- Preserve Lin's original scripts under `scripts/contributions/lin/` with SHA-256 values, original descriptions, and known issues.
- Register external input files in a run manifest first. Writing them into `01_raw/` still requires separate authorization.

### Intermediate Layer

- `02_extracted_tables/diagnostic_activity/easydesign_mismatch_mapping/`
- `EasyDesign_2024_TableS3_alignment_preserved_raw.csv`
- `EasyDesign_2024_TableS2_template_groups_raw.csv`
- `EasyDesign_2024_TableS2_TableS3_mapping_raw.csv`

### Minimal Cleaning Layer

- `03_cleaned_minimal/easydesign_mismatch/`
- `EasyDesign_2024_guide_target_alignment_v2.csv`
- `EasyDesign_2024_source_mapping_v1.csv`
- `EasyDesign_2024_mismatch_qc_v2.csv`

### Candidate Model Layer

- `04_candidate_ml_dataset/diagnostic_activity_easydesign/`
- Retain `EasyDesign_2024_diagnostic_activity_feature_table_v0.csv`
- Create `EasyDesign_2024_diagnostic_activity_feature_table_v2.csv`
- Create `feature_engineering_v2/` for the feature dictionary, QC, selection manifest, and generation report

## 3. Ordered Implementation

### Step 1: Freeze Sources and Build a Manifest

- Compute SHA-256 values for the original combined workbook, Xu inputs/scripts, Lin inputs/scripts, and existing outputs.
- Record contributor, provenance, receipt time, original filename, script entry point, and environment dependencies.
- Mark every external result as `contributor_supplied` first. A filename containing validated or final must not raise its evidence level.

Acceptance criterion: every input is uniquely locatable from the manifest and no original file is modified.

### Step 2: Rebuild a Gap-Preserving Table S3 Base Table

- Use Table S3 from the combined workbook as the authoritative input.
- Preserve the original 25-position `target_at_guide`, including `-`.
- Generate both `target_aligned_25` and `target_ungapped`; neither may overwrite the other.
- Retain `No.`, `guide_seq`, `30 min`, type1/type2, and raw Hamming.
- Generate stable `record_id`, `guide_target_pair_id`, and replicate index values.
- Remove only BOMs, surrounding whitespace, and confirmed display-formatting characters; flag IUPAC characters separately.

Acceptance criterion: all 10,634 rows remain traceable and all 740 rows containing `-` retain a 25-position alignment.

### Step 3: Define Unified 25-Position Coordinates and Event States

Use the direct Table S3 orientation throughout:

- Positions 1-4: PAM
- Positions 5-25: 21-nt spacer
- Store `match`, `substitution`, `gap_in_target`, `gap_in_guide`, or `unresolved` at each position
- Calculate `substitution_count`, `gap_count_target`, `gap_count_guide`, and `aligned_difference_count` separately
- Retain `mismatch_pos_1..25` and add `gap_pos_1..25` so substitutions and gaps are not collapsed into one binary field
- Use `target_ungapped` for composition features only, never to restore original coordinates

Acceptance criterion: position-level states sum to the row-level event list, and an absent position is never encoded as an ordinary matched zero.

### Step 4: Rebuild Table S2 Template Groups

- Record `template_group_id` using the paper-supported 22 x 9 structure.
- Mark the first row in each group as `reference_candidate`, with evidence recorded as paper plus sequence consensus.
- Mark rows 2-7 as substitution-template candidates, row 8 as an insertion-template candidate, and row 9 as a deletion-template candidate.
- Do not infer event direction from names alone; confirm it again using length and within-group alignment.
- Remove BOM/whitespace while preserving and flagging IUPAC characters such as `R`.

Acceptance criterion: all 22 groups contain nine rows, and group length patterns and reference-consensus checks are written to QC.

### Step 5: Perform Row-Level Table S3 Source Mapping

- Do not repeat an unconstrained deduplicated-guide x all-template scan.
- For every Table S3 `record_id`, use its original guide, gap-preserving target, and candidate template groups.
- Use a tested local/global sequence-alignment library with explicit scoring rather than hand-written fixed Hamming for indels.
- Test forward and reverse-complement orientations and output strand, start/end coordinates, alignment/CIGAR, substitution count, gap count, and total edit score.
- Retain every tied best hit and generate `mapping_count`, `mapping_status`, and `mapping_confidence`.
- Do not use an arbitrary `MAX_MISMATCH = 5` as truth. Mapping validity must reflect the original target, alignment completeness, PAM/spacer consistency, and ambiguity.

Acceptance criterion: every source row has `unique`, `ambiguous`, `unmapped`, or `invalid_input` status, and no unlabeled training row is generated.

### Step 6: Establish Three Evidence Levels

- `high`: valid original Table S3 pair, unique Table S2 mapping, and matching orientation and 25-position event vector.
- `medium`: valid Table S3 pair with multiple homologous or within-group templates but a consistent mismatch vector.
- `review`: indel, IUPAC, raw Hamming anomaly, tied window, or unresolved event direction.
- `exclude`: not a Table S3 experimental record, lacks a label, cannot be traced, or has damaged input.

Acceptance criterion: candidate training rows do not depend on guesses, and every downgrade reason is machine-filterable.

### Step 7: Recompute Xu-Type Features Instead of Restoring Old v1

- Generate gap-aware pair features from corrected `target_aligned_25`.
- Generate sequence-composition features from `target_ungapped`, guide, PAM, and spacer.
- Remove constants, exact duplicates, linear equivalents, and label-derived columns.
- Use former feature importance only as `prior_reference_rank`; it must not automatically determine include/exclude.
- For every feature, document input fields, formula, coordinate orientation, gap behavior, missing-value rule, and default-training eligibility.

Acceptance criterion: the gap-free subset exactly reproduces Xu's valid prior results, while all 740 indel rows pass manual sampling and row-level invariant checks.

### Step 8: Build v2 While Preserving Field Layers

Recommended v2 field groups:

- Traceability: `dataset_id`, `source_id`, `source_table_id`, `record_id`, `guide_target_pair_id`
- Labels: `label_raw_name`, `label_raw_value`, `label_normalized`, `label_status`, `label_scale_group`
- Sequence/alignment: `crRNA_sequence`, `target_aligned_25`, `target_ungapped`, `pam`, `spacer`, event counts, and position states
- Source/QC: `template_no`, `template_group_id`, `mapping_status`, `mapping_confidence`, `raw_hamming_agreement`, `alignment_qc_status`

Template ID, group, and mapping confidence should default to audit, grouping, and sensitivity analysis rather than numeric model inputs, reducing pathogen or experimental-batch leakage risk.

Acceptance criterion: v2 row counts match the corresponding v0 source rows. Every additional row must have an independent label source and may not originate from Lin's unlabeled candidates.

### Step 9: Define a Safe Baseline Usage Pattern

- First baseline: use only the 9,894 gap-free Table S3 rows to verify v2 against the reliable existing subset.
- Second baseline: add the 740 gap-aware rows and compare performance and stratified errors before and after inclusion.
- Repeated experiments with the same `guide_target_pair_id` must not cross train/validation boundaries.
- Retain the current paper or hash split and add template-group/pathogen-group sensitivity checks. Do not automatically replace the main split before source mapping stabilizes.
- Report metrics separately for gap-free, indel, unique-mapping, and ambiguous-mapping strata.

## 4. Automated QC Checklist

- Row count, unique primary keys, duplicate pairs, and replicate counts.
- Guide length, aligned target length, ungapped length, and DNA/IUPAC characters.
- TTTN PAM status and whether PAM plus spacer reconstructs the full guide.
- Whether position-state totals equal aligned difference counts.
- Agreement among raw Hamming, gap-aware Hamming, and Xu gap-free Hamming.
- Table S2 hit counts, ties, orientations, coordinates, and within-group reference consistency.
- Leakage checks across labels, splits, source mapping, and sequence features.
- One-to-one row join between v0 and v2, with explicit reasons for every unmatched row.

## 5. Stop Conditions

Do not publish v2 as the default training entry point if any condition holds:

- A row among the 740 containing `-` is used for position features after deleting its gap.
- An unlabeled Table S2 scan candidate is added as an experimental training row.
- A multi-template hit lacks an ambiguity flag.
- Mismatch coordinates omit direct/template orientation.
- Raw Hamming is treated as confirmed truth.
- v2 overwrites v0 or cannot trace back to original Table S3 rows.

## 6. Recommended Execution Order

1. Implement `build_easydesign_alignment_v2.py` for Steps 2-4 and QC only.
2. Implement `map_easydesign_table_s2_sources.py` for Steps 5-6.
3. Manually review all 188 Hamming anomalies and stratified samples of indel rows.
4. Implement `build_easydesign_feature_table_v2.py` for Steps 7-8.
5. Run an independent verifier for row-level, coordinate, and feature invariants.
6. Allow the baseline workflow to read v2 only after the audit passes.
