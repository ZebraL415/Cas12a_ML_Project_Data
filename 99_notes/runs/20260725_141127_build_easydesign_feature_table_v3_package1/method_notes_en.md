# Method Notes

The submitted Vertical3 output was first independently recomputed in an isolated ViennaRNA 2.7.2 environment. Numerical consistency was checked through SHA-256, row order, parent-column preservation, missingness, and `allclose(atol=1e-6)`. Biological validity was reviewed separately against the EasyDesign experiment, field semantics, and ViennaRNA algorithm boundaries.

Feature Table V3 uses the V2.1 context table as an immutable parent. The 21-nt spacer is separated from the PAM-containing 25-nt representation, and the guide is reverse-complemented according to the target-oriented storage convention. RNA unfolding uses Turner 2004 ensemble free energy, the local DNA duplex uses Mathews 2004 parameters, and full and PAM-proximal seed6 pairing use `RNAduplex`. All four columns include `proxy` in their names and document their limitations. All parent columns and row order remain unchanged.

P1-0 uses the fixed 8,417/2,217 split, seed 42, and original XGBoost parameters. P1-1 uses only the 8,417 training records with frozen five-fold target groups and five seeds, removes one feature block at a time, and fits 175 models. Neither fixed validation nor Table S5 participates in block selection.
