# 99_notes

This directory stores audit reports, evidence traces, unresolved questions, and decisions. It explains why the data are organized in a given way. It does not store training data.

## Top-level structure

- `current/`: active questions, meeting decisions, and paper data notes that are still in use.
- `runs/`: one independent record directory for each data organization run, directory adjustment, or Git upload.
- `README.md` / `README_en.md`: usage notes for this directory.

## Run directory naming rule

All new run directories should use:

`runs/YYYYMMDD_HHMMSS_<operation-title-slug>/`

Rules:

- `YYYYMMDD_HHMMSS` uses the local time when the operation starts or when the commit is prepared.
- `<operation-title-slug>` is the lowercase underscore form of the Git commit title or the main operation title.
- If the operation is committed to Git, the commit title should match the directory title, for example `Reorganize notes into run directories` maps to `reorganize_notes_into_run_directories`.
- Each run directory should contain at least `README.md` and `README_en.md`. Audit reports, run reports, evidence traces, method notes, and unresolved questions should use `data_audit_*`, `run_report_*`, `evidence_trace_*`, `method_notes_*`, and `problems_to_resolve_*`.

## Current records

- Current unresolved questions: `current/problems_to_resolve_zh.md` and `current/problems_to_resolve_en.md`.
- Current meeting decisions: `current/meeting_decisions_zh.md` and `current/meeting_decisions_en.md`.
- Current paper data notes: `current/paper_data_notes_zh.md` and `current/paper_data_notes_en.md`.

## Usage rules

- Record uncertain issues in `current/` instead of guessing inside data tables.
- Each data organization run and each Git upload should have its own directory under `runs/`.
- Chinese and English documentation from the same run should stay aligned.
- Historical backups should not stay on the `99_notes` front page. If a backup belongs to a run, store it in that run directory under `archived_backups/`.
