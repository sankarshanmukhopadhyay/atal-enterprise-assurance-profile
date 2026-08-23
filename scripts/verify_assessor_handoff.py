#!/usr/bin/env python3
from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path
import sys
from datetime import datetime, timezone
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MANIFEST = ROOT / "artifacts/eap-l3-assessor-handoff.json"
REPORT = ROOT / "artifacts/eap-l3-handoff-verification.json"
TAMPER_REPORT = ROOT / "artifacts/eap-l3-handoff-tamper-verification.json"
FIXTURE = ROOT / "tests/fixtures/handoff/tampered-digest.json"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify(manifest: dict, now: datetime | None = None) -> tuple[bool, list[dict]]:
    findings: list[dict] = []
    schema = load(ROOT / "schemas/assessor-handoff.schema.json")
    for error in Draft202012Validator(schema).iter_errors(manifest):
        findings.append({"code": "schema-invalid", "message": error.message})
    if findings:
        return False, findings

    required_roles = {"deployment-profile", "evidence-bundle", "assessment", "upstream-baseline", "release-record", "assurance-claim"}
    present_roles = {x["role"] for x in manifest["sources"]}
    missing = sorted(required_roles - present_roles)
    if missing:
        findings.append({"code": "missing-role", "message": ", ".join(missing)})

    for source in manifest["sources"]:
        path = ROOT / source["path"]
        if not path.exists():
            findings.append({"code": "missing-source", "path": source["path"]})
            continue
        actual = sha256(path)
        if actual != source["sha256"]:
            findings.append({"code": "digest-mismatch", "path": source["path"], "expected": source["sha256"], "actual": actual})

    claim_sources = [x for x in manifest["sources"] if x["role"] == "assurance-claim"]
    if len(claim_sources) != 1:
        findings.append({"code": "claim-cardinality", "message": "exactly one assurance claim is required"})
    else:
        claim = load(ROOT / claim_sources[0]["path"])
        if claim.get("subject") != manifest.get("subject"):
            findings.append({"code": "subject-mismatch"})
        if claim.get("authorities") != manifest.get("authorities"):
            findings.append({"code": "authority-mismatch"})
        if claim.get("state") != manifest.get("lifecycle", {}).get("state"):
            findings.append({"code": "state-mismatch"})
        validity = claim.get("validity", {})
        if validity.get("expires_at") != manifest["lifecycle"]["expires_at"]:
            findings.append({"code": "expiry-mismatch"})
        if validity.get("revoked_at") != manifest["lifecycle"].get("revoked_at"):
            findings.append({"code": "revocation-mismatch"})

    now = now or datetime.now(timezone.utc)
    expires = datetime.fromisoformat(manifest["lifecycle"]["expires_at"].replace("Z", "+00:00"))
    state = manifest["lifecycle"]["state"]
    if state == "REVOKED" or manifest["lifecycle"].get("revoked_at"):
        findings.append({"code": "revoked-claim"})
    if now > expires and state not in {"EXPIRED", "REVOKED"}:
        findings.append({"code": "stale-claim", "message": "claim validity window has elapsed"})

    return not findings, findings


def write_report(path: Path, manifest: dict, ok: bool, findings: list[dict], mode: str) -> None:
    report = {
        "schema_version": "1.0",
        "handoff_id": manifest.get("handoff_id"),
        "mode": mode,
        "result": "verified" if ok else "rejected",
        "findings": findings,
        "verified_source_count": len(manifest.get("sources", [])) if ok else 0
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", default=str(DEFAULT_MANIFEST.relative_to(ROOT)))
    parser.add_argument("--tamper-self-test", action="store_true")
    args = parser.parse_args()
    manifest_path = ROOT / args.manifest
    if not manifest_path.exists():
        print(f"ERROR: handoff manifest not found: {args.manifest}", file=sys.stderr)
        return 1
    manifest = load(manifest_path)
    ok, findings = verify(manifest)
    write_report(REPORT, manifest, ok, findings, "independent-verification")
    if not ok:
        print("✗ assessor handoff rejected", file=sys.stderr)
        for f in findings:
            print(f"  - {f}", file=sys.stderr)
        return 1
    print(f"✓ assessor handoff verified ({len(manifest['sources'])} sources)")

    if args.tamper_self_test:
        fixture = load(FIXTURE)
        tampered = copy.deepcopy(manifest)
        target_role = fixture["mutation"]["source_role"]
        candidates = [x for x in tampered["sources"] if x["role"] == target_role]
        if not candidates:
            print(f"ERROR: fixture target role absent: {target_role}", file=sys.stderr)
            return 1
        candidates[0]["sha256"] = fixture["mutation"]["replacement_sha256"]
        tamper_ok, tamper_findings = verify(tampered)
        write_report(TAMPER_REPORT, tampered, tamper_ok, tamper_findings, "tamper-self-test")
        codes = {f.get("code") for f in tamper_findings}
        if tamper_ok or fixture["expected_reason"] not in codes:
            print("ERROR: tampered handoff was not rejected for expected reason", file=sys.stderr)
            return 1
        print("✓ tampered handoff rejected for digest mismatch")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
