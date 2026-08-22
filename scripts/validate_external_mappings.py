#!/usr/bin/env python3
"""Validate external framework mappings and ensure referenced EAP controls exist."""
from __future__ import annotations

import json
from pathlib import Path
import sys

import yaml
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
MAPPING_PATH = ROOT / "mappings/external-framework-mappings.yaml"
SCHEMA_PATH = ROOT / "schemas/external-framework-mapping.schema.json"
CATALOG_PATH = ROOT / "catalogs/atal-eap-control-catalog.yaml"


def main() -> int:
    mappings = yaml.safe_load(MAPPING_PATH.read_text(encoding="utf-8"))
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    catalog = yaml.safe_load(CATALOG_PATH.read_text(encoding="utf-8"))

    failures = 0
    for error in Draft202012Validator(schema).iter_errors(mappings):
        where = ".".join(str(p) for p in error.path) or "<root>"
        print(f"ERROR {where}: {error.message}", file=sys.stderr)
        failures += 1

    controls = {control["id"] for control in catalog.get("controls", [])}
    frameworks = set(mappings.get("frameworks", {}).keys())
    seen: set[tuple[str, str, str]] = set()

    for item in mappings.get("mappings", []):
        if item["control_id"] not in controls:
            print(f"ERROR: unknown control {item['control_id']}", file=sys.stderr)
            failures += 1
        if item["framework"] not in frameworks:
            print(f"ERROR: unknown framework {item['framework']}", file=sys.stderr)
            failures += 1
        key = (item["control_id"], item["framework"], item["target"])
        if key in seen:
            print(f"ERROR: duplicate mapping {key}", file=sys.stderr)
            failures += 1
        seen.add(key)
        if item["relationship"] == "supports" and item["confidence"] == "low":
            print(f"ERROR: strong 'supports' mapping cannot have low confidence: {key}", file=sys.stderr)
            failures += 1

    print(f"Validated {len(mappings.get('mappings', []))} external mapping assertions across {len(frameworks)} frameworks.")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
