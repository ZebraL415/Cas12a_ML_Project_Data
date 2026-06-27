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
