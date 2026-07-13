# 徐同学贡献文件

本目录保存徐同学提供的原始工程特征生成脚本，文件内容按收到时原样保留。

- `generate_validated_engineered_features.py`
- 原接收路径：`/Users/linzibo/Documents/generate_validated_engineered_features.py`
- SHA-256：`cf8cd2f62eb8759e8fa311892bb8791425d2dec5c1b90e3df94d48e95e1a1830`

脚本读取 EasyDesign 特征表，比较 direct、complement、reverse 和 reverse-complement 四种表示，选择最能复现现有计算 Hamming 列的模式，并生成 139 个工程特征及 QC 文件。

使用边界：该过程验证的是与项目既有计算列的一致性，不等于独立确认生物学链方向。脚本对未对齐的位置填 `0`；最终 v1 表由 `scripts/build_easydesign_feature_table_v1.py` 将这些位置改为空值，并执行去冗余筛选。不要直接修改本目录中的贡献脚本；改进逻辑应放在新的项目脚本中。
