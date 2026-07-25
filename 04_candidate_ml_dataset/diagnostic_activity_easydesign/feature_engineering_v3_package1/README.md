# Feature Table V3

本目录存放 EasyDesign diagnostic activity 的正式 V3 候选特征数据。

- `EasyDesign_2024_diagnostic_activity_feature_table_v3.csv`：11,992 x 250，继承 V2.1 并新增四个 thermodynamic proxy；正式 192 特征见 block manifest。
- `EasyDesign_2024_diagnostic_activity_feature_table_v3_nonpositional4_candidate.csv`：保留 metadata/label 和 alignment、substitution、context、thermodynamic 四块，共 85 个候选特征。
- `EasyDesign_2024_feature_dictionary_v3.csv`：逐列定义、公式、输入序列和限制。
- `EasyDesign_2024_feature_block_manifest_v3.csv`：六块正式候选清单，训练时必须以此选列。
- `EasyDesign_2024_nonpositional4_feature_manifest_v3.csv`：非位置四块候选清单。
- `EasyDesign_2024_feature_table_v3_qc.json`：继承、缺失、唯一性和基本统计检查。
- `v3_output_manifest.json`：输出路径、大小和 SHA-256。

`nonpositional4` 只描述结构，不代表四块均已证明为高影响；热力学块尚未正式晋级。
