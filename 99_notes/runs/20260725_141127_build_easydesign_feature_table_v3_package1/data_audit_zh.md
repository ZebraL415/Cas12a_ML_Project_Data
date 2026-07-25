# Vertical3 Delta G 特征核验报告

## 结论

原 Vertical3 的四列数值可以由提交代码和 ViennaRNA 2.7.2 精确重算，但其生物学定义不能通过正式核验。问题不在软件是否执行成功，而在输入序列、方向和物理体系定义不正确。因此，原列 `dG_hybrid_full`、`dG_hybrid_seed`、`dG_self_crRNA`、`dG_self_target` 不进入 Feature Table V3；V3 改用四个明确标注为 proxy 的修正特征。

修正后的热力学块可用于受控探索，但 P1-1 未证明其具有稳定预测增益。当前决策为 **有条件保留，暂不正式晋级**。

## 核验范围

- 输入代码：`compute_deltaG_features.py`、`run_vertical3_deltaG.py`、`run_vertical3_ablation.py`、`plot_vertical3_results.py`。
- 输入数据：Vertical3 的 V2 表及含四列 Delta G 的输出表。
- 独立环境：Python 3.12.13，ViennaRNA 2.7.2，37 C，Turner 2004 RNA 参数。
- 参照数据：项目正式 V2 表、V2.1 context 表、EasyDesign 原论文和 ViennaRNA 文档。

机器核验的完整结果见 `vertical3_delta_g_audit.json`。

## 已确认事实

1. Vertical3 使用的 V2 文件与项目正式 V2 文件 SHA-256 完全一致。
2. 原输出保留了 11,992 条记录和原有列，仅增加四列，无缺失值。
3. 独立重算与原四列的最大绝对误差不超过 `1.78e-15`。
4. 原 `dG_hybrid_seed` 有 8,463/11,992 条为 0，其中 perfect-match 记录也有 69.62% 为 0。
5. 3,176 条 perfect-match 记录中，`dG_self_crRNA` 与 `dG_self_target` 100% 相同。

这些事实证明代码执行一致，但不能证明定义正确。

## 原实现为何未通过

| 问题 | 影响 |
|---|---|
| 把 25 nt `crRNA_sequence` 整列当作 crRNA | 该字段包含 4 nt PAM 表示和 21 nt spacer，不是完整物理 crRNA，也缺少 direct repeat |
| 用前 7 nt 定义 seed | 实际包含 4 nt PAM 和仅 3 nt spacer，不对应 Cas12a PAM-proximal seed |
| guide 与 target 按相同 target-oriented 字符串送入 `RNA.cofold` | 未处理 guide 的反向互补方向，配对定义失真 |
| 把 target 的 T 转为 U 并作为 RNA | EasyDesign 实验模板为 DNA，RNA-RNA 能量不能直接解释 RNA-DNA R-loop |
| 用 `RNA.cofold` 表示 hybrid | `RNAcofold` 同时允许分子内和分子间结构，不等于纯双链杂交能，更不包含 Cas12a 蛋白作用 |
| 三个 Vertical3 脚本的特征选择不一致 | 运行脚本保留 context 数值列，而消融/绘图脚本删除全部 58 个 context 特征，无法定义唯一 V3 profile |

## V3 修正热力学特征

| 特征 | 计算定义 | 解释与限制 |
|---|---|---|
| `thermo_guide_spacer_unfolding_ensemble_rna_proxy_kcal_mol` | 21 nt spacer 反向互补并转 RNA；取 ensemble free energy 的相反数 | spacer 解折叠代价 proxy；缺少 direct repeat 和蛋白结合状态 |
| `thermo_target_local_dsDNA_separation_mfe_dna_proxy_kcal_mol` | 21 nt target 与其反向互补链，Mathews 2004 DNA 参数；取 duplex MFE 的相反数 | 局部 dsDNA 打开代价 proxy；不含完整模板和 RPA 产物上下文 |
| `thermo_guide_target_full_hybrid_mfe_rna_proxy_kcal_mol` | 正确方向的 guide 与 target，用 `RNAduplex` 计算全长局部杂交 MFE | RNA-RNA 局部双链 proxy，不是 RNA-DNA 或蛋白结合 R-loop 能量 |
| `thermo_guide_target_seed6_hybrid_mfe_rna_proxy_kcal_mol` | 去除 PAM 后取 PAM-proximal 6 nt，正确方向，用 `RNAduplex` 计算 | seed 局部配对 proxy；长度依据 Cas12a seed 文献，但仍是近似量 |

列名保留 `proxy` 是强制的语义保护，不能在论文中直接写成“Cas12a R-loop Delta G”。

## 生物学依据

- EasyDesign 使用 DNA 模板、21 nt spacer 和 4 nt TTTN PAM，实验读出为 37 C 条件下的 Cas12a 荧光活性。
- Cas12a 识别涉及 PAM、PAM-proximal seed、R-loop 形成和构象激活，因此序列可及性与局部杂交稳定性具有合理生物学动机。
- 但物理上需要分别考虑 crRNA 折叠、DNA 打开和 RNA-DNA hybrid。已有 Cas12a 自由能研究也分别使用 ViennaRNA、DNA 工具和 RNA-DNA hybrid 工具，而不是把全部序列作为两个 RNA 直接 cofold。

参考：[ViennaRNA Python API](https://viennarna.readthedocs.io/en/latest/api_python.html)、[RNAcofold](https://viennarna.readthedocs.io/en/latest/man/RNAcofold.html)、[RNAduplex](https://viennarna.readthedocs.io/en/latest/man/RNAduplex.html)、[ViennaRNA energy parameters](https://viennarna.readthedocs.io/en/latest/eval/energy_parameters.html)、[Cas12a seed structure](https://pmc.ncbi.nlm.nih.gov/articles/PMC6879319/)、[Cas12a kinetic basis](https://pmc.ncbi.nlm.nih.gov/articles/PMC6679935/)、[Cas12a trans-cleavage free-energy analysis](https://academic.oup.com/nar/article/52/22/14077/7908798)、[RNA-DNA hybrid thermodynamics method](https://academic.oup.com/bioinformatics/article/28/19/2530/289009)。

## 统计检验与采用决定

修正后的四个 proxy 在 8,417 条训练记录上均无缺失，单变量 Spearman 绝对值为 0.030 至 0.112。P1-1 配对消融中，完整模型相对移除热力学块的平均 OOF Spearman 只提高 `0.000732`，5 个 seed 中 3 个为正，未达到预设的“至少 4/5 seed 为正且平均增益至少 0.005”标准。

因此：

- V3 完整表保留这四列，以支持可追溯的 Package1 和后续受控实验。
- 不把热力学块描述为已验证的重要特征。
- `nonpositional4_candidate` 表中的 thermodynamic 仅代表候选，不代表已晋级。
- 下一步若要提升物理解释，应补充完整 crRNA direct repeat、完整模板/RPA 上下文，并采用明确支持 RNA-DNA hybrid 的方法。
