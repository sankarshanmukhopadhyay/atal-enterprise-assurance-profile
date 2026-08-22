#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys

import yaml
from jsonschema import Draft7Validator, Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
CASE = ROOT / "examples" / "eap-l3-worked-example"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def schema_errors(instance, schema_path: Path, cls) -> list[str]:
    schema = load(schema_path)
    return [e.message for e in cls(schema).iter_errors(instance)]


def derives_l3(profile: dict) -> bool:
    return any([
        profile["impact"]["safety"],
        profile["impact"]["rights_affecting"],
        profile["impact"]["critical_operations"],
        profile["autonomy"]["self_modification"],
    ])


def main() -> int:
    failures: list[str] = []
    profile = load(CASE / "deployment-profile.json")
    bundle = load(CASE / "evidence-bundle.json")
    assessment = load(CASE / "assessment-result.json")
    overlay = load(ROOT / "catalogs/assurance-level-overlays/EAP-L3-overlay.json")

    for msg in schema_errors(profile, ROOT / "schemas/deployment-profile.schema.json", Draft202012Validator):
        failures.append(f"deployment profile: {msg}")
    for msg in schema_errors(bundle, ROOT / "schemas/evidence-bundle.schema.json", Draft7Validator):
        failures.append(f"evidence bundle: {msg}")
    for msg in schema_errors(assessment, ROOT / "schemas/assessment-result.schema.json", Draft7Validator):
        failures.append(f"assessment: {msg}")

    if not derives_l3(profile):
        failures.append("deployment characteristics do not deterministically derive EAP-L3")
    if bundle.get("assurance_level") != "EAP-L3" or assessment.get("assurance_level") != "EAP-L3":
        failures.append("bundle and assessment must both declare EAP-L3")

    mandatory = set(overlay.get("mandatory_control_ids", []))
    bundle_by_id = {x["control_id"]: x for x in bundle.get("control_evidence_items", [])}
    result_by_id = {x["control_id"]: x for x in assessment.get("control_results", [])}
    if mandatory != set(bundle_by_id):
        failures.append("L3 evidence bundle must contain exactly all mandatory controls")
    if mandatory != set(result_by_id):
        failures.append("L3 assessment must contain exactly all mandatory controls")
    for cid in sorted(mandatory):
        if bundle_by_id.get(cid, {}).get("status") not in {"pass", "waived"}:
            failures.append(f"mandatory evidence status is not pass/waived: {cid}")
        if result_by_id.get(cid, {}).get("result") not in {"pass", "waived"}:
            failures.append(f"mandatory assessment result is not pass/waived: {cid}")
    if assessment.get("decision", {}).get("outcome") != "conformant":
        failures.append("worked L3 assessment must be conformant")

    known_tests: dict[str, set[str]] = {}
    for path in (ROOT / "tests" / "catalog").glob("*.yaml"):
        item = yaml.safe_load(path.read_text(encoding="utf-8"))
        known_tests[item["test_id"]] = set(item["control_ids"])

    positives = sorted((CASE / "test-results").glob("*.json"))
    required_positive_ids = {
        "EAP-TEST-EI-001", "EAP-TEST-RP-001", "EAP-TEST-RC-001",
        "EAP-TEST-DC-001", "EAP-TEST-DB-001", "EAP-TEST-NB-001", "EAP-TEST-KS-001",
    }
    seen: set[str] = set()
    for path in positives:
        result = load(path)
        for msg in schema_errors(result, ROOT / "schemas/test-result.schema.json", Draft202012Validator):
            failures.append(f"{path.name}: {msg}")
        tid = result.get("test_id")
        seen.add(tid)
        if tid not in known_tests:
            failures.append(f"unknown positive test id: {tid}")
            continue
        if not set(result.get("control_ids", [])).issubset(known_tests[tid]):
            failures.append(f"positive fixture control binding exceeds catalog: {tid}")
        if result.get("result") != "pass":
            failures.append(f"positive fixture must pass: {tid}")
    missing_positive = sorted(required_positive_ids - seen)
    if missing_positive:
        failures.append("missing positive fixtures: " + ", ".join(missing_positive))

    negatives = sorted((CASE / "negative-fixtures").glob("*.json"))
    if len(negatives) < 2:
        failures.append("at least two adversarial negative fixtures are required")
    for path in negatives:
        result = load(path)
        for msg in schema_errors(result, ROOT / "schemas/test-result.schema.json", Draft202012Validator):
            failures.append(f"negative {path.name}: {msg}")
        tid = result.get("test_id")
        if tid not in known_tests:
            failures.append(f"unknown negative test id: {tid}")
        if result.get("result") != "fail":
            failures.append(f"negative fixture must encode a failing outcome: {path.name}")

    critical_requirements = {
        "EAP-CTRL-001": "EAP-TEST-EI-001.json",
        "EAP-CTRL-003": "EAP-TEST-EI-001.json",
        "EAP-CTRL-004": "EAP-TEST-RC-001.json",
        "EAP-CTRL-005": "EAP-TEST-RC-001.json",
        "EAP-CTRL-006": "EAP-TEST-RP-001.json",
        "EAP-CTRL-007": "EAP-TEST-NB-001.json",
        "EAP-CTRL-014": "EAP-TEST-NB-001.json",
        "EAP-CTRL-015": "EAP-TEST-RC-001.json",
        "EAP-CTRL-016": "EAP-TEST-DC-001.json",
        "EAP-CTRL-017": "EAP-TEST-DB-001.json",
        "EAP-CTRL-018": "EAP-TEST-DB-001.json",
        "EAP-CTRL-019": "EAP-TEST-DC-001.json",
    }
    for cid, expected in critical_requirements.items():
        artifacts = bundle_by_id.get(cid, {}).get("evidence_artifacts", [])
        qualifying = [a for a in artifacts if a.get("evidence_grade") in {"E4", "E5"} and a.get("path_or_url", "").endswith(expected)]
        if not qualifying:
            failures.append(f"critical L3 control lacks required E4+ executable evidence: {cid} -> {expected}")

    if failures:
        print("✗ EAP-L3 adversarial worked-example validation FAILED", file=sys.stderr)
        for f in failures:
            print(f"  - {f}", file=sys.stderr)
        return 1

    print("✓ EAP-L3 adversarial worked-example validation passed")
    print(f"  mandatory controls: {len(mandatory)}")
    print(f"  positive executable fixtures: {len(positives)}")
    print(f"  negative adversarial fixtures: {len(negatives)}")
    print(f"  evidence sha256: {hashlib.sha256((CASE / 'evidence-bundle.json').read_bytes()).hexdigest()}")
    print(f"  assessment sha256: {hashlib.sha256((CASE / 'assessment-result.json').read_bytes()).hexdigest()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
