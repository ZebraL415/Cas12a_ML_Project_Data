# 证据链

## 判断：原 Vertical3 四列不进入正式 V3

- 文件证据：原 V2 与正式 V2 SHA-256 一致；原输出仅新增四列且可精确重算。
- 代码证据：输入包含 PAM 的 25 nt 表示，seed 取前 7 nt，guide 未反向互补，target 被当作 RNA，调用 `RNA.cofold`。
- 文档证据：RNAcofold 描述两个 RNA 的共同二级结构，不是 RNA-DNA Cas12a R-loop 模型。
- 剩余不确定性：完整 crRNA direct repeat 和模板上下文不可得。

## 判断：采用四个修正 proxy

- 论文证据：EasyDesign 使用 4 nt TTTN PAM、21 nt spacer、DNA 模板和 37 C 荧光反应。
- 文献证据：Cas12a seed 位于 PAM-proximal spacer；自由能分析应区分 RNA 折叠、DNA 打开和 RNA-DNA hybrid。
- 实现证据：V3 明确分离 spacer、校正方向、排除 PAM，并把结果标记为 proxy。
- 剩余不确定性：proxy 不能替代真实蛋白结合 R-loop 能量。

## 判断：thermodynamic 有条件保留

- P1-1 证据：平均 OOF Spearman 增益 0.000732，3/5 seed 为正，低于至少 4/5 且增益 0.005 的预设阈值。
- 决策：保留列供可追溯受控实验，不宣称已经验证或高影响。
