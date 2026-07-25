# V2-1 三层实验最终汇总

## 结论摘要

本轮结论为：**正式晋级 `sequence_context`，冻结五个特征块共 188 个名义输入；每次训练仍须在训练折内去除常数列，本次为 183 个实际输入。** 该决定同时得到训练集内部 target-grouped 多 seed 证据和 Table S5 外部排序证据支持。V2 gap-aware core 继续保留为不可覆盖的父版本与对照组。

## 第一层：版本化特征表

- 生成 `v2.1_context` 候选表：11,992 行 × 246 列。
- 新增 58 个 `sequence_context` 特征；总候选输入从 130 增至 188。
- 所有新增值仅来自 `crRNA_sequence` 与 `target_ungapped`。
- `target_aligned_25`、mismatch/gap 位置、标签、来源、split 和记录顺序未修改。
- 两套 QC 全部通过，父表列逐值保持一致。

## 第二层：V2-1 五块消融

在 8,417 条 `baseline_train` 上复用冻结的 5 折 target 分组，seeds 为 7、21、42、84、2024，共拟合 150 个模型；固定 validation 与 Table S5 均未参与选择。

- 完整 188 特征 OOF Spearman：0.736887 ± 0.000842。
- V2 core 130 特征 OOF Spearman：0.671385 ± 0.000752。
- `sequence_context` 平均增益：0.065502；5/5 seeds 为正。
- MAE 改善：0.034527；RMSE 改善：0.044689。

| Block                |   Removed |   Spearman loss |   MAE worsening | Rule result        |
|:---------------------|----------:|----------------:|----------------:|:-------------------|
| pair_alignment       |        11 |        0.010705 |        0.012050 | retained_important |
| pair_position        |        75 |        0.000415 |        0.000570 | retained_important |
| substitution_type    |        12 |        0.013076 |        0.006624 | retained_important |
| sequence_composition |        32 |        0.002152 |        0.000772 | retained_important |
| sequence_context     |        58 |        0.065502 |        0.034527 | retained_important |

`sequence_context` 是贡献最大的块；`pair_alignment` 与 `substitution_type` 有中等、稳定贡献。`pair_position` 和 `sequence_composition` 按预注册规则保留，但 Spearman 损失仅 0.000415 和 0.002152，应理解为边际证据，不宜宣称强生物学重要性。不同块大小差异很大，消融差值也不能直接解释成单特征重要度。

## 第三层：Table S5 外部验证

在特征冻结后，用全部 10,634 条 Table S3 开发记录训练，并只在 1,358 条 Table S5 上评估。因两表标签尺度未确认一致，只报告 Spearman 与 Pearson，不报告跨尺度误差。

| variant       |   n_features |    n |   spearman_rho |   pearson_r |
|:--------------|-------------:|-----:|---------------:|------------:|
| core_v2       |          130 | 1358 |       0.401283 |    0.454384 |
| full_v2_1     |          188 | 1358 |       0.440410 |    0.505258 |
| selected_v2_1 |          188 | 1358 |       0.440410 |    0.505258 |

- full v2.1 相对 core v2 的五-seed集成 Spearman 增益：0.039127。
- 5/5 seeds 均为正，平均 seed 增益：0.038455。
- 病毒子集 full v2.1 Spearman 为 0.571260；细菌子集为 0.264193，提示跨物种类型泛化仍不均衡。
- 21 条非 45 nt 上下文只作敏感性描述，样本太少，不能形成稳健结论。

V2 归一化后发现 10 条 Table S5 记录的 25 nt `target_ungapped` 局部窗口与 Table S3 相同，共 4 个唯一窗口。这不等同于论文定义的完整 DNA template/target 重叠。排除这 10 条后，full 相对 core 的 Spearman 增益仍为 0.039263，因此晋级结论不依赖这些记录。

## 与原表模型列的关系

| published_prediction_column   |   n_missing_or_dash |    n |   spearman_rho |   pearson_r |
|:------------------------------|--------------------:|-----:|---------------:|------------:|
| CNND                          |                 499 |  859 |       0.620642 |    0.554645 |
| CNN12a                        |                 496 |  862 |       0.656868 |    0.600012 |
| CNN12ae                       |                   0 | 1358 |       0.812438 |    0.716092 |
| TransformerD                  |                 496 |  862 |       0.532478 |    0.476383 |
| Transformer12a                |                 496 |  862 |       0.541746 |    0.440071 |
| Transformer12ae               |                 496 |  862 |       0.467465 |    0.416919 |

重算值与论文所述测试层次相符：`CNN12a` 只在 862 条有值记录上约为 0.657，而 `CNN12ae` 在完整 1,358 条增强测试记录上约为 0.812。当前 full v2.1 的 0.440 高于自己的 core 对照，但明显未达到作者增强系统；两者训练数据扩增、特征/编码和测试覆盖不同，因此只能作为差距参照，不能当成同配置直接竞赛。

## 最终使用规则

1. 使用 `v2_1_final_feature_manifest.csv` 中 `selected_v2_1` 的 188 个名义输入，不按 Table S5 结果再次筛特征。
2. 每个训练折只用该折训练数据计算中位数；仍缺失则填 0；随后只移除该折训练数据中的常数列。
3. mismatch/gap 位置继续严格来自 `target_aligned_25`；组成和上下文特征来自无 gap 序列，二者不得互换。
4. 新模型比较继续采用 target-grouped split，并分别报告整体、virus/bacteria 与非 45 nt 敏感性结果。

## 限制

本轮证明 `sequence_context` 对当前固定 XGBoost workflow 有稳定预测价值，但没有证明任何 k-mer 或 GC 特征具有因果作用。细菌子集表现偏低、局部窗口重合以及 Table S3/S5 数值尺度差异仍需在后续外部数据中继续检验。
