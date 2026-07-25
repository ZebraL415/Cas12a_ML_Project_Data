# Evidence Trace

## Decision: Exclude the Submitted Vertical3 Columns from Formal V3

- File evidence: the submitted V2 and canonical V2 hashes match; the output adds only four columns and is exactly reproducible.
- Code evidence: the input is a PAM-containing 25-nt representation, the seed is the first 7 nt, the guide is not reverse-complemented, the target is treated as RNA, and `RNA.cofold` is used.
- Documentation evidence: RNAcofold describes the joint secondary structure of two RNAs, not an RNA-DNA Cas12a R-loop model.
- Remaining uncertainty: the complete crRNA direct repeat and template context are unavailable.

## Decision: Adopt Four Corrected Proxies

- Paper evidence: EasyDesign uses a 4-nt TTTN PAM, 21-nt spacer, DNA templates, and a 37 C fluorescence reaction.
- Literature evidence: the Cas12a seed is PAM-proximal, and free-energy analyses should distinguish RNA folding, DNA opening, and RNA-DNA hybridization.
- Implementation evidence: V3 separates the spacer, corrects orientation, excludes the PAM, and labels every output as a proxy.
- Remaining uncertainty: proxies do not replace protein-bound R-loop energy.

## Decision: Retain Thermodynamics Conditionally

- P1-1 evidence: mean OOF Spearman gain is 0.000732 and 3/5 seeds are positive, below the preregistered requirement of at least 4/5 and a gain of 0.005.
- Decision: preserve the columns for traceable controlled experiments without claiming validation or high impact.
