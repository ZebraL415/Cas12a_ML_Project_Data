# Reproducible Scripts

This directory stores project scripts for data audit, cleaning, candidate-table generation, and verification. Scripts may only read `01_raw/`; outputs must be written to `02_extracted_tables/`, `03_cleaned_minimal/`, `04_candidate_ml_dataset/`, or the corresponding `99_notes/runs/` directory.

## EasyDesign

- `inspect_easy_design.py`: first-round workbook/sheet audit.
- `resolve_easy_design_round2.py`: paper-evidence-based baseline v0 builder.
- `build_easydesign_alignment_v2.py`: preserves Table S3 gaps, rebuilds the Table S2 22 x 9 template groups, and saves all exact/IUPAC source hits.
- `build_easydesign_feature_table_v2.py`: builds gap-aware feature table v2, the feature dictionary, and QC from alignment v2 and v0.
- `verify_easydesign_v2.py`: independently checks rows, coordinates, event counts, label/split preservation, and pair-level split leakage.

Run from the project root:

```bash
python3 scripts/build_easydesign_alignment_v2.py --root . --run-dir 99_notes/runs/<run_id>
python3 scripts/build_easydesign_feature_table_v2.py --root . --run-dir 99_notes/runs/<run_id>
python3 scripts/verify_easydesign_v2.py --root . --run-dir 99_notes/runs/<run_id>
```

Before and after execution, confirm that `git status -- 01_raw` is empty. Record script versions and SHA-256 values in the run's `script_manifest.csv`.
