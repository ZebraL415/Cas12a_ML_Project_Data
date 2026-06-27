# EasyDesign_2024 Round-2 Method Notes

Raw supplementary files were left unchanged. The second-round audit used the original paper PDF and the supporting-information screenshot to resolve round-1 unresolved questions.
Excel data were read from the combined source-data workbook as the authoritative source; standalone tables were recorded only as duplicate sources.
Tables S3, S4, and S5 were identified as training, augmentation, and test data, respectively. The Table S3 `30 min` field was retained as the primary internal-baseline label, the Table S4 `out_logk_measurement` field was retained as an optional augmentation label, and the Table S5 `true value` field was retained as an external test truth value.
Each Table S5 DNA context was mapped to a 25-nt target window by the paper-described 10-nt-flank rule when possible; non-45-nt contexts used a best-match fallback. Only basic sequence features were computed; no model was trained.
