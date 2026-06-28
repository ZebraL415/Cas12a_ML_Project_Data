# EasyDesign_2024 第二轮方法记录

原始补充文件保持不变。第二轮审计使用原论文 PDF 和补充资料截图校对上一轮 unresolved questions。
Excel 数据以 combined source-data workbook 为权威来源读取；standalone 表只作为重复来源记录。
Table S3、Table S4、Table S5 分别被识别为训练、增强和测试数据。Table S3 的 `30 min` 被保留为主 baseline 内部标签，Table S4 的 `out_logk_measurement` 被保留为可选增强标签，Table S5 的 `true value` 被保留为外部测试真值。
Table S5 的 45 nt DNA context 被程序化定位到与 crRNA 最匹配的 25 nt target window。仅计算基础序列特征；未训练模型。
