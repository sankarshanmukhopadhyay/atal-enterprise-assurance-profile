#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
CASE = ROOT / "examples" / "eap-l2-worked-example"
OUT = ROOT / "artifacts" / "eap-l2-assurance-claim.json"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    profile = load(CASE / "deployment-profile.json")
    assessment = load(CASE / "assessment-result.json")
    results = assessment["control_results"]
    required = [r for r in results if r["control_id"] not in {"EAP-CTRL-009", "EAP-CTRL-013", "EAP-CTRL-019"}]
    counts = {
        "required": len([r for r in required if r["control_id"] != "EAP-CTRL-006"]),
        "passed": len([r for r in required if r["control_id"] != "EAP-CTRL-006" and r["result"] == "pass"]),
        "waived": len([r for r in required if r["control_id"] != "EAP-CTRL-006" and r["result"] == "waived"]),
        "failed": len([r for r in required if r["control_id"] != "EAP-CTRL-006" and r["result"] == "fail"]),
        "partial": len([r for r in required if r["control_id"] != "EAP-CTRL-006" and r["result"] == "partial"]),
    }
    state = "CONFORMANT" if counts["failed"] == 0 and counts["partial"] == 0 and counts["waived"] == 0 else "CONFORMANT-WITH-EXCEPTIONS"
    claim = {
        "schema_version": "1.0",
        "claim_id": "eap:claim:sample-purchasing-agent:prod-apac-01:2026-08-22",
        "subject": {
            "system_id": profile["system"]["system_id"],
            "deployment_id": profile["system"]["deployment_id"],
        },
        "profile": {"id": "EAP-L2", "version": "0.9.1"},
        "state": state,
        "control_summary": counts,
        "evidence_bundle": {
            "path": "examples/eap-l2-worked-example/evidence-bundle.json",
            "sha256": digest(CASE / "evidence-bundle.json"),
        },
        "assessment": {
            "path": "examples/eap-l2-worked-example/assessment-result.json",
            "sha256": digest(CASE / "assessment-result.json"),
        },
        "validity": {
            "assessed_at": "2026-08-22T15:10:00Z",
            "expires_at": "2026-11-20T23:59:59Z",
            "revoked_at": None,
            "revocation_reason": None,
        },
        "authorities": {
            "profile_authority": "ATAL Enterprise Assurance Profile maintainers",
            "system_authority": profile["authorities"]["system_authority"],
            "assessment_authority": profile["authorities"]["assessment_authority"],
            "risk_acceptance_authority": profile["authorities"]["risk_acceptance_authority"],
        },
    }
    schema = load(ROOT / "schemas/assurance-claim.schema.json")
    errors = list(Draft202012Validator(schema).iter_errors(claim))
    if errors:
        raise SystemExit("claim schema validation failed: " + "; ".join(e.message for e in errors))
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(claim, indent=2) + "\n", encoding="utf-8")
    print(f"✓ wrote {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
