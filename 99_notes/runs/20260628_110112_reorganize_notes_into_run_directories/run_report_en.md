# Run Report: Reorganize Notes Into Run Directories

## Scope

This operation only processed `99_notes/`. It did not modify data files under `01_raw/`, `02_extracted_tables/`, `03_cleaned_minimal/`, or `04_candidate_ml_dataset/`.

## Directory rule

The new rule is that each data organization run, directory adjustment, or Git upload should have an independent directory under `99_notes/runs/`, named as `YYYYMMDD_HHMMSS_<operation-title-slug>/`. If the operation is committed to Git, `operation-title-slug` should correspond to the commit title.

## Completed organization

- Created `current/` for active questions, meeting decisions, and paper data notes.
- Created `runs/20260627_203620_audit_easy_design_2024_round1/` for the first EasyDesign audit records.
- Created `runs/20260628_004335_resolve_easy_design_2024_round2_baseline_dataset/` for the second EasyDesign PDF-based review and baseline dataset records.
- Created `runs/20260628_010938_initial_data_project_snapshot/` as a retrospective record of the first Git upload.
- Created `runs/20260628_105240_organize_backups_and_add_directory_guides/` as a retrospective record of the previous directory organization commit.
- Created `runs/20260628_110112_reorganize_notes_into_run_directories/` for this organization record.

## File naming

Files within one run directory use standardized names, such as `data_audit_zh.md`, `data_audit_en.md`, `run_report_zh.md`, `run_report_en.md`, `evidence_trace_zh.md`, `method_notes_en.md`, and `problems_to_resolve_zh.md`.

## Additional user change included

The user confirmed that the deletion of `04_candidate_ml_dataset/split_plan.md` was user-initiated. This deletion is included in the same commit. It is not part of the `99_notes` reorganization itself, but it is recorded with this Git submission.
