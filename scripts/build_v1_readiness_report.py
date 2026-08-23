#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import yaml

ROOT = Path(__file__).resolve().parents[1]
CRITERIA = ROOT / "assurance/v1-readiness-criteria.yaml"
OUT_JSON = ROOT / "artifacts/v1-readiness-report.json"
OUT_MD = ROOT / "artifacts/v1-readiness-report.md"


def exists(path: str) -> bool:
    return (ROOT / path).exists()


def load_json(path: str):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def command_ok(args: list[str]) -> bool:
    return subprocess.run([sys.executable, *args], cwd=ROOT, capture_output=True, text=True).returncode == 0


def evaluate(criteria_id: str) -> tuple[bool, str]:
    if criteria_id == "V1-RDY-001":
        ok = command_ok(["scripts/release_governance.py", "validate-current"])
        return ok, "release governance validates current version" if ok else "release governance failed"
    if criteria_id == "V1-RDY-002":
        baseline = yaml.safe_load((ROOT / "upstream/atal-baseline.yaml").read_text(encoding="utf-8"))
        commit = baseline.get("upstream", {}).get("commit", "")
        compat = baseline.get("upstream", {}).get("compatibility_class")
        ok = len(commit) == 40 and bool(compat)
        return ok, f"upstream commit={commit or 'missing'} compatibility={compat or 'missing'}"
    if criteria_id == "V1-RDY-003":
        required = [
            "evidence/samples/eap-l1-sample-evidence-bundle.json",
            "examples/eap-l2-worked-example/evidence-bundle.json",
            "examples/eap-l3-worked-example/evidence-bundle.json",
            "scripts/validate_l2_worked_example.py",
            "scripts/validate_l3_worked_example.py",
        ]
        ok = all(exists(p) for p in required)
        return ok, "L1/L2/L3 reference assurance paths present" if ok else "one or more assurance paths missing"
    if criteria_id == "V1-RDY-004":
        neg = ROOT / "examples/eap-l3-worked-example/negative-fixtures"
        ok = neg.exists() and len(list(neg.glob("*.json"))) >= 2
        return ok, f"adversarial negative fixtures={len(list(neg.glob('*.json'))) if neg.exists() else 0}"
    if criteria_id == "V1-RDY-005":
        clean_path = "artifacts/eap-l3-handoff-verification.json"
        tamper_path = "artifacts/eap-l3-handoff-tamper-verification.json"
        if not exists(clean_path) or not exists(tamper_path):
            return False, "handoff verification reports missing"
        clean = load_json(clean_path)
        tamper = load_json(tamper_path)
        ok = clean.get("result") == "verified" and tamper.get("result") == "rejected" and any(f.get("code") == "digest-mismatch" for f in tamper.get("findings", []))
        return ok, "clean handoff verified; tampered handoff rejected" if ok else "handoff reproducibility evidence incomplete"
    if criteria_id == "V1-RDY-006":
        ok = command_ok(["scripts/check_contract_compatibility.py"])
        return ok, "candidate-stable compatibility checks pass" if ok else "candidate-stable compatibility check failed"
    if criteria_id == "V1-RDY-007":
        ok = command_ok(["scripts/validate_conformance_corpus.py"])
        return ok, "positive and negative conformance corpus passes" if ok else "conformance corpus failed"
    if criteria_id == "V1-RDY-008":
        ok = exists("assurance/governance-freeze.yaml")
        return ok, "governance freeze present" if ok else "governance freeze pending v0.9.5"
    return False, "unknown readiness criterion"


def main() -> int:
    model = yaml.safe_load(CRITERIA.read_text(encoding="utf-8"))
    results = []
    blockers = []
    for criterion in model["criteria"]:
        passed, detail = evaluate(criterion["id"])
        result = {
            "id": criterion["id"],
            "description": criterion["description"],
            "blocking": bool(criterion.get("blocking")),
            "passed": passed,
            "detail": detail,
        }
        if not passed and result["blocking"]:
            blockers.append({"id": result["id"], "detail": detail, "expected_in": criterion.get("expected_in")})
        results.append(result)
    status = "ready_for_v1_decision" if not blockers else "not_ready"
    report = {
        "schema_version": "1.0",
        "profile_version": str(model["profile_version"]),
        "status": status,
        "criteria": results,
        "blockers": blockers,
        "assurance_boundary": "Readiness is repository/profile readiness for an explicit v1.0 decision; it is not deployment certification, legal compliance, regulator approval, or risk acceptance."
    }
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    lines = ["# v1.0 Readiness Report", "", f"**Profile:** {report['profile_version']}", f"**Status:** `{status}`", "", "## Criteria", "", "| ID | Passed | Blocking | Evidence |", "|---|---:|---:|---|"]
    for item in results:
        lines.append(f"| {item['id']} | {'yes' if item['passed'] else 'no'} | {'yes' if item['blocking'] else 'no'} | {item['detail']} |")
    lines += ["", "## Blocking findings", ""]
    if blockers:
        lines += [f"- **{b['id']}** — {b['detail']}" + (f" (expected in {b['expected_in']})" if b.get("expected_in") else "") for b in blockers]
    else:
        lines.append("None. The repository is ready for the separate explicit v1.0 decision gate.")
    lines += ["", "## Assurance boundary", "", report["assurance_boundary"], ""]
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")
    print(f"✓ wrote readiness report: {status} ({len(blockers)} blocker(s))")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
