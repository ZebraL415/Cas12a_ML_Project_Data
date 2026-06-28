# 99_notes

本目录保存审计、证据、问题和决策记录。它解释数据为什么这样整理，不存放训练数据。

## 顶层结构

- `current/`：当前仍在使用的活动问题、会议记录和论文数据备注。
- `runs/`：每一次数据整理、目录调整或 Git 上传的独立记录目录。
- `README.md` / `README_en.md`：本目录使用说明。

## 运行目录命名规则

所有新运行目录统一命名为：

`runs/YYYYMMDD_HHMMSS_<operation-title-slug>/`

规则如下：

- `YYYYMMDD_HHMMSS` 使用本次操作开始或提交前确认的本地时间。
- `<operation-title-slug>` 使用 Git commit 标题或本次操作主标题的小写下划线形式。
- 若本次操作会提交到 Git，commit 标题应与目录主标题一致，例如 `Reorganize notes into run directories` 对应 `reorganize_notes_into_run_directories`。
- 每个运行目录至少包含 `README.md` 和 `README_en.md`；如有审计、运行报告、证据链、方法记录或待解决问题，应分别使用 `data_audit_*`、`run_report_*`、`evidence_trace_*`、`method_notes_*`、`problems_to_resolve_*` 命名。

## 当前记录

- 当前待解决问题：`current/problems_to_resolve_zh.md` 和 `current/problems_to_resolve_en.md`。
- 当前会议决策：`current/meeting_decisions_zh.md` 和 `current/meeting_decisions_en.md`。
- 当前论文数据备注：`current/paper_data_notes_zh.md` 和 `current/paper_data_notes_en.md`。

## 使用原则

- 不确定问题写入 `current/`，不要在数据表里猜测。
- 每轮整理和每次 Git 上传都应在 `runs/` 下建立一个独立目录。
- 同一轮中的中英文说明文件应保持一一对应。
- 历史备份不放在 `99_notes` 首页；若备份属于某次运行，应放入该运行目录的 `archived_backups/`。
