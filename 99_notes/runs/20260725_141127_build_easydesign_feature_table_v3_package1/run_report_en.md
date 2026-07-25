# Run Report

## Scope

This run covers only EasyDesign diagnostic-activity V2/V2.1, the submitted Vertical3 Delta G work, and V3 Package1. It does not modify `01_raw/`, merge editing activity, or train a new model family.

## Inputs

- Submitted Vertical3 code and V2 / V2-with-DG outputs.
- Canonical project V2, V2.1 context table, dictionaries, block manifest, and frozen target-grouped folds.
- The EasyDesign paper, official ViennaRNA documentation, and Cas12a seed, kinetic, and free-energy literature.

## Actions

1. Independently recomputed the four submitted columns under ViennaRNA 2.7.2 and audited their definitions.
2. Because the submitted definitions failed, built four explicitly named proxy features using corrected guide orientation, PAM exclusion, and a seed6 definition.
3. Inherited V2.1 rows, labels, splits, provenance, and 188 candidate inputs and built a 192-feature V3 table.
4. Generated the complete V3 table, non-position four-block candidate table, dictionary, block manifests, QC, and hash manifest.
5. Ran P1-0 fixed validation and P1-1 six-block grouped ablation in the integrated local project.

## Outputs and Checks

- Complete V3: 11,992 x 250; SHA-256 `3701482e61fbdb0fb30af2173fa0911154329b12555552592dbe37d2e72ed89a`.
- Non-position four-block candidate table: 11,992 x 143 with 85 candidate features.
- Parent values, record order, labels, and splits are preserved; the four thermodynamic columns are complete.
- P1-0 fixed-validation Spearman: 0.7702.
- P1-1 full-model OOF Spearman: 0.73762 +/- 0.00106.
- Context, substitution, and alignment are best supported; thermodynamics fails promotion.

## Classification Decisions

- Submitted Delta G: numerically reproducible, biologically invalid, **not adopted**.
- Corrected thermodynamic proxies: **conditionally adopted** for controlled V3 experiments, not presented as validated features.
- Complete V3 table: **adopted as the Package1 and Horizontal baseline input**.
- Nonpositional4 table: **candidate-selection table**, not the default training table.

## Next Step

Freeze P1-0 and prioritize compact position encoding, a core-three-block comparator, and gap-subset robustness. Each Horizontal experiment should change one module only.
