# 数据划分计划

## Split Plan
- Table S3 被划分为 baseline_train=8417 行和 baseline_validation=2217 行。
- 划分方法：对 `target_sequence` 做 SHA1 hash，并按 bucket < 80 进入训练集，其余进入验证集。
- 目的：降低同一 target sequence 同时出现在训练和验证中的风险。
- Table S5 保留为 external_test_scale_unconfirmed=1358 行；在 label scale 未确认前不作为默认测试集。
- Table S4 保留为 optional_augmentation=31993 行；默认 baseline 不使用。
