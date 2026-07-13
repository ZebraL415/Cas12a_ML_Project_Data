# Reference Improved Result

This directory is copied from `/Users/linzibo/Desktop/MLRS/improved_feature_outputs/` and is used to assess the potential value of engineered features.

Confirmed facts: all 2,217 predictions correspond to the current `baseline_validation` rows; record IDs, crRNA, target, and labels match exactly. Recalculated metrics are Spearman 0.765651, Pearson 0.747238, MAE 0.327815, RMSE 0.424830, and R2 0.554858, consistent with the JSON. The maximum difference between saved and recomputed residuals is `1.19e-7`, attributable to output precision.

Reproducibility boundary: training code, model parameters, dependency lock, and random seed were not supplied. Feature names also differ from Xu's generator and include duplicate or linearly equivalent variables. This directory therefore establishes internal consistency of saved outputs, not independent reproduction of training or selection of a final model.
