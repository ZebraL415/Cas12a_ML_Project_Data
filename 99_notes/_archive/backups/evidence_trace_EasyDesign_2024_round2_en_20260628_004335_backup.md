# EasyDesign_2024 Round-2 Evidence Trace

## Evidence Trace
Each decision separates evidence from the processing action.

### Decision 1: Table S3 is the primary internal-baseline source
Evidence: the PDF states that the 30-minute fluorescence value was used as the activity indicator; the supplement describes Table S3 as CRISPR fluorescence-reaction training data.
Action: use `30 min` and create baseline_train/baseline_validation by target-sequence hash.

### Decision 2: Table S4 is optional augmentation
Evidence: the PDF describes 20/30-minute readouts for data augmentation; the supplement describes Table S4 as the augment dataset.
Action: output a separate optional file and exclude it from the default baseline.

### Decision 3: Table S5 is the external paper test
Evidence: the supplement describes Table S5 as test data; the PDF methods give 1,358 testing pairs.
Action: keep `true value` and paper prediction columns, but use prediction columns only as references.

### Decision 4: PAM is an inferred field only
Evidence: the PDF discusses a TTTN PAM; Excel has no separate PAM column.
Action: infer `pam` from the 5-prime TTTN prefix and record `pam_inference_status`.
