# Integrate Xu Engineered Features

本轮将徐同学提供的首轮特征重要性 CSV 和工程特征脚本纳入项目，使用脚本对 EasyDesign v0 特征表重新生成完整特征，核对参考改进结果，并构建推荐的 `EasyDesign_2024_diagnostic_activity_feature_table_v1.csv`。

本轮只进行审计、复算、特征筛选和数据整理，没有训练模型，也没有把 EasyDesign diagnostic activity 与 DeepCas12a editing activity 合并。

主要记录：

- `data_audit_zh.md` / `data_audit_en.md`
- `evidence_trace_zh.md` / `evidence_trace_en.md`
- `feature_selection_rationale_zh.md` / `feature_selection_rationale_en.md`
- `method_notes_zh.md` / `method_notes_en.md`
- `run_report_zh.md` / `run_report_en.md`
- `verification_results.json`
- `input_manifest.csv`
