# 可复现脚本

本目录保存项目数据审计、清洗、候选表生成和验证脚本。脚本只能读取 `01_raw/`，输出必须写入 `02_extracted_tables/`、`03_cleaned_minimal/`、`04_candidate_ml_dataset/` 或对应 `99_notes/runs/`。

## EasyDesign

- `inspect_easy_design.py`：第一轮 workbook/sheet 审计。
- `resolve_easy_design_round2.py`：结合论文证据构建 baseline v0。
- `build_easydesign_alignment_v2.py`：保留 Table S3 gap 对齐、重建 Table S2 22 x 9 模板组，并保存全部精确/IUPAC 来源命中。
- `build_easydesign_feature_table_v2.py`：从 alignment v2 和 v0 生成 gap-aware feature table v2、特征词典和 QC。
- `verify_easydesign_v2.py`：独立检查行数、坐标、事件计数、标签/split 保真和 pair-level split 泄漏。

从项目根目录运行：

```bash
python3 scripts/build_easydesign_alignment_v2.py --root . --run-dir 99_notes/runs/<run_id>
python3 scripts/build_easydesign_feature_table_v2.py --root . --run-dir 99_notes/runs/<run_id>
python3 scripts/verify_easydesign_v2.py --root . --run-dir 99_notes/runs/<run_id>
```

运行前后应检查 `git status -- 01_raw` 为空。脚本版本及其 SHA-256 应写入对应 run 的 `script_manifest.csv`。
