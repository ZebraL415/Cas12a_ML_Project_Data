# Git 操作记录：Organize Backups And Add Directory Guides

## Git 信息

- 时间：2026-06-28 10:52:40 +0800
- commit：`d4bbe55`
- commit 标题：`Organize backups and add directory guides`
- 分支：`main`
- 远端：`origin/main`

## 操作内容

- 将 75 个历史备份文件移入对应目录的 `_archive/backups/`。
- 在 `00_data_catalog/`、`01_raw/`、`02_extracted_tables/`、`03_cleaned_minimal/`、`04_candidate_ml_dataset/` 和 `99_notes/` 下新增中英文 README。
- 更新根目录 README，说明首页只保留当前有效文件，历史备份进入 `_archive/backups/`。

## 注意

该次操作没有修改 `01_raw` 中已有原始来源文件；只在 `01_raw` 下新增项目层面的 README。
