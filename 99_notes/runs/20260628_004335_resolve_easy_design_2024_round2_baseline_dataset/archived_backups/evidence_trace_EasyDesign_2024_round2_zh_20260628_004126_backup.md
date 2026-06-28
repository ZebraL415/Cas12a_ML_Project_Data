# EasyDesign_2024 第二轮证据追踪

## 证据追踪
每条判断均区分证据和处理决定。

### 决定 1：Table S3 是主 baseline 内部分割来源
证据：PDF 说明 30 分钟荧光值作为活性指标；补充资料说明 Table S3 是 CRISPR fluorescence reaction 训练数据。
处理：使用 `30 min`，按 target sequence hash 生成 baseline_train/baseline_validation。

### 决定 2：Table S4 是 optional augmentation
证据：PDF 说明 20/30 分钟读数用于数据增强；补充资料说明 Table S4 是 augment dataset。
处理：单独输出 optional 文件，不并入默认 baseline。

### 决定 3：Table S5 是 external paper test
证据：补充资料说明 Table S5 是测试数据；PDF 方法部分给出 1,358 testing pairs。
处理：保留 `true value` 和 paper prediction columns，但 prediction columns 只作参考。

### 决定 4：PAM 只作推断字段
证据：PDF 讨论 TTTN PAM；Excel 无独立 PAM 列。
处理：从 5' TTTN 前缀推断 `pam`，并记录 `pam_inference_status`。
