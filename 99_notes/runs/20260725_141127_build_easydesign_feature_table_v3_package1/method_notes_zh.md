# 方法记录

原 Vertical3 输出首先在隔离环境中使用 ViennaRNA 2.7.2 独立重算。数值一致性通过 SHA-256、行顺序、父列保真、缺失值和 `allclose(atol=1e-6)` 检查；生物学定义依据 EasyDesign 实验设计、字段语义和 ViennaRNA 算法边界单独审查。

Feature Table V3 以 V2.1 context 表为不可变父表。21 nt spacer 从含 PAM 的 25 nt 表示中分离；guide 按 target-oriented 存储约定反向互补。RNA unfolding 使用 Turner 2004 ensemble free energy，局部 DNA duplex 使用 Mathews 2004 参数，full 和 PAM-proximal seed6 pairing 使用 `RNAduplex`。所有四列均以 `proxy` 命名并记录限制。父表所有列和记录顺序保持不变。

P1-0 使用固定 8,417/2,217 split、seed 42 和原 XGBoost 参数。P1-1 仅在 8,417 条训练记录内使用冻结 target-grouped 5 折和 5 个 seed，每次移除一个特征块，共拟合 175 个模型。固定验证和 Table S5 均不参与特征块选择。
