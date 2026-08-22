#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys

from jsonschema import Draft7Validator, Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
CASE = ROOT / "examples" / "eap-l2-worked-example"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def validate_schema(instance, schema_path: Path, validator_cls) -> list[str]:
    schema = load(schema_path)
    return [error.message for error in validator_cls(schema).iter_errors(instance)]


def derive_l2(profile: dict) -> bool:
    if any([
        profile["impact"]["safety"],
        profile["impact"]["rights_affecting"],
        profile["impact"]["critical_operations"],
        profile["autonomy"]["self_modification"],
    ]):
        return False
    return any([
        profile["autonomy"]["tool_use"],
        profile["autonomy"]["persistent_memory"],
        profile["autonomy"]["external_side_effects"],
        profile["impact"]["financial"],
        profile["impact"]["regulated_data"],
        profile["environment"]["production"],
        profile["environment"]["internet_exposed"],
    ])


def main() -> int:
    failures: list[str] = []
    profile = load(CASE / "deployment-profile.json")
    bundle = load(CASE / "evidence-bundle.json")
    assessment = load(CASE / "assessment-result.json")
    overlay = load(ROOT / "catalogs/assurance-level-overlays/EAP-L2-overlay.json")

    for message in validate_schema(profile, ROOT / "schemas/deployment-profile.schema.json", Draft202012Validator):
        failures.append(f"deployment profile: {message}")
    for message in validate_schema(bundle, ROOT / "schemas/evidence-bundle.schema.json", Draft7Validator):
        failures.append(f"evidence bundle: {message}")
    for message in validate_schema(assessment, ROOT / "schemas/assessment-result.schema.json", Draft7Validator):
        failures.append(f"assessment: {message}")

    if not derive_l2(profile):
        failures.append("deployment characteristics do not deterministically derive EAP-L2")
    if bundle.get("assurance_level") != "EAP-L2" or assessment.get("assurance_level") != "EAP-L2":
        failures.append("bundle and assessment must both declare EAP-L2")

    mandatory = set(overlay.get("mandatory_control_ids", []))
    bundle_by_id = {item["control_id"]: item for item in bundle.get("control_evidence_items", [])}
    result_by_id = {item["control_id"]: item for item in assessment.get("control_results", [])}
    missing_bundle = sorted(mandatory - set(bundle_by_id))
    missing_result = sorted(mandatory - set(result_by_id))
    if missing_bundle:
        failures.append("mandatory controls missing from evidence: " + ", ".join(missing_bundle))
    if missing_result:
        failures.append("mandatory controls missing from assessment: " + ", ".join(missing_result))

    for control_id in sorted(mandatory):
        if bundle_by_id.get(control_id, {}).get("status") not in {"pass", "waived"}:
            failures.append(f"mandatory evidence status is not pass/waived: {control_id}")
        if result_by_id.get(control_id, {}).get("result") not in {"pass", "waived"}:
            failures.append(f"mandatory assessment result is not pass/waived: {control_id}")

    if assessment.get("decision", {}).get("outcome") != "conformant":
        failures.append("worked L2 assessment must be conformant")

    known_tests = {}
    for path in (ROOT / "tests/catalog").glob("*.yaml"):
        import yaml
        item = yaml.safe_load(path.read_text(encoding="utf-8"))
        known_tests[item["test_id"]] = set(item["control_ids"])

    for filename in ["EAP-TEST-NB-001.json", "EAP-TEST-KS-001.json"]:
        result = load(CASE / "test-results" / filename)
        for message in validate_schema(result, ROOT / "schemas/test-result.schema.json", Draft202012Validator):
            failures.append(f"{filename}: {message}")
        test_id = result.get("test_id")
        if test_id not in known_tests:
            failures.append(f"unknown test id in result: {test_id}")
            continue
        if not set(result.get("control_ids", [])).issubset(known_tests[test_id]):
            failures.append(f"test result control binding exceeds catalog definition: {test_id}")
        if result.get("result") != "pass":
            failures.append(f"worked example test must pass: {test_id}")

    # Verify the evidence bundle actually points to the executable test results used for
    # EAP-CTRL-007/014/016 rather than merely asserting that those controls passed.
    required_test_refs = {
        "EAP-CTRL-007": "EAP-TEST-NB-001.json",
        "EAP-CTRL-014": "EAP-TEST-NB-001.json",
        "EAP-CTRL-016": "EAP-TEST-KS-001.json",
    }
    for control_id, expected in required_test_refs.items():
        refs = [a.get("path_or_url", "") for a in bundle_by_id[control_id].get("evidence_artifacts", [])]
        if not any(ref.endswith(expected) for ref in refs):
            failures.append(f"{control_id} is missing executable test evidence {expected}")

    if failures:
        print("✗ EAP-L2 worked-example validation FAILED", file=sys.stderr)
        for failure in failures:
            print(f"  - {failure}", file=sys.stderr)
        return 1

    evidence_digest = hashlib.sha256((CASE / "evidence-bundle.json").read_bytes()).hexdigest()
    assessment_digest = hashlib.sha256((CASE / "assessment-result.json").read_bytes()).hexdigest()
    print("✓ EAP-L2 worked-example validation passed")
    print(f"  mandatory controls: {len(mandatory)}")
    print(f"  evidence sha256: {evidence_digest}")
    print(f"  assessment sha256: {assessment_digest}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
