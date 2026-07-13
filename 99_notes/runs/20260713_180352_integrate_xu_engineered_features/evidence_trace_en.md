# Evidence Trace

## Decision 1: Preserve Xu's Original Script

Evidence: the received file SHA-256 is `cf8cd2f...a1830`, and the script runs unchanged against the current v0 table.

Action: preserve it under `scripts/contributions/xu/` and place project-side corrections in a separate v1 builder.

## Decision 2: Use Direct Computationally Without Claiming Biological Validation

Evidence: `direct` has 1.0 exact agreement with computed Hamming, while the other three modes are near zero. The script itself states that source documentation is still required for biological convention.

Action: allow direct-mode pairwise recomputation while leaving all proximal, seed, and distal interpretations unconfirmed.

## Decision 3: Do Not Select Every High-Importance Column Directly

Evidence: `eng_mismatch_count` exactly duplicates computed Hamming, and `eng_match_fraction + eng_mismatch_fraction = 1`. The raw Hamming meaning is unresolved.

Action: v1 excludes simple duplicates and unresolved-semantic fields and retains one interpretable representation.

## Decision 4: Retain Position Features As A Complete Family And Fix Unaligned Encoding

Evidence: positions 2 and 4 are important in the reference result, but 740 primary targets are shorter than 25 nt; the original generator encodes nonexistent positions as zero.

Action: retain the complete positions 1 through 25, write unaligned cells as missing, and use the existing `target_length` to interpret alignment coverage.

## Decision 5: Treat The Improved Result As Internally Consistent Reference Only

Evidence: predictions match the project validation rows and metrics can be recomputed, but training code, parameters, dependencies, and random seed are absent.

Action: store the files under `evaluation/reference_improved_feature_run/` without claiming independent reproduction or final-model performance.
