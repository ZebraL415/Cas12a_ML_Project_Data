<!-- BEGIN EasyDesign_2024 -->
## EasyDesign_2024

- 确认 `30 min` 与 `20 min normalized` 的准确单位和转换关系：它们是否均为实验荧光/活性读数，还是一个为归一化派生标签？
- 确认 `out_logk_measurement` 是否由同一实验读数转换而来，是否可作为 primary diagnostic activity label。
- 确认 `true value` 在 Test data/Table S5 中的来源：是否为实验测量值，以及是否与训练集标签处在同一尺度。
- 确认 standalone workbooks (`Table S1.xlsx`-`Table S4.xlsx`) 与 combined source-data workbook (`imt2214-sup-0002...xlsx`) 的重复关系，后续清洗时只保留哪一套来源。
- Figure source data 中的 normalized fluorescence/fluorescence unit 是否能映射回具体 crRNA-target pair；当前不能直接作为 tidy training rows。
- README/代码中的 `guide-expected-activities` 是模型预测输出，不能当作实验标签；若后续使用，需要明确作为 predicted_library 或辅助特征。
- 未在当前 Excel 结构中发现明确 PAM 列；需要确认 Cas12a PAM 是否隐含在 target/context sequence 中。
- 人工确认 imt2214-sup-0002-tables1-9sourcedata (1).xlsx / Fig.S3 的内容类型和标签含义。
<!-- END EasyDesign_2024 -->

<!-- BEGIN EasyDesign_2024_ROUND2 -->
## EasyDesign_2024 Round2

- Table S3 的负值 `30 min` 标签与 Table S5 的正值 `true value` 是否可通过已知转换映射到同一尺度，仍需人工确认或方法学决定。
- Table S3 原始 `guide_target_hamming_dist` 与从 `guide_seq`/`target_at_guide` 直接计算的 mismatch 并不总一致；该原始列的真实语义仍需确认。
- Excel 中没有明确独立 PAM 列；当前 PAM 仅根据 TTTN 前缀推断，后续若要作为模型特征需要确认序列定义。
- Table S4 增强数据是否进入首个正式训练流程，需要在模型方案确定后决定。
- Table S3 只有 type1/type2，不含具体 pathogen 名称；如果要做物种分组验证，需要额外映射。
<!-- END EasyDesign_2024_ROUND2 -->
