#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
import re
import sys
import yaml

ROOT = Path(__file__).resolve().parents[1]
DECL = ROOT / "assurance/stable-contracts.yaml"


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    failures: list[str] = []
    contract = yaml.safe_load(DECL.read_text(encoding="utf-8"))
    for schema_path in contract["schemas"]:
        path = ROOT / schema_path
        if not path.exists():
            failures.append(f"stable schema missing: {schema_path}")
            continue
        try:
            load_json(path)
        except Exception as exc:
            failures.append(f"stable schema not parseable: {schema_path}: {exc}")

    claim = load_json(ROOT / "schemas/assurance-claim.schema.json")
    claim_states = set(claim["properties"]["state"]["enum"])
    missing_claim_states = sorted(set(contract["claim_states"]) - claim_states)
    if missing_claim_states:
        failures.append("claim states removed/renamed: " + ", ".join(missing_claim_states))

    result_schema = load_json(ROOT / "schemas/test-result.schema.json")
    result_states = set(result_schema["properties"]["result"]["enum"])
    missing_result_states = sorted(set(contract["test_result_states"]) - result_states)
    if missing_result_states:
        failures.append("test-result states removed/renamed: " + ", ".join(missing_result_states))

    control_pattern = contract["identifiers"]["control_id_pattern"]
    test_pattern = contract["identifiers"]["test_id_pattern"]
    if not re.fullmatch(control_pattern, "EAP-CTRL-001"):
        failures.append("declared control identifier pattern no longer accepts canonical IDs")
    if not re.fullmatch(test_pattern, "EAP-TEST-NB-001"):
        failures.append("declared test identifier pattern no longer accepts canonical IDs")

    catalog_schema = load_json(ROOT / "schemas/control-catalog.schema.json")
    control_schema_text = json.dumps(catalog_schema)
    test_schema_text = json.dumps(result_schema)
    if "EAP-CTRL" not in control_schema_text:
        failures.append("control catalog schema no longer exposes EAP control identifier semantics")
    if "EAP-TEST" not in test_schema_text:
        failures.append("test result schema no longer exposes EAP test identifier semantics")

    if failures:
        print("✗ candidate contract compatibility FAILED", file=sys.stderr)
        for failure in failures:
            print(f"  - {failure}", file=sys.stderr)
        return 1
    print(f"✓ candidate contract compatibility passed ({len(contract['schemas'])} stable schemas)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
