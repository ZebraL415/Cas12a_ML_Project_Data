# 00_data_catalog

本目录是项目的数据导航中心，只保存索引、词典和数据源级说明，不保存原始实验文件。

## 应先查看的文件

- `master_data_catalog.xlsx`：数据源级目录。一行代表一个数据源，用于判断来源、路径类型、标签状态、是否可训练。
- `source_sheet_index.xlsx`：Excel sheet 级目录。一行代表一个 workbook sheet，用于追踪 sheet 名、行列数、示例值、初步分类和导出建议。
- `label_dictionary.xlsx`：标签词典。用于区分实验标签、预测分数、注释字段和元数据字段。

## 使用原则

- 新增数据源时，先在这里登记，再导出表格到 `02_extracted_tables/`。
- 不要把不同 label system 混写成同一个标签。
- 对字段含义没有把握时，在 `99_notes/problems_to_resolve.md` 记录问题。

## 归档

历史备份文件统一放在 `_archive/backups/`。目录首页只保留当前有效版本。
