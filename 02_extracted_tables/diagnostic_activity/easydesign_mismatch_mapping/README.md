# EasyDesign mismatch 来源映射中间表

本目录保存从 EasyDesign combined supplementary workbook 原样拆出并附加追溯字段的中间表，不是最终训练集。

- `EasyDesign_2024_TableS3_alignment_preserved_raw.csv`：Table S3 原始训练行，保留 `target_at_guide` 中的 `-`。
- `EasyDesign_2024_TableS2_template_groups_raw.csv`：Table S2 的 198 条模板及 22 x 9 分组、组内角色和长度 QC。
- `EasyDesign_2024_TableS2_TableS3_mapping_hits_raw.csv`：Table S3 到 Table S2 的全部精确或 IUPAC 兼容窗口命中；同分命中没有被丢弃。

这些映射只用于来源追溯、分组和复核，不能作为实验标签，也不应默认作为模型特征。清洗后的行级结果位于 `03_cleaned_minimal/easydesign_mismatch/`。
