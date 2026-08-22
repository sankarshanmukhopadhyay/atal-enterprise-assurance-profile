#!/usr/bin/env python3
"""Validate all declarative EAP conformance test vectors."""
from __future__ import annotations

import json
from pathlib import Path
import sys

import yaml
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = json.loads((ROOT / "schemas/test-case.schema.json").read_text(encoding="utf-8"))
CATALOG = ROOT / "tests/catalog"


def main() -> int:
    validator = Draft202012Validator(SCHEMA)
    seen: set[str] = set()
    failures = 0
    files = sorted(CATALOG.glob("*.yaml"))
    if not files:
        print("ERROR: no executable test vectors found", file=sys.stderr)
        return 1

    for path in files:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        errors = sorted(validator.iter_errors(data), key=lambda e: list(e.path))
        if data.get("test_id") in seen:
            print(f"ERROR {path}: duplicate test_id {data.get('test_id')}", file=sys.stderr)
            failures += 1
        seen.add(data.get("test_id"))
        for error in errors:
            where = ".".join(str(p) for p in error.path) or "<root>"
            print(f"ERROR {path}:{where}: {error.message}", file=sys.stderr)
            failures += 1
        if not errors:
            print(f"OK: {data['test_id']} -> {', '.join(data['control_ids'])}")

    print(f"Validated {len(files)} executable test vector(s).")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
