<!-- BEGIN EasyDesign_2024 -->
## EasyDesign_2024 Data Audit Method

Raw supplementary files were stored without modification. Excel workbooks were programmatically scanned using Python, pandas, and openpyxl. Each worksheet was indexed by file name, sheet name, dimensions, detected header row, first columns, and representative values. Sheets were classified by data type based on detected sequence fields, candidate label fields, source documentation, sheet names, and table captions. Experimentally measured diagnostic activity candidates were exported only as raw traceable CSV tables under `02_extracted_tables/diagnostic_activity/`; no final training dataset was built and no model was trained. Predicted activity scores and model outputs were recorded separately from measured labels.
<!-- END EasyDesign_2024 -->
