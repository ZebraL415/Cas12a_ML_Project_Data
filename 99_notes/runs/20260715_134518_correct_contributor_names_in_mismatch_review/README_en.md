# Correct Contributor Names in the Mismatch Review

## Scope

This run only corrects how the two contributors are named in the EasyDesign mismatch contribution review. It does not change data, statistics, conclusions, or the processing roadmap.

## Replacement Rules

- Chinese: `Xu 同学` / `Xu` becomes “诗睿同学” or “诗睿”.
- Chinese: `林同学` / `林` becomes “可恩同学” or “可恩”.
- English: first mentions use `Shirui (诗睿)` and `Ke'en (可恩)`; later mentions use `Shirui` and `Ke'en`.
- Historical Git commit title `Integrate Xu engineered features` is an immutable quoted title and therefore remains unchanged.

## Files Changed

- `mismatch_contribution_review_zh.md`
- `mismatch_contribution_review_en.md`

## Boundary

No file under `01_raw/`, CSV, Excel workbook, script, model input, or audit conclusion was changed.
