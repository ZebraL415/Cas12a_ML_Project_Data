# 回退 Xu 直接合并并审计错配贡献

## 本轮范围

本轮回退提交 `fa8d67b Integrate Xu engineered features`，并审计 Xu 同学与林同学针对 EasyDesign 错配信息的处理。Git 使用 `revert` 保留完整历史，没有重写提交历史。

## 状态

- 回退提交：`653fb6f Revert "Integrate Xu engineered features"`
- 回退后的文件树与 `6a6535a Organize candidate ML datasets by source path` 一致。
- EasyDesign 默认候选数据恢复为 v0；原 Xu 整合结果仍可从 Git 提交 `fa8d67b` 审计或择项恢复。
- 未修改 `01_raw/`，未训练模型，未把不同标签体系合并。

## 文件

- `mismatch_contribution_review_zh.md`：两位同学方法的证据、相互印证、局限和采用边界。
- `mismatch_integration_roadmap_zh.md`：修复、验证、分层整合到总数据表的实施路线。
- `run_report_zh.md`：本轮输入、操作、输出和 Git 状态。
- `problems_to_resolve_zh.md`：本轮结束时的活动问题快照。
- 对应英文文件使用 `_en.md`；中英文内容一一对应。

## 当前决定

现有 Xu v1 合并表和林同学 `mismatch_wide_table.xlsx` 均不作为默认训练入口。后续应从原始 Table S3 的 25 位含缺口对齐重新构建 mismatch v2，再把经验证的序列特征和来源映射作为分层字段加入新的候选表，不能覆盖 v0。
