#!/usr/bin/env python3
"""
validate_catalog.py — Validate an EAP control catalog (JSON or YAML) against
the control-catalog.schema.json schema.

Usage:
    python scripts/validate_catalog.py catalogs/atal-eap-control-catalog.json
    python scripts/validate_catalog.py catalogs/atal-eap-control-catalog.yaml
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

try:
    import yaml
except ImportError:
    yaml = None


REPO_ROOT = pathlib.Path(__file__).parent.parent
SCHEMA_PATH = REPO_ROOT / "schemas" / "control-catalog.schema.json"


def load_file(path: pathlib.Path) -> dict:
    suffix = path.suffix.lower()
    text = path.read_text(encoding="utf-8")
    if suffix in (".yaml", ".yml"):
        if yaml is None:
            print("ERROR: pyyaml not installed. Run: pip install pyyaml", file=sys.stderr)
            sys.exit(2)
        return yaml.safe_load(text)
    else:
        return json.loads(text)


def main():
    parser = argparse.ArgumentParser(description="Validate an EAP control catalog against its schema.")
    parser.add_argument("catalog", help="Path to catalog JSON or YAML file")
    args = parser.parse_args()

    catalog_path = pathlib.Path(args.catalog)
    if not catalog_path.exists():
        print(f"ERROR: File not found: {catalog_path}", file=sys.stderr)
        sys.exit(2)

    if not SCHEMA_PATH.exists():
        print(f"ERROR: Schema not found: {SCHEMA_PATH}", file=sys.stderr)
        sys.exit(2)

    print(f"Loading catalog:  {catalog_path}")
    catalog = load_file(catalog_path)

    print(f"Loading schema:   {SCHEMA_PATH}")
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))

    validator = jsonschema.Draft7Validator(schema)
    errors = sorted(validator.iter_errors(catalog), key=lambda e: list(e.path))

    if not errors:
        ctrl_count = len(catalog.get("controls", []))
        print(f"\n✓ Catalog is valid.")
        print(f"  Version:  {catalog.get('version', 'N/A')}")
        print(f"  Controls: {ctrl_count}")
        sys.exit(0)
    else:
        print(f"\n✗ Catalog validation FAILED — {len(errors)} error(s):\n", file=sys.stderr)
        for i, err in enumerate(errors, 1):
            path = " > ".join(str(p) for p in err.absolute_path) or "(root)"
            print(f"  [{i}] Path: {path}", file=sys.stderr)
            print(f"       {err.message}\n", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
