#!/usr/bin/env python3
"""Grade an EAP evidence bundle against the repository evidence-strength model."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

import yaml

ROOT = Path(__file__).resolve().parents[1]
MODEL = yaml.safe_load((ROOT / "evidence/evidence-strength-model.yaml").read_text(encoding="utf-8"))


def artifact_grade(artifact_type: str) -> tuple[str, int]:
    best = ("E0", 0)
    for grade, definition in MODEL["grades"].items():
        if artifact_type in definition.get("artifact_types", []):
            rank = int(definition["rank"])
            if rank > best[1]:
                best = (grade, rank)
    return best


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("bundle")
    parser.add_argument("--strict", action="store_true", help="Exit non-zero when any passing control is below the level minimum.")
    args = parser.parse_args()

    bundle = json.loads(Path(args.bundle).read_text(encoding="utf-8"))
    level = bundle["assurance_level"]
    minimum = MODEL["minimums"][level]["default_minimum_grade"]
    minimum_rank = MODEL["grades"][minimum]["rank"]

    results = []
    failures = 0
    for item in bundle.get("control_evidence_items", []):
        if item.get("status") in {"not_applicable", "waived"}:
            continue
        grades = [artifact_grade(a.get("artifact_type", "")) for a in item.get("evidence_artifacts", [])]
        observed = max(grades, key=lambda g: g[1]) if grades else ("E0", 0)
        sufficient = observed[1] >= minimum_rank
        if item.get("status") == "pass" and not sufficient:
            failures += 1
        results.append({
            "control_id": item["control_id"],
            "status": item.get("status"),
            "observed_grade": observed[0],
            "required_minimum": minimum,
            "sufficient": sufficient,
        })

    output = {
        "bundle_id": bundle.get("bundle_id"),
        "assurance_level": level,
        "default_minimum_grade": minimum,
        "controls": results,
        "below_minimum_count": failures,
    }
    print(json.dumps(output, indent=2))
    if args.strict and failures:
        print(f"ERROR: {failures} passing control(s) are supported only by evidence below {minimum}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
