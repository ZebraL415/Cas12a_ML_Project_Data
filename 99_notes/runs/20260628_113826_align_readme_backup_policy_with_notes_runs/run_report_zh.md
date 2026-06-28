# 运行报告：Align README Backup Policy With Notes Runs

## 范围

本次处理范围为根目录 `README.md` 和本运行记录目录。未修改原始数据、提取表、清洗表或候选建模数据。

## 背景

根目录 README 原先写着 `99_notes/` 的历史备份位于 `99_notes/_archive/backups/`，但当前 `99_notes/` 已采用按操作轮次组织的 `runs/` 结构，顶层 `_archive/backups/` 不存在。

## 决定

以 `99_notes/runs/YYYYMMDD_HHMMSS_<operation-title-slug>/` 作为 `99_notes/` 的历史记录主逻辑。某一轮内部反复生成的旧副本可放入该运行目录自己的 `archived_backups/`。

## 已完成修改

- 更新根目录 `README.md` 的全局原则：数据层历史备份使用 `_archive/backups/`，`99_notes/` 历史记录使用 `runs/`。
- 更新根目录 `README.md` 的 `99_notes/` 章节，移除不存在的 `99_notes/_archive/backups/` 表述。
- 更新根目录 `README.md` 的推荐使用顺序，将当前问题清单入口改为 `99_notes/current/problems_to_resolve_*.md`。
- 更新根目录 `README.md` 的协作注意事项，将问题记录入口改为 `99_notes/current/problems_to_resolve_*.md`。
- 新增本次操作的中英文运行记录。
