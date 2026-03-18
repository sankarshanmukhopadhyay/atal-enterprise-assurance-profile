#!/usr/bin/env python3
"""
generate_profile_checklist.py — Generate a control checklist for a given EAP
assurance level from the master catalog and the level overlay.

Outputs JSON, CSV, and/or Markdown depending on --format flag.

Usage:
    python scripts/generate_profile_checklist.py --level EAP-L1
    python scripts/generate_profile_checklist.py --level EAP-L2 --format csv
    python scripts/generate_profile_checklist.py --level EAP-L3 --format md
    python scripts/generate_profile_checklist.py --level EAP-L1 --format all
"""

import sys
import json
import csv
import pathlib
import argparse


REPO_ROOT = pathlib.Path(__file__).parent.parent
CATALOG_PATH = REPO_ROOT / "catalogs" / "atal-eap-control-catalog.json"
OVERLAY_DIR = REPO_ROOT / "catalogs" / "assurance-level-overlays"
OUTPUT_DIR = REPO_ROOT / "artifacts"

VALID_LEVELS = ["EAP-L1", "EAP-L2", "EAP-L3"]
VALID_FORMATS = ["json", "csv", "md", "all"]


def load_json(path: pathlib.Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def build_checklist(level: str) -> list[dict]:
    catalog = load_json(CATALOG_PATH)
    overlay_path = OVERLAY_DIR / f"{level}-overlay.json"
    if not overlay_path.exists():
        print(f"ERROR: Overlay not found: {overlay_path}", file=sys.stderr)
        sys.exit(2)
    overlay = load_json(overlay_path)

    ctrl_index = {c["id"]: c for c in catalog["controls"]}
    overlay_index = {o["control_id"]: o for o in overlay["applicable_controls"]}
    mandatory_ids = set(overlay.get("mandatory_control_ids", []))

    checklist = []
    for ctrl_id in sorted(ctrl_index.keys()):
        ctrl = ctrl_index[ctrl_id]
        ov = overlay_index.get(ctrl_id, {})
        applicable = ov.get("applicable", False)
        strength = ov.get("normative_strength_override") or ctrl.get("normative_strength", "")
        mandatory = ctrl_id in mandatory_ids
        note = ov.get("note") or ""
        checklist.append({
            "control_id": ctrl_id,
            "title": ctrl["title"],
            "family": ctrl["family"],
            "applicable": applicable,
            "normative_strength": strength if applicable else "N/A",
            "mandatory": mandatory,
            "criticality": ctrl["criticality"],
            "note": note,
            "status": "",  # to be filled by assessor
        })
    return checklist


def write_json(checklist: list[dict], level: str):
    OUTPUT_DIR.mkdir(exist_ok=True)
    out = OUTPUT_DIR / f"{level}-checklist.json"
    out.write_text(json.dumps({"assurance_level": level, "checklist": checklist}, indent=2), encoding="utf-8")
    print(f"  Written: {out}")


def write_csv(checklist: list[dict], level: str):
    OUTPUT_DIR.mkdir(exist_ok=True)
    out = OUTPUT_DIR / f"{level}-checklist.csv"
    fields = ["control_id", "title", "family", "applicable", "normative_strength", "mandatory", "criticality", "note", "status"]
    with open(out, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for row in checklist:
            writer.writerow(row)
    print(f"  Written: {out}")


def write_md(checklist: list[dict], level: str):
    OUTPUT_DIR.mkdir(exist_ok=True)
    out = OUTPUT_DIR / f"{level}-checklist.md"
    lines = [
        f"# EAP Control Checklist — {level}",
        "",
        f"Generated from `catalogs/atal-eap-control-catalog.json` and `catalogs/assurance-level-overlays/{level}-overlay.json`.",
        "",
        "| Control ID | Title | Family | Applicable | Strength | Mandatory | Criticality | Status |",
        "|---|---|---|:---:|:---:|:---:|:---:|:---:|",
    ]
    for row in checklist:
        applicable = "Yes" if row["applicable"] else "No"
        mandatory = "**Yes**" if row["mandatory"] else "No"
        lines.append(
            f"| {row['control_id']} | {row['title']} | {row['family']} | {applicable} "
            f"| {row['normative_strength']} | {mandatory} | {row['criticality']} | {row['status'] or '—'} |"
        )
    lines += [
        "",
        "## Notes",
        "",
    ]
    for row in checklist:
        if row["note"]:
            lines.append(f"- **{row['control_id']}**: {row['note']}")
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"  Written: {out}")


def main():
    parser = argparse.ArgumentParser(description="Generate an EAP profile checklist.")
    parser.add_argument("--level", required=True, choices=VALID_LEVELS, help="Assurance level to generate checklist for")
    parser.add_argument("--format", default="all", choices=VALID_FORMATS, help="Output format (default: all)")
    args = parser.parse_args()

    print(f"Generating checklist for {args.level} ...")
    checklist = build_checklist(args.level)
    applicable_count = sum(1 for c in checklist if c["applicable"])
    mandatory_count = sum(1 for c in checklist if c["mandatory"])
    print(f"  Controls total:      {len(checklist)}")
    print(f"  Applicable at level: {applicable_count}")
    print(f"  Mandatory:           {mandatory_count}")

    fmt = args.format
    if fmt in ("json", "all"):
        write_json(checklist, args.level)
    if fmt in ("csv", "all"):
        write_csv(checklist, args.level)
    if fmt in ("md", "all"):
        write_md(checklist, args.level)

    print("Done.")


if __name__ == "__main__":
    main()
