# Problems To Resolve DeepCas12a_2026

## Confirmed

- DeepCas12a belongs to `editing_activity`, not `diagnostic_activity`.
- `label` is a binary AsCas12a on-target activity label and must not be treated as fluorescence/RFU.
- The 34 bp `sequence` is a target-context sequence containing upstream context, PAM, protospacer, and downstream context.
- The HT methylation/DNase features are standardized model inputs according to the repository documentation and should not be interpreted as true epigenetic states at unknown integration loci.

## Still Needs Confirmation

- The repository provides model-ready binary labels only; continuous indel frequencies require tracing back to the original Kim et al. values.
- PAM/protospacer can be inferred from the 34 bp target-context sequence, but there is no independent crRNA sequence; crRNA derivation requires strand and complement-rule confirmation.
- HEK in situ A/N epigenetic feature calls should be discussed separately from HT standardized features in downstream model interpretation.
