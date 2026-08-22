#!/usr/bin/env python3
"""Cross-artifact assurance invariant checks for the v0.9 candidate."""
from __future__ import annotations

import json
from pathlib import Path
import sys

import yaml

ROOT = Path(__file__).resolve().parents[1]


def fail(message: str, failures: list[str]) -> None:
    failures.append(message)
    print(f"ERROR: {message}", file=sys.stderr)


def main() -> int:
    failures: list[str] = []

    baseline = yaml.safe_load((ROOT / "upstream/atal-baseline.yaml").read_text(encoding="utf-8"))
    commit = baseline.get("upstream", {}).get("commit", "")
    compat = baseline.get("upstream", {}).get("compatibility_class")
    if len(commit) != 40 or not compat:
        fail("EAP-INV-001 upstream provenance is incomplete", failures)

    catalog = yaml.safe_load((ROOT / "catalogs/atal-eap-control-catalog.yaml").read_text(encoding="utf-8"))
    controls = {c["id"] for c in catalog.get("controls", [])}
    mappings = yaml.safe_load((ROOT / "mappings/external-framework-mappings.yaml").read_text(encoding="utf-8"))
    frameworks = set(mappings.get("frameworks", {}))
    for mapping in mappings.get("mappings", []):
        if mapping["control_id"] not in controls or mapping["framework"] not in frameworks:
            fail(f"EAP-INV-002 unresolved external mapping {mapping}", failures)

    for path in sorted((ROOT / "tests/catalog").glob("*.yaml")):
        case = yaml.safe_load(path.read_text(encoding="utf-8"))
        if not case.get("control_ids") or case.get("evidence_grade") not in {"E3", "E4", "E5"}:
            fail(f"EAP-INV-003 invalid executable test vector {path.name}", failures)
        for control_id in case.get("control_ids", []):
            if control_id not in controls:
                fail(f"EAP-INV-003 test {case.get('test_id')} references unknown {control_id}", failures)

    claim_schema = json.loads((ROOT / "schemas/assurance-claim.schema.json").read_text(encoding="utf-8"))
    states = set(claim_schema["properties"]["state"]["enum"])
    if not {"EXPIRED", "REVOKED"}.issubset(states):
        fail("EAP-INV-004 claim schema lacks expiry/revocation lifecycle", failures)

    evidence = yaml.safe_load((ROOT / "evidence/evidence-strength-model.yaml").read_text(encoding="utf-8"))
    ranks = evidence["grades"]
    minimums = evidence["minimums"]
    sequence = [ranks[minimums[level]["default_minimum_grade"]]["rank"] for level in ("EAP-L1", "EAP-L2", "EAP-L3")]
    if not sequence[0] < sequence[1] < sequence[2]:
        fail(f"EAP-INV-005 evidence minimums are not strictly increasing: {sequence}", failures)

    gate = (ROOT / "scripts/run_quality_gate.py").read_text(encoding="utf-8")
    required = [
        "check_upstream_integrity.py",
        "validate_test_catalog.py",
        "validate_external_mappings.py",
        "check_assurance_invariants.py",
        "validate_l2_worked_example.py",
        "validate_l3_worked_example.py",
    ]
    missing = [name for name in required if name not in gate]
    if missing:
        fail(f"EAP-INV-006 quality gate missing validators: {', '.join(missing)}", failures)

    l3_case = ROOT / "examples/eap-l3-worked-example"
    if l3_case.exists():
        assessment = json.loads((l3_case / "assessment-result.json").read_text(encoding="utf-8"))
        bundle = json.loads((l3_case / "evidence-bundle.json").read_text(encoding="utf-8"))
        if assessment.get("decision", {}).get("outcome") == "conformant":
            by_control = {item["control_id"]: item for item in bundle.get("control_evidence_items", [])}
            critical = {
                "EAP-CTRL-001", "EAP-CTRL-003", "EAP-CTRL-004", "EAP-CTRL-005",
                "EAP-CTRL-006", "EAP-CTRL-007", "EAP-CTRL-014", "EAP-CTRL-015",
                "EAP-CTRL-016", "EAP-CTRL-017", "EAP-CTRL-018", "EAP-CTRL-019",
            }
            for control_id in sorted(critical):
                artifacts = by_control.get(control_id, {}).get("evidence_artifacts", [])
                if not any(a.get("artifact_type") == "test_result" and a.get("evidence_grade") in {"E4", "E5"} for a in artifacts):
                    fail(f"EAP-INV-007 conformant L3 assessment lacks E4+ executable evidence for {control_id}", failures)

    if failures:
        print(f"{len(failures)} assurance invariant(s) failed.", file=sys.stderr)
        return 1
    print("OK: all EAP v0.9 assurance invariants hold.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
