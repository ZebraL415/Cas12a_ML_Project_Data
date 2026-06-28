# Run Report: Align README Backup Policy With Notes Runs

## Scope

This operation covers the root `README.md` and this run record directory. It does not modify raw data, extracted tables, cleaned tables, or candidate modeling datasets.

## Background

The root README previously stated that historical backups for `99_notes/` were stored in `99_notes/_archive/backups/`, but the current `99_notes/` organization uses per-operation `runs/` directories and does not have a top-level `_archive/backups/`.

## Decision

Use `99_notes/runs/YYYYMMDD_HHMMSS_<operation-title-slug>/` as the main historical-record logic for `99_notes/`. Old copies produced by repeated runs within one operation may be stored in that run directory under `archived_backups/`.

## Changes made

- Updated the root `README.md` global rule: data-layer historical backups use `_archive/backups/`, while `99_notes/` historical records use `runs/`.
- Updated the root `README.md` `99_notes/` section to remove the nonexistent `99_notes/_archive/backups/` path.
- Updated the root `README.md` recommended usage order so the current question-list entry points to `99_notes/current/problems_to_resolve_*.md`.
- Updated the root `README.md` collaboration notes so the question-record entry points to `99_notes/current/problems_to_resolve_*.md`.
- Added Chinese and English run records for this operation.
