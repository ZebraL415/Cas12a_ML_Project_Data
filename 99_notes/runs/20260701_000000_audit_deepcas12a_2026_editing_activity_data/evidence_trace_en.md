# DeepCas12a_2026 Evidence Trace

## Decision: DeepCas12a belongs to editing_activity

Evidence:
- The paper title and abstract describe AsCas12a efficiency prediction.
- The methods describe AsCas12a on-target cleavage/editing efficiency data.
- The GitHub README describes the task as AsCas12a on-target guide efficiency prediction.

Reasoning:
The source describes Cas12a editing/cleavage efficiency, not CRISPR diagnostics fluorescence readouts.

Remaining uncertainty:
None; `path_type` is `editing_activity`.

## Decision: `label` is a binary editing activity label

Evidence:
- `Dataset/README.md` states that the label is binary, with `0` for low activity and `1` for high activity.
- `Data_Descriptions.txt` states that `1` indicates high activity and `0` indicates low activity.
- The paper methods state that binary labels were assigned using thresholds on background-corrected indel frequencies.

Reasoning:
This column can be used as a primary binary classification label, but it is not a continuous indel frequency and not fluorescence/RFU.

Remaining uncertainty:
The original continuous indel frequency values are not included in the current model-ready repository.

## Decision: The 34 bp sequence is a target-context sequence

Evidence:
- The README and Dataset documentation define the sequence as 4 bp upstream context + PAM + 23 bp protospacer + 3 bp downstream context.
- The paper methods describe 34 bp target sequences.

Reasoning:
PAM can be inferred from positions 5-8 and protospacer from positions 9-31. There is no independent crRNA sequence column.

Remaining uncertainty:
If crRNA sequences are needed later, strand orientation and complement rules must be confirmed before derivation.
