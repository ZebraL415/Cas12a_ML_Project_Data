# Revert Xu Direct Merge and Audit Mismatch Contributions

## Scope

This run reverts commit `fa8d67b Integrate Xu engineered features` and audits the EasyDesign mismatch processing contributed by Xu and Lin. Git `revert` preserves the complete history and does not rewrite commits.

## Status

- Revert commit: `653fb6f Revert "Integrate Xu engineered features"`
- The reverted file tree matches `6a6535a Organize candidate ML datasets by source path`.
- The default EasyDesign candidate dataset is restored to v0. The former Xu integration remains auditable and selectively recoverable from Git commit `fa8d67b`.
- `01_raw/` was not modified, no model was trained, and different label systems were not merged.

## Files

- `mismatch_contribution_review_en.md`: evidence, mutual corroboration, limitations, and adoption boundaries for both contributions.
- `mismatch_integration_roadmap_en.md`: implementation sequence for correction, validation, and layered integration into the master dataset.
- `run_report_en.md`: inputs, actions, outputs, and Git status for this run.
- `problems_to_resolve_en.md`: snapshot of active unresolved questions at the end of this run.
- Chinese counterparts use `_zh.md` or `README.md`; the two languages correspond section by section.

## Current Decision

Neither the former Xu v1 merged table nor Lin's `mismatch_wide_table.xlsx` is a default training entry point. Mismatch v2 should be rebuilt from the original 25-position, gap-preserving Table S3 alignment. Only validated sequence features and source mappings should then be added as layered fields in a new candidate table without overwriting v0.
