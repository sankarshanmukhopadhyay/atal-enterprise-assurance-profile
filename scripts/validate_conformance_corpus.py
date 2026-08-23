#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
import sys
import yaml
from jsonschema import Draft7Validator, Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "tests/fixtures/conformance/manifest.yaml"


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def validator_for(schema: dict):
    uri = schema.get("$schema", "")
    return Draft7Validator if "draft-07" in uri else Draft202012Validator


def main() -> int:
    corpus = yaml.safe_load(MANIFEST.read_text(encoding="utf-8"))
    failures: list[str] = []
    valid_count = 0
    invalid_count = 0
    for fixture in corpus["fixtures"]:
        schema_path = ROOT / fixture["schema"]
        instance_path = ROOT / fixture["instance"]
        if not schema_path.exists() or not instance_path.exists():
            failures.append(f"{fixture['id']}: schema or instance missing")
            continue
        schema = load_json(schema_path)
        instance = load_json(instance_path)
        errors = list(validator_for(schema)(schema).iter_errors(instance))
        actual = "invalid" if errors else "valid"
        if actual != fixture["expected"]:
            failures.append(f"{fixture['id']}: expected {fixture['expected']}, got {actual}")
        if fixture["expected"] == "valid":
            valid_count += 1
        else:
            invalid_count += 1
    if valid_count == 0 or invalid_count == 0:
        failures.append("conformance corpus must contain both positive and negative fixtures")
    if failures:
        print("✗ conformance corpus validation FAILED", file=sys.stderr)
        for failure in failures:
            print(f"  - {failure}", file=sys.stderr)
        return 1
    print(f"✓ conformance corpus passed ({valid_count} positive, {invalid_count} negative fixtures)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
