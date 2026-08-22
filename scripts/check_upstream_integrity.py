#!/usr/bin/env python3
"""Validate the EAP upstream provenance declaration.

Fails closed when the pinned ATAL baseline is incomplete or contains placeholders.
This is intentionally repository-local and deterministic; network freshness checks are
separate because release validation must remain reproducible offline.
"""
from __future__ import annotations

import json
from pathlib import Path
import re
import sys

import yaml

ROOT = Path(__file__).resolve().parents[1]
BASELINE = ROOT / "upstream" / "atal-baseline.yaml"
SCHEMA = ROOT / "schemas" / "upstream-baseline.schema.json"

try:
    from jsonschema import Draft202012Validator
except ImportError as exc:
    raise SystemExit("jsonschema is required; install requirements.txt") from exc


def main() -> int:
    baseline = yaml.safe_load(BASELINE.read_text(encoding="utf-8"))
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    errors = sorted(Draft202012Validator(schema).iter_errors(baseline), key=lambda e: list(e.path))
    if errors:
        for error in errors:
            where = ".".join(str(p) for p in error.path) or "<root>"
            print(f"ERROR {where}: {error.message}")
        return 1

    serialized = json.dumps(baseline).lower()
    if "tbd" in serialized or "todo" in serialized:
        print("ERROR: upstream baseline contains unresolved placeholder text")
        return 1

    commit = baseline["upstream"]["commit"]
    if not re.fullmatch(r"[0-9a-f]{40}", commit):
        print("ERROR: upstream commit must be a full 40-character SHA")
        return 1

    print(
        "OK: EAP {eap} pins {repo} {version} at {commit} ({compat})".format(
            eap=baseline["eap_version"],
            repo=baseline["upstream"]["repository"],
            version=baseline["upstream"]["specification_version"],
            commit=commit,
            compat=baseline["upstream"]["compatibility_class"],
        )
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
