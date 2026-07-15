#!/usr/bin/env python3
"""Build a gap-preserving EasyDesign Table S3 alignment and source map.

The script reads the authoritative combined supplementary workbook and never
writes to 01_raw. Source mapping is deliberately conservative: it records all
exact or IUPAC-compatible Table S2 sequence-window hits and never selects the
first hit as truth.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import defaultdict
from pathlib import Path
from typing import Any

import pandas as pd


SOURCE_ID = "EasyDesign_2024"
RAW_REL = Path("01_raw/EasyDesign_2024/data/imt2214-sup-0002-tables1-9sourcedata (1).xlsx")
EXTRACTED_REL = Path("02_extracted_tables/diagnostic_activity/easydesign_mismatch_mapping")
CLEANED_REL = Path("03_cleaned_minimal/easydesign_mismatch")

IUPAC = {
    "A": frozenset("A"),
    "C": frozenset("C"),
    "G": frozenset("G"),
    "T": frozenset("T"),
    "R": frozenset("AG"),
    "Y": frozenset("CT"),
    "S": frozenset("GC"),
    "W": frozenset("AT"),
    "K": frozenset("GT"),
    "M": frozenset("AC"),
    "B": frozenset("CGT"),
    "D": frozenset("AGT"),
    "H": frozenset("ACT"),
    "V": frozenset("ACG"),
    "N": frozenset("ACGT"),
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def clean_sequence(value: Any, keep_gap: bool = False) -> str:
    text = "" if pd.isna(value) else str(value).upper()
    allowed = r"[^ACGTRYSWKMBDHVN-]" if keep_gap else r"[^ACGTRYSWKMBDHVN]"
    return re.sub(allowed, "", text)


def reverse_complement(seq: str) -> str:
    table = str.maketrans("ACGTRYSWKMBDHVN", "TGCAYRSWMKVHDBN")
    return seq.translate(table)[::-1]


def pair_id(guide: str, target_aligned: str) -> str:
    token = hashlib.sha1(f"{guide}|{target_aligned}".encode("utf-8")).hexdigest()[:16]
    return f"EasyDesign_2024_pair_{token}"


def compatible(query: str, template_window: str) -> bool:
    if len(query) != len(template_window):
        return False
    return all(bool(IUPAC.get(a, frozenset()) & IUPAC.get(b, frozenset())) for a, b in zip(query, template_window))


def event_features(guide: str, target_aligned: str) -> dict[str, Any]:
    result: dict[str, Any] = {}
    events: list[str] = []
    for position in range(25):
        guide_base = guide[position] if position < len(guide) else ""
        target_base = target_aligned[position] if position < len(target_aligned) else ""
        if not guide_base or not target_base:
            event = "unresolved"
        elif guide_base == "-" and target_base != "-":
            event = "gap_in_guide"
        elif target_base == "-" and guide_base != "-":
            event = "gap_in_target"
        elif guide_base not in "ACGT" or target_base not in "ACGT":
            event = "unresolved"
        elif guide_base == target_base:
            event = "match"
        else:
            event = "substitution"
        events.append(event)
        result[f"difference_pos_{position + 1:02d}"] = int(event in {"substitution", "gap_in_target", "gap_in_guide"})
        result[f"substitution_pos_{position + 1:02d}"] = int(event == "substitution")
        result[f"target_gap_pos_{position + 1:02d}"] = int(event == "gap_in_target")

    result["position_event_string"] = ";".join(f"{i + 1}:{event}" for i, event in enumerate(events) if event != "match")
    result["aligned_difference_count"] = sum(event in {"substitution", "gap_in_target", "gap_in_guide"} for event in events)
    result["substitution_count"] = events.count("substitution")
    result["gap_count_target"] = events.count("gap_in_target")
    result["gap_count_guide"] = events.count("gap_in_guide")
    result["unresolved_count"] = events.count("unresolved")
    result["pam_difference_count"] = sum(event in {"substitution", "gap_in_target", "gap_in_guide"} for event in events[:4])
    result["spacer_difference_count"] = sum(event in {"substitution", "gap_in_target", "gap_in_guide"} for event in events[4:])
    result["alignment_event_status"] = (
        "unresolved"
        if result["unresolved_count"]
        else "gap_preserved"
        if result["gap_count_target"] or result["gap_count_guide"]
        else "substitution_or_match_only"
    )
    return result


def template_role(member: int) -> str:
    if member == 1:
        return "original_reference"
    if 2 <= member <= 7:
        return "substitution_template"
    if member == 8:
        return "insertion_template"
    return "deletion_template"


def build_template_table(raw: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for _, source in raw.iterrows():
        template_no = int(source["Template No."])
        group = (template_no - 1) // 9 + 1
        member = (template_no - 1) % 9 + 1
        seq = clean_sequence(source["Sequence"])
        rows.append(
            {
                "source_id": SOURCE_ID,
                "source_sheet": "Table S2",
                "template_no": template_no,
                "template_group_id": f"EasyDesign_2024_template_group_{group:02d}",
                "template_group_number": group,
                "template_group_member": member,
                "template_role_from_paper_order": template_role(member),
                "template_sequence_raw": str(source["Sequence"]),
                "template_sequence_clean": seq,
                "template_length": len(seq),
                "contains_iupac_ambiguity": "yes" if not re.fullmatch(r"[ACGT]+", seq) else "no",
            }
        )
    out = pd.DataFrame(rows)
    reference_lengths = out[out["template_group_member"] == 1].set_index("template_group_number")["template_length"]
    out["length_delta_vs_group_reference"] = out.apply(
        lambda row: int(row["template_length"] - reference_lengths.loc[row["template_group_number"]]), axis=1
    )
    out["group_structure_qc"] = out.apply(
        lambda row: (
            "pass"
            if (row["template_group_member"] <= 7 and row["length_delta_vs_group_reference"] == 0)
            or (row["template_group_member"] == 8 and row["length_delta_vs_group_reference"] > 0)
            or (row["template_group_member"] == 9 and row["length_delta_vs_group_reference"] < 0)
            else "review"
        ),
        axis=1,
    )
    return out


def build_alignment_table(raw: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    replicate_counter: dict[tuple[str, str], int] = defaultdict(int)
    for _, source in raw.iterrows():
        record_no = int(source["No."])
        guide = clean_sequence(source["guide_seq"], keep_gap=True)
        target_aligned = clean_sequence(source["target_at_guide"], keep_gap=True)
        target_ungapped = target_aligned.replace("-", "")
        replicate_counter[(guide, target_aligned)] += 1
        events = event_features(guide, target_aligned)
        raw_hamming = int(source["guide_target_hamming_dist"])
        aligned_hamming = int(events["aligned_difference_count"])
        qc_status = (
            "review_invalid_alignment_length"
            if len(guide) != 25 or len(target_aligned) != 25
            else "review_ambiguous_base"
            if events["unresolved_count"]
            else "pass_gap_preserved"
            if "-" in guide or "-" in target_aligned
            else "pass_no_gap"
        )
        rows.append(
            {
                "dataset_id": "EasyDesign_2024_alignment_v2",
                "source_id": SOURCE_ID,
                "source_table_id": "EasyDesign_2024_TableS3_training",
                "record_id": f"EasyDesign_2024_TableS3_{record_no:05d}",
                "record_id_original": record_no,
                "guide_target_pair_id": pair_id(guide, target_aligned),
                "replicate_index_within_aligned_pair": replicate_counter[(guide, target_aligned)],
                "guide_seq_raw": str(source["guide_seq"]),
                "target_at_guide_raw": str(source["target_at_guide"]),
                "crRNA_sequence": guide,
                "target_aligned_25": target_aligned,
                "target_ungapped": target_ungapped,
                "guide_length": len(guide),
                "target_alignment_length": len(target_aligned),
                "target_ungapped_length": len(target_ungapped),
                "alignment_has_gap": "yes" if "-" in guide or "-" in target_aligned else "no",
                "pam_sequence_guide": guide[:4],
                "pam_sequence_target_aligned": target_aligned[:4],
                "spacer_sequence_guide": guide[4:],
                "spacer_sequence_target_aligned": target_aligned[4:],
                "spacer_sequence_target_ungapped_by_alignment": target_aligned[4:].replace("-", ""),
                "guide_target_hamming_dist_raw": raw_hamming,
                "raw_hamming_agreement": "yes" if raw_hamming == aligned_hamming else "no",
                "label_raw_name": "30 min",
                "label_raw_value": float(source["30 min"]),
                "label_status": "measured",
                "type1": source.get("type1", ""),
                "type2": source.get("type2", ""),
                "alignment_qc_status": qc_status,
                "default_training_tier": "core_no_gap" if qc_status == "pass_no_gap" else "conditional_gap_aware_review",
                **events,
            }
        )
    return pd.DataFrame(rows)


def build_exact_index(templates: pd.DataFrame, lengths: list[int]) -> dict[tuple[int, str], list[dict[str, Any]]]:
    index: dict[tuple[int, str], list[dict[str, Any]]] = defaultdict(list)
    for _, template in templates.iterrows():
        seq = template["template_sequence_clean"]
        for length in lengths:
            for start in range(0, len(seq) - length + 1):
                kmer = seq[start : start + length]
                if re.fullmatch(r"[ACGT]+", kmer):
                    index[(length, kmer)].append(
                        {
                            "template_no": int(template["template_no"]),
                            "template_group_id": template["template_group_id"],
                            "template_group_number": int(template["template_group_number"]),
                            "template_group_member": int(template["template_group_member"]),
                            "template_role": template["template_role_from_paper_order"],
                            "start_0based": start,
                            "end_0based_exclusive": start + length,
                        }
                    )
    return index


def iupac_hits(query: str, templates: pd.DataFrame, orientation: str) -> list[dict[str, Any]]:
    hits: list[dict[str, Any]] = []
    for _, template in templates.iterrows():
        seq = template["template_sequence_clean"]
        for start in range(0, len(seq) - len(query) + 1):
            window = seq[start : start + len(query)]
            if window != query and compatible(query, window):
                hits.append(
                    {
                        "template_no": int(template["template_no"]),
                        "template_group_id": template["template_group_id"],
                        "template_group_number": int(template["template_group_number"]),
                        "template_group_member": int(template["template_group_member"]),
                        "template_role": template["template_role_from_paper_order"],
                        "start_0based": start,
                        "end_0based_exclusive": start + len(query),
                        "orientation": orientation,
                        "match_mode": "iupac_compatible",
                        "matched_template_window": window,
                    }
                )
    return hits


def build_source_map(alignment: pd.DataFrame, templates: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    lengths = sorted(alignment["target_ungapped_length"].unique().tolist())
    exact_index = build_exact_index(templates, lengths)
    hit_rows: list[dict[str, Any]] = []
    summary_rows: list[dict[str, Any]] = []

    for _, record in alignment.iterrows():
        target = record["target_ungapped"]
        candidates: list[dict[str, Any]] = []
        for orientation, query in (("forward", target), ("reverse_complement", reverse_complement(target))):
            for hit in exact_index.get((len(query), query), []):
                candidates.append(
                    {
                        **hit,
                        "orientation": orientation,
                        "match_mode": "exact_acgt",
                        "matched_template_window": query,
                    }
                )
        if not candidates:
            for orientation, query in (("forward", target), ("reverse_complement", reverse_complement(target))):
                candidates.extend(iupac_hits(query, templates, orientation))

        for hit_index, hit in enumerate(candidates, start=1):
            hit_rows.append(
                {
                    "source_id": SOURCE_ID,
                    "record_id": record["record_id"],
                    "record_id_original": int(record["record_id_original"]),
                    "guide_target_pair_id": record["guide_target_pair_id"],
                    "alignment_has_gap": record["alignment_has_gap"],
                    "target_ungapped": target,
                    "mapping_hit_index": hit_index,
                    **hit,
                    "mapping_interpretation": "source_mapping_metadata_only_not_a_label",
                }
            )

        template_nos = sorted({int(hit["template_no"]) for hit in candidates})
        group_ids = sorted({str(hit["template_group_id"]) for hit in candidates})
        orientations = sorted({str(hit["orientation"]) for hit in candidates})
        positions = {(int(hit["template_no"]), int(hit["start_0based"]), str(hit["orientation"])) for hit in candidates}
        modes = sorted({str(hit["match_mode"]) for hit in candidates})
        if not candidates:
            status = "unmapped_exact_or_iupac"
            confidence = "review"
        elif len(positions) == 1 and modes == ["exact_acgt"]:
            status = "unique_exact_window"
            confidence = "high"
        elif len(template_nos) == 1 and modes == ["exact_acgt"]:
            status = "ambiguous_position_same_template"
            confidence = "medium"
        elif len(group_ids) == 1 and modes == ["exact_acgt"]:
            status = "ambiguous_template_single_group"
            confidence = "medium"
        elif modes == ["iupac_compatible"] and len(group_ids) == 1:
            status = "iupac_compatible_single_group"
            confidence = "review"
        elif len(group_ids) > 1:
            status = "ambiguous_multiple_groups"
            confidence = "review"
        else:
            status = "ambiguous_source_mapping"
            confidence = "review"

        summary_rows.append(
            {
                "source_id": SOURCE_ID,
                "record_id": record["record_id"],
                "record_id_original": int(record["record_id_original"]),
                "guide_target_pair_id": record["guide_target_pair_id"],
                "alignment_has_gap": record["alignment_has_gap"],
                "mapping_status": status,
                "mapping_confidence": confidence,
                "mapping_hit_count": len(candidates),
                "mapping_template_count": len(template_nos),
                "mapping_group_count": len(group_ids),
                "mapping_orientation_count": len(orientations),
                "mapping_candidate_template_nos": ";".join(map(str, template_nos)),
                "mapping_candidate_group_ids": ";".join(group_ids),
                "mapping_candidate_orientations": ";".join(orientations),
                "mapping_match_modes": ";".join(modes),
                "mapping_use": "audit_grouping_only_not_default_model_feature",
            }
        )
    return pd.DataFrame(hit_rows), pd.DataFrame(summary_rows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--run-dir", type=Path)
    args = parser.parse_args()
    root = args.root.resolve()
    raw_path = root / RAW_REL
    extracted_dir = root / EXTRACTED_REL
    cleaned_dir = root / CLEANED_REL
    extracted_dir.mkdir(parents=True, exist_ok=True)
    cleaned_dir.mkdir(parents=True, exist_ok=True)

    raw_s2 = pd.read_excel(raw_path, sheet_name="Table S2", header=1)
    raw_s3 = pd.read_excel(raw_path, sheet_name="Table S3", header=1)
    templates = build_template_table(raw_s2)
    alignment = build_alignment_table(raw_s3)
    hits, source_map = build_source_map(alignment, templates)

    raw_alignment_path = extracted_dir / "EasyDesign_2024_TableS3_alignment_preserved_raw.csv"
    raw_templates_path = extracted_dir / "EasyDesign_2024_TableS2_template_groups_raw.csv"
    raw_hits_path = extracted_dir / "EasyDesign_2024_TableS2_TableS3_mapping_hits_raw.csv"
    alignment_path = cleaned_dir / "EasyDesign_2024_guide_target_alignment_v2.csv"
    source_map_path = cleaned_dir / "EasyDesign_2024_source_mapping_v1.csv"
    qc_path = cleaned_dir / "EasyDesign_2024_mismatch_qc_v2.csv"

    raw_s3.assign(
        record_id=[f"EasyDesign_2024_TableS3_{int(value):05d}" for value in raw_s3["No."]],
        target_aligned_25=[clean_sequence(value, keep_gap=True) for value in raw_s3["target_at_guide"]],
    ).to_csv(raw_alignment_path, index=False)
    templates.to_csv(raw_templates_path, index=False)
    hits.to_csv(raw_hits_path, index=False)
    alignment.to_csv(alignment_path, index=False)
    source_map.to_csv(source_map_path, index=False)
    alignment.merge(source_map, on=["source_id", "record_id", "record_id_original", "guide_target_pair_id", "alignment_has_gap"], how="left").query(
        "alignment_qc_status != 'pass_no_gap' or raw_hamming_agreement != 'yes' or mapping_confidence != 'high'"
    ).to_csv(qc_path, index=False)

    report = {
        "input": str(RAW_REL),
        "input_sha256": sha256(raw_path),
        "table_s2_rows": int(len(templates)),
        "table_s2_groups": int(templates["template_group_number"].nunique()),
        "table_s2_group_structure_review_rows": int((templates["group_structure_qc"] != "pass").sum()),
        "table_s3_rows": int(len(alignment)),
        "no_gap_rows": int((alignment["alignment_has_gap"] == "no").sum()),
        "gap_rows": int((alignment["alignment_has_gap"] == "yes").sum()),
        "raw_hamming_agreement_rows": int((alignment["raw_hamming_agreement"] == "yes").sum()),
        "raw_hamming_disagreement_rows": int((alignment["raw_hamming_agreement"] == "no").sum()),
        "mapping_status_counts": source_map["mapping_status"].value_counts().to_dict(),
        "mapping_confidence_counts": source_map["mapping_confidence"].value_counts().to_dict(),
        "mapping_any_hit_rows": int((source_map["mapping_hit_count"] > 0).sum()),
        "mapping_unmapped_rows": int((source_map["mapping_hit_count"] == 0).sum()),
        "mapping_hit_rows": int(len(hits)),
        "outputs": [
            str(path.relative_to(root))
            for path in (raw_alignment_path, raw_templates_path, raw_hits_path, alignment_path, source_map_path, qc_path)
        ],
    }
    if args.run_dir:
        args.run_dir.mkdir(parents=True, exist_ok=True)
        (args.run_dir / "alignment_mapping_qc.json").write_text(
            json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
