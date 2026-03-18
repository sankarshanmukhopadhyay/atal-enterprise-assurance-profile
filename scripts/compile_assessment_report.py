#!/usr/bin/env python3
"""
compile_assessment_report.py — Merge profile overlay, evidence bundle, and
assessment result into a human-readable Markdown assessment report.

Usage:
    python scripts/compile_assessment_report.py \\
        --level EAP-L1 \\
        --bundle evidence/samples/eap-l1-sample-evidence-bundle.json \\
        --result assessments/samples/eap-l1-sample-assessment.json \\
        [--output artifacts/EAP-L1-assessment-report.md]
"""

import sys
import json
import pathlib
import argparse
from datetime import date


REPO_ROOT = pathlib.Path(__file__).parent.parent
CATALOG_PATH = REPO_ROOT / "catalogs" / "atal-eap-control-catalog.json"
OVERLAY_DIR = REPO_ROOT / "catalogs" / "assurance-level-overlays"
OUTPUT_DIR = REPO_ROOT / "artifacts"

VALID_LEVELS = ["EAP-L1", "EAP-L2", "EAP-L3"]

STATUS_EMOJI = {
    "pass": "✅",
    "fail": "❌",
    "partial": "⚠️",
    "not_applicable": "—",
    "waived": "〰️",
}


