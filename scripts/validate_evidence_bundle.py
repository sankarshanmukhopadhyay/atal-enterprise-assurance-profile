#!/usr/bin/env python3
"""
validate_evidence_bundle.py — Validate an EAP evidence bundle against
the evidence-bundle.schema.json schema.

Usage:
    python scripts/validate_evidence_bundle.py evidence/samples/eap-l1-sample-evidence-bundle.json
"""

import sys
import json
import pathlib
import argparse

try:
    import jsonschema
except ImportError:
    print("ERROR: jsonschema not installed. Run: pip install jsonschema", file=sys.stderr)
    sys.exit(2)


REPO_ROOT = pathlib.Path(__file__).parent.parent
SCHEMA_PATH = REPO_ROOT / "schemas" / "evidence-bundle.schema.json"


def main():
    parser = argparse.ArgumentParser(description="Validate an EAP evidence bundle against its schema.")
    parser.add_argument("bundle", help="Path to evidence bundle JSON file")
    args = parser.parse_args()

    bundle_path = pathlib.Path(args.bundle)
    if not bundle_path.exists():
        print(f"ERROR: File not found: {bundle_path}", file=sys.stderr)
        sys.exit(2)

    if not SCHEMA_PATH.exists():
        print(f"ERROR: Schema not found: {SCHEMA_PATH}", file=sys.stderr)
        sys.exit(2)

    print(f"Loading bundle: {bundle_path}")
    bundle = json.loads(bundle_path.read_text(encoding="utf-8"))

    print(f"Loading schema: {SCHEMA_PATH}")
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))

    validator = jsonschema.Draft7Validator(schema)
    errors = sorted(validator.iter_errors(bundle), key=lambda e: list(e.path))

    if not errors:
        items = bundle.get("control_evidence_items", [])
        status_counts = {}
        for item in items:
            s = item.get("status", "unknown")
            status_counts[s] = status_counts.get(s, 0) + 1
        print(f"\n✓ Evidence bundle is valid.")
        print(f"  Bundle ID:       {bundle.get('bundle_id', 'N/A')}")
        print(f"  Assurance level: {bundle.get('assurance_level', 'N/A')}")
        print(f"  Control items:   {len(items)}")
        for status, count in sorted(status_counts.items()):
            print(f"    {status}: {count}")
        sys.exit(0)
    else:
        print(f"\n✗ Evidence bundle validation FAILED — {len(errors)} error(s):\n", file=sys.stderr)
        for i, err in enumerate(errors, 1):
            path = " > ".join(str(p) for p in err.absolute_path) or "(root)"
            print(f"  [{i}] Path: {path}", file=sys.stderr)
            print(f"       {err.message}\n", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
