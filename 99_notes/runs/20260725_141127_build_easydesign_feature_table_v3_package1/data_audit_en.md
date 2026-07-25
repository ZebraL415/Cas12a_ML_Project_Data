# Vertical3 Delta G Feature Audit

## Verdict

The four submitted Vertical3 columns are numerically reproducible with the submitted code and ViennaRNA 2.7.2, but their biological definitions fail formal validation. The issue is not software execution; it is the definition of the input sequences, orientation, and physical system. The original `dG_hybrid_full`, `dG_hybrid_seed`, `dG_self_crRNA`, and `dG_self_target` columns are therefore excluded from Feature Table V3 and replaced by four explicitly named proxy features.

The corrected thermodynamic block is suitable for controlled exploration. P1-1 did not demonstrate a stable predictive gain, so the current decision is **retain conditionally; do not formally promote**.

## Audit Scope

- Submitted code: `compute_deltaG_features.py`, `run_vertical3_deltaG.py`, `run_vertical3_ablation.py`, and `plot_vertical3_results.py`.
- Submitted data: the Vertical3 V2 input and its four-column Delta G output.
- Independent environment: Python 3.12.13, ViennaRNA 2.7.2, 37 C, Turner 2004 RNA parameters.
- References: the canonical project V2 table, V2.1 context table, the EasyDesign paper, and ViennaRNA documentation.

The complete machine-readable audit is in `vertical3_delta_g_audit.json`.

## Confirmed Facts

1. The Vertical3 V2 input and the canonical project V2 table have identical SHA-256 hashes.
2. The submitted output preserves all 11,992 records and base columns and adds exactly four complete columns.
3. Independent recomputation matches all four submitted columns with a maximum absolute difference below `1.78e-15`.
4. The submitted `dG_hybrid_seed` is zero for 8,463/11,992 records and for 69.62% of perfect-match records.
5. `dG_self_crRNA` equals `dG_self_target` for 100% of the 3,176 perfect-match records.

These results establish execution consistency, not biological validity.

## Why the Submitted Definition Failed

| Issue | Consequence |
|---|---|
| The complete 25-nt `crRNA_sequence` field was treated as crRNA | It is a 4-nt PAM representation plus a 21-nt spacer, not a physical crRNA, and the direct repeat is unavailable |
| The first 7 nt were treated as the seed | They contain the 4-nt PAM and only 3 spacer bases, so they do not represent the Cas12a PAM-proximal seed |
| Guide and target were passed to `RNA.cofold` in the same target-oriented representation | The reverse-complement guide orientation was not represented |
| The DNA target was converted from T to U and folded as RNA | EasyDesign used DNA templates; RNA-RNA energy does not directly represent an RNA-DNA R-loop |
| `RNA.cofold` was treated as a hybrid-energy calculator | RNAcofold allows both intra- and intermolecular structures and does not represent a protein-bound Cas12a R-loop |
| The three Vertical3 modeling scripts selected different inputs | One kept numeric context features while the ablation and plotting scripts removed all 58 context features |

## Corrected V3 Thermodynamic Features

| Feature | Definition | Interpretation and limitation |
|---|---|---|
| `thermo_guide_spacer_unfolding_ensemble_rna_proxy_kcal_mol` | Reverse-complement the 21-nt spacer, convert it to RNA, and negate its ensemble free energy | Spacer unfolding-cost proxy; no direct repeat or protein-bound state |
| `thermo_target_local_dsDNA_separation_mfe_dna_proxy_kcal_mol` | Duplex the 21-nt target with its reverse complement under Mathews 2004 DNA parameters and negate the MFE | Local dsDNA-opening proxy; no full template or RPA-product context |
| `thermo_guide_target_full_hybrid_mfe_rna_proxy_kcal_mol` | Use correctly oriented guide and target representations with `RNAduplex` | Local RNA-RNA duplex proxy, not RNA-DNA or protein-bound R-loop energy |
| `thermo_guide_target_seed6_hybrid_mfe_rna_proxy_kcal_mol` | Exclude the PAM, use the first six PAM-proximal spacer bases, and calculate an `RNAduplex` proxy | Seed-pairing proxy; biologically motivated but still approximate |

The `proxy` suffix is mandatory semantic protection. These values must not be reported as direct Cas12a R-loop Delta G measurements.

## Biological Rationale

EasyDesign uses DNA templates, a 21-nt spacer, a 4-nt TTTN PAM, and Cas12a fluorescence activity measured at 37 C. Cas12a recognition depends on PAM recognition, PAM-proximal seed pairing, R-loop formation, and conformational activation. Sequence accessibility and local pairing stability are therefore biologically motivated, but crRNA folding, DNA opening, and RNA-DNA hybridization are distinct physical components. Published Cas12a free-energy analyses likewise use separate tools for RNA, DNA, and RNA-DNA hybrid terms rather than cofolding all inputs as two RNAs.

References: [ViennaRNA Python API](https://viennarna.readthedocs.io/en/latest/api_python.html), [RNAcofold](https://viennarna.readthedocs.io/en/latest/man/RNAcofold.html), [RNAduplex](https://viennarna.readthedocs.io/en/latest/man/RNAduplex.html), [ViennaRNA energy parameters](https://viennarna.readthedocs.io/en/latest/eval/energy_parameters.html), [Cas12a seed structure](https://pmc.ncbi.nlm.nih.gov/articles/PMC6879319/), [Cas12a kinetic basis](https://pmc.ncbi.nlm.nih.gov/articles/PMC6679935/), [Cas12a trans-cleavage free-energy analysis](https://academic.oup.com/nar/article/52/22/14077/7908798), and an [RNA-DNA hybrid thermodynamics method](https://academic.oup.com/bioinformatics/article/28/19/2530/289009).

## Statistical Decision

All four corrected proxies are complete across 8,417 training records. Their absolute univariate Spearman correlations range from 0.030 to 0.112. In paired P1-1 ablation, the full model improves mean OOF Spearman by only `0.000732` over the model without the thermodynamic block, with positive effects in 3/5 seeds. This fails the preregistered threshold of at least 4/5 positive seeds and a mean improvement of at least 0.005.

Therefore:

- The complete V3 table retains the four columns for traceable Package1 and controlled follow-up experiments.
- The thermodynamic block is not described as a validated important feature family.
- Thermodynamic columns in `nonpositional4_candidate` remain candidates, not promoted features.
- Stronger physical interpretation requires the complete crRNA direct repeat, full template/RPA context, and a method explicitly parameterized for RNA-DNA hybrids.
