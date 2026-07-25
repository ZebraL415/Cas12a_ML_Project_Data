#!/usr/bin/env python3
"""Independently audit the submitted Vertical 3 ViennaRNA features."""

from __future__ import annotations

import argparse
import hashlib
import json
from functools import lru_cache
from pathlib import Path

import numpy as np
import pandas as pd
import RNA


DG_COLUMNS = [
    "dG_hybrid_full",
    "dG_hybrid_seed",
    "dG_self_crRNA",
    "dG_self_target",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--v2-table", required=True, type=Path)
    parser.add_argument("--v2-with-dg-table", required=True, type=Path)
    parser.add_argument("--canonical-v2-table", required=True, type=Path)
    parser.add_argument("--output-json", required=True, type=Path)
    return parser.parse_args()


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def clean(value: object) -> str:
    if pd.isna(value):
        return ""
    return str(value).strip().upper().replace("T", "U")


@lru_cache(maxsize=None)
def reproduce_pair(guide: str, target: str) -> tuple[float, float, float, float]:
    if len(guide) < 5 or len(target) < 5:
        return (np.nan, np.nan, np.nan, np.nan)
    _, full = RNA.cofold(f"{guide}&{target}")
    if len(guide) >= 7 and len(target) >= 7:
        _, seed = RNA.cofold(f"{guide[:7]}&{target[:7]}")
    else:
        seed = np.nan
    _, guide_self = RNA.fold(guide)
    _, target_self = RNA.fold(target)
    return float(full), float(seed), float(guide_self), float(target_self)


def main() -> None:
    args = parse_args()
    args.output_json.parent.mkdir(parents=True, exist_ok=True)

    v2 = pd.read_csv(args.v2_table, low_memory=False)
    with_dg = pd.read_csv(args.v2_with_dg_table, low_memory=False)
    canonical = pd.read_csv(args.canonical_v2_table, low_memory=False)

    if RNA.__version__ != "2.7.2":
        raise RuntimeError(f"Expected ViennaRNA 2.7.2, found {RNA.__version__}")
    RNA.params_load_RNA_Turner2004()
    RNA.cvar.temperature = 37.0
    RNA.cvar.dangles = 2

    guide = v2["crRNA_sequence"].map(clean)
    target = v2["target_sequence"].map(clean)
    recomputed = pd.DataFrame(
        [reproduce_pair(g, t) for g, t in zip(guide, target)],
        columns=DG_COLUMNS,
        index=v2.index,
    )

    differences = {}
    exact_with_tolerance = {}
    for column in DG_COLUMNS:
        submitted = pd.to_numeric(with_dg[column], errors="coerce")
        absolute = (submitted - recomputed[column]).abs()
        differences[column] = float(absolute.max(skipna=True))
        exact_with_tolerance[column] = bool(
            np.allclose(submitted, recomputed[column], atol=1e-6, rtol=0, equal_nan=True)
        )

    perfect = v2["crRNA_sequence"].eq(v2["target_sequence"])
    seed = pd.to_numeric(with_dg["dG_hybrid_seed"], errors="coerce")
    self_equal = np.isclose(
        pd.to_numeric(with_dg.loc[perfect, "dG_self_crRNA"], errors="coerce"),
        pd.to_numeric(with_dg.loc[perfect, "dG_self_target"], errors="coerce"),
        atol=1e-6,
        equal_nan=True,
    )

    base_columns = [column for column in with_dg.columns if column not in DG_COLUMNS]
    result = {
        "audit_status": "completed",
        "formal_use_verdict": "fail_original_implementation_use_corrected_proxy_features",
        "viennarna_version": RNA.__version__,
        "temperature_c": 37.0,
        "v2_sha256": sha256(args.v2_table),
        "canonical_v2_sha256": sha256(args.canonical_v2_table),
        "v2_input_matches_canonical": sha256(args.v2_table) == sha256(args.canonical_v2_table),
        "submitted_sha256": sha256(args.v2_with_dg_table),
        "v2_shape": list(v2.shape),
        "submitted_shape": list(with_dg.shape),
        "expected_four_columns_added": with_dg.shape[1] == v2.shape[1] + 4,
        "record_order_preserved": bool(with_dg["record_id"].equals(v2["record_id"])),
        "base_columns_value_preserved": bool(with_dg.loc[:, base_columns].equals(v2)),
        "submitted_missing_counts": with_dg[DG_COLUMNS].isna().sum().astype(int).to_dict(),
        "submitted_unique_counts": with_dg[DG_COLUMNS].nunique().astype(int).to_dict(),
        "submitted_summary": with_dg[DG_COLUMNS].describe().to_dict(),
        "reproduction_max_abs_difference": differences,
        "reproduction_matches_at_1e_minus_6": exact_with_tolerance,
        "perfect_match_row_count": int(perfect.sum()),
        "seed_zero_count_all": int(np.isclose(seed, 0.0, atol=1e-12).sum()),
        "seed_zero_fraction_all": float(np.isclose(seed, 0.0, atol=1e-12).mean()),
        "seed_zero_fraction_perfect_matches": float(
            np.isclose(seed.loc[perfect], 0.0, atol=1e-12).mean()
        ),
        "self_crrna_equals_self_target_fraction_perfect_matches": float(self_equal.mean()),
        "code_findings": [
            "The 25-nt crRNA_sequence field includes the 4-nt PAM representation and is not a complete physical crRNA.",
            "The first seven bases used for the submitted seed feature contain four PAM bases and only three spacer bases.",
            "Submitted guide and target strings use the same target-oriented representation; they were not reverse-complemented before cofolding.",
            "RNA.cofold evaluates two RNAs and allows intra- and intermolecular structures; it is not a pure RNA-DNA hybrid energy.",
            "The target sequence was converted T-to-U and folded as RNA although EasyDesign assays used DNA templates.",
            "The submitted ablation and plotting scripts remove all 58 v2.1 sequence-context features, while run_vertical3_deltaG.py keeps numeric context columns; the scripts therefore do not define one consistent V3 input profile.",
        ],
    }
    args.output_json.write_text(
        json.dumps(result, indent=2, ensure_ascii=False, allow_nan=False) + "\n"
    )
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
