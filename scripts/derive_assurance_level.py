#!/usr/bin/env python3
"""Derive the minimum EAP assurance level from a deployment profile."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = json.loads((ROOT / "schemas/deployment-profile.schema.json").read_text(encoding="utf-8"))


def derive(profile: dict) -> tuple[str, list[str]]:
    autonomy = profile["autonomy"]
    impact = profile["impact"]
    environment = profile["environment"]
    reasons: list[str] = []

    if any([impact["safety"], impact["rights_affecting"], impact["critical_operations"], autonomy["self_modification"]]):
        if impact["safety"]: reasons.append("safety impact")
        if impact["rights_affecting"]: reasons.append("rights-affecting decisions")
        if impact["critical_operations"]: reasons.append("critical operations")
        if autonomy["self_modification"]: reasons.append("self-modification")
        return "EAP-L3", reasons

    l2_signals = [
        (autonomy["tool_use"], "tool use"),
        (autonomy["persistent_memory"], "persistent memory"),
        (autonomy["external_side_effects"], "external side effects"),
        (impact["financial"], "financial impact"),
        (impact["regulated_data"], "regulated data"),
        (environment["production"], "production deployment"),
        (environment["internet_exposed"], "internet exposure"),
    ]
    reasons = [label for active, label in l2_signals if active]
    return ("EAP-L2", reasons) if reasons else ("EAP-L1", ["baseline deployment characteristics"])


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("profile")
    args = parser.parse_args()
    profile = json.loads(Path(args.profile).read_text(encoding="utf-8"))
    errors = list(Draft202012Validator(SCHEMA).iter_errors(profile))
    if errors:
        for error in errors:
            print(f"ERROR: {error.message}", file=sys.stderr)
        return 1
    level, reasons = derive(profile)
    print(json.dumps({"minimum_assurance_level": level, "reasons": reasons}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
