# 01_raw

This directory is the raw data warehouse. It stores original source files such as paper PDFs, supplementary tables, GitHub repositories, README files, source data, and archives.

## Core rules

- Raw files are read-only. Do not rename, overwrite, clean, or directly modify them.
- Processing scripts may read from this directory, but outputs should be written to `02_extracted_tables/`, `03_cleaned_minimal/`, or `04_candidate_ml_dataset/`.
- If the meaning of a raw file needs documentation, write it in `00_data_catalog/` or `99_notes/` instead of editing the original source file.

## Current source subdirectories

- `DeepCpf1_Kim2018/`
- `DeepCas12a_2026/`
- `EasyDesign_2024/`
- `AdvancedScience_2025/`
- `ARTEMIS_2024/`
- `HEPSD_NAR2025/`
- `Iterative_PAMfree_2024/`

## Note

This README is a project-level usage note. It is not part of any original paper or database material.
