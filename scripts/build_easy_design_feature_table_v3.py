#!/usr/bin/env python3
"""Build EasyDesign feature table v3 from the audited v2.1 table.

The four thermodynamic variables are deliberately named as proxies. ViennaRNA
does not model the Cas12a protein-bound R-loop, and the source table does not
contain the complete crRNA direct repeat or full DNA-template context for every
record. The script therefore uses only source-preserving local sequence fields.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from functools import lru_cache
from pathlib import Path

import numpy as np
import pandas as pd
import RNA
from scipy.stats import spearmanr


THERMO_FEATURES = [
    "thermo_guide_spacer_unfolding_ensemble_rna_proxy_kcal_mol",
    "thermo_target_local_dsDNA_separation_mfe_dna_proxy_kcal_mol",
    "thermo_guide_target_full_hybrid_mfe_rna_proxy_kcal_mol",
    "thermo_guide_target_seed6_hybrid_mfe_rna_proxy_kcal_mol",
]

NONPOSITIONAL4_BLOCKS = {
    "pair_alignment",
    "substitution_type",
    "sequence_context",
    "thermodynamic",
}

DNA_COMPLEMENT = str.maketrans("ACGT", "TGCA")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--v2-1-table", required=True, type=Path)
    parser.add_argument("--v2-1-dictionary", required=True, type=Path)
    parser.add_argument("--v2-1-block-manifest", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    return parser.parse_args()


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def clean_dna(value: object, *, allow_gap: bool = False) -> str:
    if pd.isna(value):
        return ""
    sequence = str(value).strip().upper()
    allowed = set("ACGT-") if allow_gap else set("ACGT")
    if not sequence or not set(sequence).issubset(allowed):
        return ""
    return sequence


def reverse_complement(sequence: str) -> str:
    return sequence.translate(DNA_COMPLEMENT)[::-1]


def as_rna(sequence: str) -> str:
    return sequence.replace("T", "U")


def configure_rna_model() -> None:
    RNA.params_load_RNA_Turner2004()
    RNA.cvar.temperature = 37.0
    RNA.cvar.dangles = 2


def configure_dna_model() -> None:
    RNA.params_load_DNA_Mathews2004()
    RNA.cvar.temperature = 37.0
    RNA.cvar.dangles = 2


@lru_cache(maxsize=None)
def guide_spacer_unfolding_proxy(guide_stored: str) -> float:
    if len(guide_stored) < 5:
        return np.nan
    actual_guide_rna = as_rna(reverse_complement(guide_stored))
    model = RNA.md()
    model.temperature = 37.0
    model.dangles = 2
    compound = RNA.fold_compound(actual_guide_rna, model)
    _, mfe = compound.mfe()
    compound.exp_params_rescale(mfe)
    _, ensemble_free_energy = compound.pf()
    return float(-ensemble_free_energy)


@lru_cache(maxsize=None)
def rna_duplex_proxy(guide_stored: str, target_stored: str) -> float:
    if len(guide_stored) < 3 or len(target_stored) < 3:
        return np.nan
    actual_guide_rna = as_rna(reverse_complement(guide_stored))
    target_rna_proxy = as_rna(target_stored)
    return float(RNA.duplexfold(actual_guide_rna, target_rna_proxy).energy)


@lru_cache(maxsize=None)
def dna_duplex_separation_proxy(target_stored: str) -> float:
    if len(target_stored) < 3:
        return np.nan
    complement = reverse_complement(target_stored)
    formation_energy = float(RNA.duplexfold(target_stored, complement).energy)
    return -formation_energy


def compute_thermodynamic_features(frame: pd.DataFrame) -> pd.DataFrame:
    required = {
        "spacer_sequence_guide",
        "spacer_sequence_target_aligned",
        "spacer_sequence_target_ungapped_by_alignment",
    }
    missing = required.difference(frame.columns)
    if missing:
        raise ValueError(f"Missing required sequence fields: {sorted(missing)}")

    guide = frame["spacer_sequence_guide"].map(clean_dna)
    target_aligned = frame["spacer_sequence_target_aligned"].map(
        lambda value: clean_dna(value, allow_gap=True)
    )
    target_ungapped = frame[
        "spacer_sequence_target_ungapped_by_alignment"
    ].map(clean_dna)

    configure_rna_model()
    guide_unfolding = guide.map(guide_spacer_unfolding_proxy)
    full_hybrid = pd.Series(
        [rna_duplex_proxy(g, t) for g, t in zip(guide, target_ungapped)],
        index=frame.index,
        dtype=float,
    )
    seed_hybrid = pd.Series(
        [
            rna_duplex_proxy(g[:6], t[:6].replace("-", ""))
            for g, t in zip(guide, target_aligned)
        ],
        index=frame.index,
        dtype=float,
    )

    configure_dna_model()
    target_separation = target_ungapped.map(dna_duplex_separation_proxy)
    configure_rna_model()

    return pd.DataFrame(
        {
            THERMO_FEATURES[0]: guide_unfolding,
            THERMO_FEATURES[1]: target_separation,
            THERMO_FEATURES[2]: full_hybrid,
            THERMO_FEATURES[3]: seed_hybrid,
        },
        index=frame.index,
    )


def append_dictionary(parent: pd.DataFrame) -> pd.DataFrame:
    rows = [
        {
            "feature_name": THERMO_FEATURES[0],
            "category": "thermodynamic",
            "input_fields": "spacer_sequence_guide",
            "formula_or_definition": (
                "Negative ViennaRNA Turner-2004 ensemble free energy of the "
                "reverse-complemented 21-nt guide representation at 37 C."
            ),
            "gap_behavior": "guide has fixed 21-nt A/C/G/T sequence",
            "default_model_role": "candidate_input",
            "leakage_risk": "none_known",
            "notes": (
                "Spacer-only RNA unfolding proxy; not the complete crRNA because "
                "the direct repeat is unavailable. Positive values indicate a "
                "larger predicted unfolding cost."
            ),
        },
        {
            "feature_name": THERMO_FEATURES[1],
            "category": "thermodynamic",
            "input_fields": "spacer_sequence_target_ungapped_by_alignment",
            "formula_or_definition": (
                "Negative ViennaRNA Mathews-2004 DNA duplex MFE between the local "
                "target and its reverse complement at 37 C."
            ),
            "gap_behavior": "gaps removed after alignment; length retained separately",
            "default_model_role": "candidate_input",
            "leakage_risk": "none_known",
            "notes": (
                "Positive local dsDNA separation-cost proxy; not a full plasmid or "
                "RPA-product free energy."
            ),
        },
        {
            "feature_name": THERMO_FEATURES[2],
            "category": "thermodynamic",
            "input_fields": (
                "spacer_sequence_guide; "
                "spacer_sequence_target_ungapped_by_alignment"
            ),
            "formula_or_definition": (
                "ViennaRNA RNAduplex MFE at 37 C after reverse-complementing the "
                "stored guide representation; target is converted T-to-U."
            ),
            "gap_behavior": "target gaps removed; bulges may arise from unequal lengths",
            "default_model_role": "candidate_input",
            "leakage_risk": "none_known",
            "notes": (
                "RNA-RNA hybridization proxy only; the physical Cas12a R-loop is an "
                "RNA-DNA hybrid and includes protein effects."
            ),
        },
        {
            "feature_name": THERMO_FEATURES[3],
            "category": "thermodynamic",
            "input_fields": (
                "first 6 PAM-proximal bases of spacer_sequence_guide and "
                "spacer_sequence_target_aligned"
            ),
            "formula_or_definition": (
                "ViennaRNA RNAduplex MFE for the PAM-proximal six-base spacer "
                "segment at 37 C."
            ),
            "gap_behavior": "aligned target gap removed within seed6 segment",
            "default_model_role": "candidate_input",
            "leakage_risk": "none_known",
            "notes": (
                "Seed6 RNA-RNA proxy based on the Cas12a PAM-proximal seed; PAM "
                "bases themselves are excluded."
            ),
        },
    ]
    return pd.concat([parent, pd.DataFrame(rows, columns=parent.columns)], ignore_index=True)


def safe_spearman(x: pd.Series, y: pd.Series) -> float | None:
    pair = pd.concat([pd.to_numeric(x, errors="coerce"), y], axis=1).dropna()
    if len(pair) < 3 or pair.iloc[:, 0].nunique() < 2:
        return None
    return float(spearmanr(pair.iloc[:, 0], pair.iloc[:, 1]).statistic)


def main() -> None:
    args = parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)

    if RNA.__version__ != "2.7.2":
        raise RuntimeError(f"Expected ViennaRNA 2.7.2, found {RNA.__version__}")

    frame = pd.read_csv(args.v2_1_table, low_memory=False)
    dictionary = pd.read_csv(args.v2_1_dictionary, low_memory=False)
    block_manifest = pd.read_csv(args.v2_1_block_manifest, low_memory=False)

    if frame.shape != (11992, 246):
        raise ValueError(f"Unexpected v2.1 shape: {frame.shape}")
    if frame["record_id"].duplicated().any():
        raise ValueError("record_id is not unique")
    if len(block_manifest) != 188:
        raise ValueError(f"Expected 188 v2.1 features, found {len(block_manifest)}")

    thermo = compute_thermodynamic_features(frame)
    if thermo.isna().any().any():
        raise ValueError(f"Thermodynamic features contain missing values: {thermo.isna().sum().to_dict()}")

    output = pd.concat([frame.copy(), thermo], axis=1)
    output["feature_table_version"] = "v3_context_thermodynamic_proxy"

    thermo_manifest = pd.DataFrame(
        {"feature_name": THERMO_FEATURES, "category": "thermodynamic"}
    )
    full_manifest = pd.concat([block_manifest, thermo_manifest], ignore_index=True)
    if full_manifest["feature_name"].duplicated().any() or len(full_manifest) != 192:
        raise ValueError("v3 feature manifest is not a unique 192-feature list")

    feature_set = set(full_manifest["feature_name"])
    missing_features = feature_set.difference(output.columns)
    if missing_features:
        raise ValueError(f"Feature columns absent from v3 table: {sorted(missing_features)}")

    metadata_columns = [column for column in output.columns if column not in feature_set]
    priority_features = full_manifest.loc[
        full_manifest["category"].isin(NONPOSITIONAL4_BLOCKS), "feature_name"
    ].tolist()
    selected = output.loc[:, metadata_columns + priority_features].copy()
    selected["default_model_input_profile"] = "v3_nonpositional4_candidate"

    full_dictionary = append_dictionary(dictionary)

    outputs = {
        "full_table": args.output_dir / "EasyDesign_2024_diagnostic_activity_feature_table_v3.csv",
        "nonpositional4_table": args.output_dir / "EasyDesign_2024_diagnostic_activity_feature_table_v3_nonpositional4_candidate.csv",
        "feature_dictionary": args.output_dir / "EasyDesign_2024_feature_dictionary_v3.csv",
        "feature_block_manifest": args.output_dir / "EasyDesign_2024_feature_block_manifest_v3.csv",
        "nonpositional4_manifest": args.output_dir / "EasyDesign_2024_nonpositional4_feature_manifest_v3.csv",
        "qc": args.output_dir / "EasyDesign_2024_feature_table_v3_qc.json",
    }

    output.to_csv(outputs["full_table"], index=False)
    selected.to_csv(outputs["nonpositional4_table"], index=False)
    full_dictionary.to_csv(outputs["feature_dictionary"], index=False)
    full_manifest.to_csv(outputs["feature_block_manifest"], index=False)
    full_manifest.loc[full_manifest["category"].isin(NONPOSITIONAL4_BLOCKS)].to_csv(
        outputs["nonpositional4_manifest"], index=False
    )

    label = pd.to_numeric(output["label_normalized"], errors="coerce")
    primary_train = (
        output["label_is_primary_baseline"].astype(str).str.lower().eq("yes")
        & output["baseline_split"].eq("baseline_train")
    )
    qc = {
        "build_status": "passed",
        "parent_table": str(args.v2_1_table),
        "parent_sha256": sha256(args.v2_1_table),
        "viennarna_version": RNA.__version__,
        "temperature_c": 37.0,
        "rna_parameter_set": "Turner2004",
        "dna_parameter_set": "Mathews2004",
        "full_table_shape": list(output.shape),
        "nonpositional4_table_shape": list(selected.shape),
        "candidate_feature_count": len(full_manifest),
        "nonpositional4_feature_count": len(priority_features),
        "block_counts": full_manifest.groupby("category").size().to_dict(),
        "record_id_unique": bool(output["record_id"].is_unique),
        "row_order_preserved": bool(output["record_id"].equals(frame["record_id"])),
        "parent_columns_preserved": bool(
            output.loc[:, frame.columns.difference(["feature_table_version"], sort=False)].equals(
                frame.loc[:, frame.columns.difference(["feature_table_version"], sort=False)]
            )
        ),
        "thermodynamic_missing_counts": thermo.isna().sum().astype(int).to_dict(),
        "thermodynamic_unique_counts": thermo.nunique().astype(int).to_dict(),
        "thermodynamic_summary": thermo.describe().to_dict(),
        "training_label_spearman_univariate": {
            feature: safe_spearman(output.loc[primary_train, feature], label.loc[primary_train])
            for feature in THERMO_FEATURES
        },
        "limitations": [
            "No complete crRNA direct-repeat sequence is available; guide unfolding is spacer-only.",
            "No full DNA-template context is available for every row; dsDNA separation is local.",
            "ViennaRNA RNAduplex is an RNA-RNA proxy, not an RNA-DNA/protein-bound R-loop model.",
        ],
    }
    outputs["qc"].write_text(json.dumps(qc, indent=2, ensure_ascii=False, allow_nan=False) + "\n")

    manifest = {
        key: {"file_name": path.name, "sha256": sha256(path), "bytes": path.stat().st_size}
        for key, path in outputs.items()
    }
    manifest_path = args.output_dir / "v3_output_manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n")

    print(json.dumps({"outputs": manifest, "qc": qc}, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
