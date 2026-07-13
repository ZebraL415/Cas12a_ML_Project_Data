# 参考改进结果

本目录复制自 `/Users/linzibo/Desktop/MLRS/improved_feature_outputs/`，用于核对工程特征的潜在价值。

已确认事实：2,217 条预测全部对应现有 `baseline_validation`；record ID、crRNA、target 和标签逐行完全匹配；由预测重算得到 Spearman 0.765651、Pearson 0.747238、MAE 0.327815、RMSE 0.424830、R2 0.554858，与 JSON 一致。保存的 residual 与重算值最大差 `1.19e-7`，属于输出精度舍入。

复现边界：未提供训练代码、模型参数、依赖锁定和随机种子；特征名与徐同学生成器存在重命名差异，并含重复或线性等价特征。因此本目录只能证明保存结果内部一致，不能证明训练过程已独立复现，也不能据此确定最终模型。
