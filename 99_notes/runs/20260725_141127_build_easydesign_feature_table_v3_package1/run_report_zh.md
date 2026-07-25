# 运行报告

## 范围

本轮只处理 EasyDesign diagnostic activity 的 V2/V2.1、Vertical3 Delta G 提交和 V3 Package1。没有修改 `01_raw/`，没有合并 editing activity，也没有训练新模型类型。

## 输入

- Vertical3 原代码和 V2 / V2-with-DG 输出。
- 项目正式 V2、V2.1 context 表、词典、block manifest 和冻结 target-grouped folds。
- EasyDesign 原论文、ViennaRNA 官方文档及 Cas12a seed/kinetic/free-energy 文献。

## 执行

1. 在 ViennaRNA 2.7.2 下独立重算原四列并进行定义审查。
2. 因原定义未通过，按正确 guide 方向、PAM 排除和 seed6 定义构建四个明确标记为 proxy 的修正特征。
3. 继承 V2.1 的行、标签、split、来源和 188 个候选输入，构建 192 特征 V3。
4. 生成完整 V3 与非位置四块候选表、词典、block manifest、QC 和哈希清单。
5. 在本地综合项目中运行 P1-0 固定验证和 P1-1 六块 grouped ablation。

## 输出与检查

- 完整 V3：11,992 x 250；SHA-256 `3701482e61fbdb0fb30af2173fa0911154329b12555552592dbe37d2e72ed89a`。
- 非位置四块候选表：11,992 x 143；85 个候选特征。
- 父表列值、record order、label 和 split 全部保持；热力学四列无缺失。
- P1-0 固定验证 Spearman 0.7702。
- P1-1 完整模型 OOF Spearman 0.73762 +/- 0.00106。
- context、substitution、alignment 是最有支持的三块；thermodynamic 未达到晋级阈值。

## 分类判断

- 原 Delta G：数值重算通过，生物学定义未通过，**不采用**。
- 修正 thermodynamic proxy：**有条件采用**，保留在 V3 供受控实验，不宣称已验证。
- V3 完整表：**采用为 Package1 和 Horizontal 新基线输入**。
- nonpositional4 表：**候选遴选表**，不是默认训练表。

## 下一步

固定 P1-0，优先开展紧凑位置编码、核心三块对照和 gap 子集稳健性实验。每个 Horizontal 实验只改变一个模块。
