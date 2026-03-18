#!/usr/bin/env python3
"""
validate_assessment_result.py — Validate an EAP assessment result against
the assessment-result.schema.json schema.

Usage:
    python scripts/validate_assessment_result.py assessments/samples/eap-l1-sample-assessment.json
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
SCHEMA_PATH = REPO_ROOT / "schemas" / "assessment-result.schema.json"


def main():
    parser = argparse.ArgumentParser(description="Validate an EAP assessment result against its schema.")
    parser.add_argument("result", help="Path to assessment result JSON file")
    args = parser.parse_args()

    result_path = pathlib.Path(args.result)
    if not result_path.exists():
        print(f"ERROR: File not found: {result_path}", file=sys.stderr)
        sys.exit(2)

    if not SCHEMA_PATH.exists():
        print(f"ERROR: Schema not found: {SCHEMA_PATH}", file=sys.stderr)
        sys.exit(2)

    print(f"Loading result: {result_path}")
    result = json.loads(result_path.read_text(encoding="utf-8"))

    print(f"Loading schema: {SCHEMA_PATH}")
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))

    validator = jsonschema.Draft7Validator(schema)
    errors = sorted(validator.iter_errors(result), key=lambda e: list(e.path))

    if not errors:
        ctrl_results = result.get("control_results", [])
        outcome = result.get("decision", {}).get("outcome", "N/A")
        findings_count = len(result.get("findings", []))
        print(f"\n✓ Assessment result is valid.")
        print(f"  Assessment ID:   {result.get('assessment_id', 'N/A')}")
        print(f"  Assurance level: {result.get('assurance_level', 'N/A')}")
        print(f"  Decision:        {outcome}")
        print(f"  Controls:        {len(ctrl_results)}")
        print(f"  Findings:        {findings_count}")
        sys.exit(0)
    else:
        print(f"\n✗ Assessment result validation FAILED — {len(errors)} error(s):\n", file=sys.stderr)
        for i, err in enumerate(errors, 1):
            path = " > ".join(str(p) for p in err.absolute_path) or "(root)"
            print(f"  [{i}] Path: {path}", file=sys.stderr)
            print(f"       {err.message}\n", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