def load_json(path: pathlib.Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main():
    parser = argparse.ArgumentParser(description="Compile a Markdown assessment report from EAP artifacts.")
    parser.add_argument("--level", required=True, choices=VALID_LEVELS)
    parser.add_argument("--bundle", required=True, help="Path to evidence bundle JSON")
    parser.add_argument("--result", required=True, help="Path to assessment result JSON")
    parser.add_argument("--output", default=None, help="Output path for the report (default: artifacts/<level>-assessment-report.md)")
    args = parser.parse_args()

    bundle_path = pathlib.Path(args.bundle)
    result_path = pathlib.Path(args.result)
    overlay_path = OVERLAY_DIR / f"{args.level}-overlay.json"

    for p in [bundle_path, result_path, overlay_path, CATALOG_PATH]:
        if not p.exists():
            print(f"ERROR: File not found: {p}", file=sys.stderr)
            sys.exit(2)

    catalog = load_json(CATALOG_PATH)
    overlay = load_json(overlay_path)
    bundle = load_json(bundle_path)
    result = load_json(result_path)

    ctrl_index = {c["id"]: c for c in catalog["controls"]}
    bundle_index = {i["control_id"]: i for i in bundle.get("control_evidence_items", [])}
    result_index = {r["control_id"]: r for r in result.get("control_results", [])}
    mandatory_ids = set(overlay.get("mandatory_control_ids", []))

    decision = result.get("decision", {})
    outcome = decision.get("outcome", "N/A")
    system = bundle.get("assessed_system", {})
    period = bundle.get("assessment_period", {})
    attestation = bundle.get("attestation", {})

    lines = [
        f"# EAP Assessment Report — {args.level}",
        "",
        f"**Assurance level:** {args.level}  ",
        f"**Assessment ID:** {result.get('assessment_id', 'N/A')}  ",
        f"**Assessment date:** {result.get('assessment_date', 'N/A')}  ",
        f"**Assessor:** {result.get('assessor', 'N/A')}  ",
        f"**Report compiled:** {date.today().isoformat()}  ",
        "",
        "---",
        "",
        "## System",
        "",
        f"| Field | Value |",
        f"|---|---|",
        f"| System name | {system.get('name', 'N/A')} |",
        f"| Version | {system.get('version', 'N/A')} |",
        f"| Environment | {system.get('environment', 'N/A')} |",
        f"| Assessment period | {period.get('start', 'N/A')} to {period.get('end', 'N/A')} |",
        f"| Attested by | {attestation.get('attested_by', 'N/A')} ({attestation.get('attestation_role', 'N/A')}) |",
        "",
        "---",
        "",
        "## Decision",
        "",
        f"**Outcome: {outcome.upper()}**",
        "",
        f"{decision.get('summary', '')}",
    ]

    conditions = decision.get("conditions", [])
    if conditions:
        lines += ["", "**Conditions:**", ""]
        for cond in conditions:
            lines.append(f"- {cond}")

    valid_until = decision.get("valid_until")
    if valid_until:
        lines += ["", f"**Valid until:** {valid_until}"]

    lines += [
        "",
        "---",
        "",
        "## Control Results",
        "",
        "| Control ID | Title | Family | Mandatory | Result | Finding |",
        "|---|---|---|:---:|:---:|---|",
    ]

    for ctrl_id in sorted(ctrl_index.keys()):
        ctrl = ctrl_index[ctrl_id]
        res = result_index.get(ctrl_id, {})
        result_val = res.get("result", "—")
        emoji = STATUS_EMOJI.get(result_val, result_val)
        mandatory = "**Yes**" if ctrl_id in mandatory_ids else "No"
        finding = res.get("finding", "") or ""
        lines.append(
            f"| {ctrl_id} | {ctrl['title']} | {ctrl['family']} | {mandatory} | {emoji} {result_val} | {finding} |"
        )

    # Summary counts
    all_results = [r.get("result", "") for r in result.get("control_results", [])]
    counts = {s: all_results.count(s) for s in ["pass", "fail", "partial", "not_applicable", "waived"]}

    lines += [
        "",
        "**Summary:**",
        "",
        f"| Status | Count |",
        f"|---|:---:|",
    ]
    for status, count in counts.items():
        lines.append(f"| {status} | {count} |")

    # Findings
    findings = result.get("findings", [])
    if findings:
        lines += [
            "",
            "---",
            "",
            "## Findings",
            "",
            "| Finding ID | Control | Severity | Description | Remediation Target |",
            "|---|---|:---:|---|:---:|",
        ]
        for f in findings:
            lines.append(
                f"| {f.get('finding_id', '')} | {f.get('control_id', '')} | {f.get('severity', '')} "
                f"| {f.get('description', '')} | {f.get('remediation_target_date', '—')} |"
            )

    # Residual risks
    risks = result.get("residual_risks", [])
    if risks:
        lines += [
            "",
            "---",
            "",
            "## Residual Risks",
            "",
            "| Risk ID | Description | Controls | Accepted By | Acceptance Date |",
            "|---|---|---|---|:---:|",
        ]
        for r in risks:
            ctrl_refs = ", ".join(r.get("related_control_ids", []))
            lines.append(
                f"| {r.get('risk_id', '')} | {r.get('description', '')} | {ctrl_refs} "
                f"| {r.get('accepted_by', '')} | {r.get('acceptance_date', '—')} |"
            )

    # Evidence references per control
    lines += [
        "",
        "---",
        "",
        "## Evidence References",
        "",
    ]
    for ctrl_id in sorted(bundle_index.keys()):
        bitem = bundle_index[ctrl_id]
        artifacts = bitem.get("evidence_artifacts", [])
        if not artifacts:
            continue
        ctrl_title = ctrl_index.get(ctrl_id, {}).get("title", ctrl_id)
        lines += [f"### {ctrl_id} — {ctrl_title}", ""]
        for art in artifacts:
            ref = art.get("path_or_url", "")
            lines.append(f"- **{art.get('artifact_id', '')}**: {art.get('description', '')}  ")
            if ref:
                lines.append(f"  `{ref}`")
        lines.append("")

    lines += [
        "---",
        "",
        "*Report generated by `scripts/compile_assessment_report.py`. "
        "Review all referenced evidence artifacts before relying on this report for conformance decisions.*",
        "",
    ]

    OUTPUT_DIR.mkdir(exist_ok=True)
    out_path = pathlib.Path(args.output) if args.output else OUTPUT_DIR / f"{args.level}-assessment-report.md"
    out_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"✓ Report written to: {out_path}")


if __name__ == "__main__":
    main()
