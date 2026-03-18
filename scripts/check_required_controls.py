#!/usr/bin/env python3
"""
check_required_controls.py — Check whether all mandatory controls for the
selected assurance level are present and assessed in an evidence bundle or
assessment result.

Usage:
    python scripts/check_required_controls.py --level EAP-L1 --bundle evidence/samples/eap-l1-sample-evidence-bundle.json
    python scripts/check_required_controls.py --level EAP-L1 --result assessments/samples/eap-l1-sample-assessment.json
"""

import sys
import json
import pathlib
import argparse


REPO_ROOT = pathlib.Path(__file__).parent.parent
OVERLAY_DIR = REPO_ROOT / "catalogs" / "assurance-level-overlays"

VALID_LEVELS = ["EAP-L1", "EAP-L2", "EAP-L3"]
PASSING_STATUSES = {"pass", "waived"}


def load_json(path: pathlib.Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def get_mandatory_ids(level: str) -> set[str]:
    overlay_path = OVERLAY_DIR / f"{level}-overlay.json"
    if not overlay_path.exists():
        print(f"ERROR: Overlay not found: {overlay_path}", file=sys.stderr)
        sys.exit(2)
    overlay = load_json(overlay_path)
    return set(overlay.get("mandatory_control_ids", []))


def check_bundle(mandatory_ids: set[str], bundle: dict) -> tuple[list, list, list]:
    items = bundle.get("control_evidence_items", [])
    assessed = {item["control_id"]: item["status"] for item in items}
    missing, failing, passing = [], [], []
    for ctrl_id in sorted(mandatory_ids):
        if ctrl_id not in assessed:
            missing.append(ctrl_id)
        elif assessed[ctrl_id] not in PASSING_STATUSES:
            failing.append((ctrl_id, assessed[ctrl_id]))
        else:
            passing.append((ctrl_id, assessed[ctrl_id]))
    return missing, failing, passing


def check_result(mandatory_ids: set[str], result: dict) -> tuple[list, list, list]:
    items = result.get("control_results", [])
    assessed = {item["control_id"]: item["result"] for item in items}
    missing, failing, passing = [], [], []
    for ctrl_id in sorted(mandatory_ids):
        if ctrl_id not in assessed:
            missing.append(ctrl_id)
        elif assessed[ctrl_id] not in PASSING_STATUSES:
            failing.append((ctrl_id, assessed[ctrl_id]))
        else:
            passing.append((ctrl_id, assessed[ctrl_id]))
    return missing, failing, passing


def main():
    parser = argparse.ArgumentParser(description="Check required controls for an assurance level.")
    parser.add_argument("--level", required=True, choices=VALID_LEVELS)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--bundle", help="Path to evidence bundle JSON")
    group.add_argument("--result", help="Path to assessment result JSON")
    args = parser.parse_args()

    mandatory_ids = get_mandatory_ids(args.level)
    print(f"Mandatory controls for {args.level}: {len(mandatory_ids)}")

    if args.bundle:
        path = pathlib.Path(args.bundle)
        if not path.exists():
            print(f"ERROR: File not found: {path}", file=sys.stderr)
            sys.exit(2)
        artifact = load_json(path)
        missing, failing, passing = check_bundle(mandatory_ids, artifact)
        source_label = "evidence bundle"
    else:
        path = pathlib.Path(args.result)
        if not path.exists():
            print(f"ERROR: File not found: {path}", file=sys.stderr)
            sys.exit(2)
        artifact = load_json(path)
        missing, failing, passing = check_result(mandatory_ids, artifact)
        source_label = "assessment result"

    print(f"Checking {source_label}: {path}\n")

    if passing:
        print(f"✓ Passing mandatory controls ({len(passing)}):")
        for ctrl_id, status in passing:
            print(f"    {ctrl_id}  [{status}]")

    if missing:
        print(f"\n✗ Missing mandatory controls ({len(missing)}) — not present in {source_label}:")
        for ctrl_id in missing:
            print(f"    {ctrl_id}")

    if failing:
        print(f"\n✗ Failing mandatory controls ({len(failing)}):")
        for ctrl_id, status in failing:
            print(f"    {ctrl_id}  [{status}]")

    total_issues = len(missing) + len(failing)
    print()
    if total_issues == 0:
        print(f"✓ All {len(mandatory_ids)} mandatory controls pass for {args.level}.")
        sys.exit(0)
    else:
        print(f"✗ {total_issues} issue(s) found. Level {args.level} conformance requirements are NOT met.", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
