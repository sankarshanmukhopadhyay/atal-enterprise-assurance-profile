#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys
import yaml
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "assurance/handoff-source-set.yaml"
OUT = ROOT / "artifacts/eap-l3-assessor-handoff.json"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def repository_version() -> str:
    status = yaml.safe_load((ROOT / "PROJECT-STATUS.yaml").read_text(encoding="utf-8"))
    return str(status["project"]["version"])


def main() -> int:
    config = yaml.safe_load(CONFIG.read_text(encoding="utf-8"))
    version = repository_version()
    claim_path = ROOT / "artifacts/eap-l3-assurance-claim.json"
    if not claim_path.exists():
        print("ERROR: build the L3 assurance claim before the handoff", file=sys.stderr)
        return 1
    claim = load_json(claim_path)
    sources = []
    for entry in config["sources"]:
        rel = entry.get("path") or entry.get("path_template", "").format(version=version)
        if not rel:
            print(f"ERROR: handoff source lacks path: {entry}", file=sys.stderr)
            return 1
        path = ROOT / rel
        if not path.exists():
            print(f"ERROR: missing handoff source {rel}", file=sys.stderr)
            return 1
        sources.append({"role": entry["role"], "path": rel, "sha256": digest(path)})
    manifest = {
        "schema_version": "1.0",
        "handoff_id": f"eap:handoff:{claim['subject']['system_id']}:{claim['subject']['deployment_id']}:{version}",
        "profile": {"id": "EAP-L3", "version": version},
        "subject": claim["subject"],
        "authorities": claim["authorities"],
        "lifecycle": {
            "assessed_at": claim["validity"]["assessed_at"],
            "expires_at": claim["validity"]["expires_at"],
            "state": claim["state"],
            "revoked_at": claim["validity"].get("revoked_at"),
            "revocation_reason": claim["validity"].get("revocation_reason")
        },
        "sources": sources
    }
    schema = load_json(ROOT / "schemas/assessor-handoff.schema.json")
    errors = list(Draft202012Validator(schema).iter_errors(manifest))
    if errors:
        print("ERROR: generated handoff is invalid: " + "; ".join(e.message for e in errors), file=sys.stderr)
        return 1
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"✓ wrote {OUT.relative_to(ROOT)} for v{version} with {len(sources)} digest-bound sources")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
