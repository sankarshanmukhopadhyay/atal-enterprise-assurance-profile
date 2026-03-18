#!/usr/bin/env python3
"""
build_traceability_matrix.py — Generate updated traceability outputs from the
control catalog and existing mappings. Produces JSON, CSV, and Markdown outputs.

Usage:
    python scripts/build_traceability_matrix.py
    python scripts/build_traceability_matrix.py --format csv
    python scripts/build_traceability_matrix.py --format md
"""

import sys
import json
import csv
import pathlib
import argparse


REPO_ROOT = pathlib.Path(__file__).parent.parent
CATALOG_PATH = REPO_ROOT / "catalogs" / "atal-eap-control-catalog.json"
OUTPUT_DIR = REPO_ROOT / "artifacts"

VALID_FORMATS = ["json", "csv", "md", "all"]


def load_json(path: pathlib.Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def build_matrix(catalog: dict) -> list[dict]:
    rows = []
    for ctrl in catalog["controls"]:
        atal_refs = "; ".join(ctrl.get("mapped_atal_references", []))
        repo_sources = "; ".join(ctrl.get("mapped_repo_sources", []))
        levels = ", ".join(ctrl.get("assurance_levels", []))
        related_risks = "; ".join(ctrl.get("related_risks", []))
        compensating = ", ".join(ctrl.get("compensating_controls", []))
        rows.append({
            "control_id": ctrl["id"],
            "title": ctrl["title"],
            "family": ctrl["family"],
            "assurance_levels": levels,
            "normative_strength": ctrl["normative_strength"],
            "criticality": ctrl["criticality"],
            "control_type": ctrl["control_type"],
            "atal_references": atal_refs,
            "repo_sources": repo_sources,
            "related_risks": related_risks,
            "compensating_controls": compensating,
            "automation_candidate": str(ctrl.get("automation_candidate", False)),
        })
    return rows


def write_json(rows: list[dict], catalog: dict):
    OUTPUT_DIR.mkdir(exist_ok=True)
    out = OUTPUT_DIR / "traceability-matrix.json"
    payload = {
        "catalog_version": catalog.get("version", "N/A"),
        "generated_from": str(CATALOG_PATH.relative_to(REPO_ROOT)),
        "rows": rows,
    }
    out.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"  Written: {out}")


def write_csv(rows: list[dict]):
    OUTPUT_DIR.mkdir(exist_ok=True)
    out = OUTPUT_DIR / "traceability-matrix.csv"
    fields = list(rows[0].keys()) if rows else []
    with open(out, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    print(f"  Written: {out}")


def write_md(rows: list[dict], catalog: dict):
    OUTPUT_DIR.mkdir(exist_ok=True)
    out = OUTPUT_DIR / "traceability-matrix.md"
    lines = [
        "# EAP Traceability Matrix",
        "",
        f"Generated from `{CATALOG_PATH.relative_to(REPO_ROOT)}` (v{catalog.get('version', 'N/A')}).",
        "",
        "| Control ID | Title | Family | Levels | Strength | ATAL References | Repo Sources |",
        "|---|---|---|:---:|:---:|---|---|",
    ]
    for row in rows:
        lines.append(
            f"| {row['control_id']} | {row['title']} | {row['family']} "
            f"| {row['assurance_levels']} | {row['normative_strength']} "
            f"| {row['atal_references']} | {row['repo_sources']} |"
        )
    lines += [
        "",
        "## Risk and Compensating Control Cross-Reference",
        "",
        "| Control ID | Related Risks | Compensating Controls | Automation Candidate |",
        "|---|---|---|:---:|",
    ]
    for row in rows:
        lines.append(
            f"| {row['control_id']} | {row['related_risks']} "
            f"| {row['compensating_controls']} | {row['automation_candidate']} |"
        )
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"  Written: {out}")


def main():
    parser = argparse.ArgumentParser(description="Build the EAP traceability matrix from the control catalog.")
    parser.add_argument("--format", default="all", choices=VALID_FORMATS)
    args = parser.parse_args()

    if not CATALOG_PATH.exists():
        print(f"ERROR: Catalog not found: {CATALOG_PATH}", file=sys.stderr)
        sys.exit(2)

    print(f"Loading catalog: {CATALOG_PATH}")
    catalog = load_json(CATALOG_PATH)
    rows = build_matrix(catalog)
    print(f"  Controls: {len(rows)}")

    fmt = args.format
    if fmt in ("json", "all"):
        write_json(rows, catalog)
    if fmt in ("csv", "all"):
        write_csv(rows)
    if fmt in ("md", "all"):
        write_md(rows, catalog)

    print("Done.")


if __name__ == "__main__":
    main()
