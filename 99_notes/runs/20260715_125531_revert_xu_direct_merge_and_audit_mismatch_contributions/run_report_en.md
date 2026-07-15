# Run Report

## Scope

This run handles EasyDesign mismatch-related contributions by reverting the direct Xu integration, independently reproducing Lin's scripts, cross-checking both result sets, and designing an integrated correction workflow.

## Inputs Scanned

- Git commit `fa8d67b Integrate Xu engineered features` and its parent `6a6535a`.
- Table S2, Table S3, Table S4, and Table S5 in original combined workbook `01_raw/EasyDesign_2024/data/imt2214-sup-0002-tables1-9sourcedata (1).xlsx`.
- Original EasyDesign paper at `/Users/linzibo/Downloads/iMeta - 2024 - Huang - Deep learning enhancing guide RNA design for CRISPR Cas12a‐based diagnostics.pdf`.
- Two Python scripts and two Excel inputs in Lin's directory `/Users/linzibo/Downloads/EasyDesign_S2_scanning/`.
- Lin's existing output `/Users/linzibo/Documents/mismatch_wide_table.xlsx`.
- Xu's original script and integrated artifacts from Git commit `fa8d67b`.
- Current v0 candidate tables and the active EasyDesign usage guide.

## Actions

- Confirmed that the pre-revert Git worktree was clean and that the latest commit was the Xu integration commit.
- Ran non-destructive `git revert fa8d67b`, producing commit `653fb6f`.
- Confirmed that the reverted file tree exactly matches `6a6535a`.
- Reran Lin's two scripts under `/private/tmp/easydesign_s2_lins_repro/` without writing to the original directory.
- Independently compared Table S2, Table S3, Lin's output, and the former Xu/v1 features.
- Reviewed paper pages 10-11 for the 22 x 9 template structure, TTTN PAM, 21-nt spacer, and `-` indel encoding.
- Generated bilingual review and integration-roadmap documents.
- Updated `99_notes/current/problems_to_resolve_en.md` and its Chinese counterpart.

## Confirmed Results

- The rollback was feasible and is complete. The former integration remains in Git history.
- Lin's inputs correspond to original Table S2/Table S3, and the output is reproducible cell by cell.
- Of 6,506 Lin output rows, 5,078 crosslink to Table S3, representing 3,404 unique gap-free pairs and 4,457 experimental rows.
- In the crosslinked subset, Xu direct mismatch counts and the coordinate-reversed 21-position vectors both agree at 100%.
- The remaining 1,428 Lin output rows are not Table S3 experimental records and have no fluorescence label.
- Table S3 contains 740 25-position alignments with `-`; current Xu processing cannot interpret position features correctly after deleting the gap.
- Raw Hamming agrees with direct counting on the gap-preserving 25-position alignment at 98.232%; 188 rows representing 28 unique pairs disagree.
- Lin's source scan supports the direct count for 10 anomalous pairs and 90 rows, but does not resolve every anomaly.

## Data Quality Issues

- Existing Xu indel features suffer from gap deletion and coordinate shifts.
- Lin's script loses source row number, target, label, and replicate, and generates unlabeled combinations.
- Lin's fixed Hamming and arbitrary threshold of five do not handle indels or report every tied hit.
- Table S2 contains BOMs, whitespace, and IUPAC `R`; normalization affects four Lin output rows.
- Project standalone `Table S2.xlsx` and `Table S3.xlsx` names do not match their actual contents. Catalog descriptions should be corrected without modifying raw files.

## Outputs Generated

- `99_notes/runs/20260715_125531_revert_xu_direct_merge_and_audit_mismatch_contributions/README.md`
- `99_notes/runs/20260715_125531_revert_xu_direct_merge_and_audit_mismatch_contributions/README_en.md`
- `mismatch_contribution_review_zh.md` / `mismatch_contribution_review_en.md`
- `mismatch_integration_roadmap_zh.md` / `mismatch_integration_roadmap_en.md`
- `run_report_zh.md` / `run_report_en.md`
- Updated bilingual current-problems files

## Evidence Boundary

### Facts Confirmed from Files

Row counts, column counts, sequence content, gap counts, output reproduction, Git-tree equality, and numerical agreement rates come from programmatic comparison. The 22 x 9 structure, TTTN/21-nt boundary, and `-` encoding come from the paper methods and are supported by workbook structure.

### Preliminary Inferences

Raw Hamming likely represents an author-provided gap-preserving aligned distance for most rows, but 188 anomalies prevent treating that interpretation as universally confirmed. The biological provenance of multi-template identical-sequence hits also cannot be determined from sequence identity alone.

## Next Recommended Actions

Follow `mismatch_integration_roadmap_en.md` to build alignment v2, row-level Table S2 source mapping, and feature table v2 in sequence. Until the audit passes, v0 remains the default entry point and existing position-mismatch features must not be used for the 740 indel records.
