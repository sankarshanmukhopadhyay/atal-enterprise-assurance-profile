#!/usr/bin/env python3
"""
validate_repo_integrity.py — Perform repository-level semantic and cross-artifact
integrity checks beyond schema validation.

Checks include:
- unique control identifiers in the catalog
- JSON and YAML catalog equivalence
- overlay references only valid control identifiers
- mandatory controls are applicable at the selected level
- dependency rules point to valid and applicable controls
- bundle and assessment reference only valid controls
- assurance levels align across samples and overlays
- duplicate control entries are not present in samples
"""

from __future__ import annotations

import json
import pathlib
import sys
from collections import Counter

try:
    import yaml
except ImportError:
    print("ERROR: pyyaml not installed. Run: pip install -r requirements.txt", file=sys.stderr)
    sys.exit(2)

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
CATALOG_JSON_PATH = REPO_ROOT / "catalogs" / "atal-eap-control-catalog.json"
CATALOG_YAML_PATH = REPO_ROOT / "catalogs" / "atal-eap-control-catalog.yaml"
OVERLAY_DIR = REPO_ROOT / "catalogs" / "assurance-level-overlays"
BUNDLE_SAMPLE_PATH = REPO_ROOT / "evidence" / "samples" / "eap-l1-sample-evidence-bundle.json"
RESULT_SAMPLE_PATH = REPO_ROOT / "assessments" / "samples" / "eap-l1-sample-assessment.json"
VALID_LEVELS = ["EAP-L1", "EAP-L2", "EAP-L3"]


def load_json(path: pathlib.Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def load_yaml(path: pathlib.Path) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def canonicalize(value):
    if isinstance(value, dict):
        return {k: canonicalize(value[k]) for k in sorted(value.keys())}
    if isinstance(value, list):
        if all(isinstance(item, dict) for item in value):
            keyed = sorted(value, key=lambda item: json.dumps(canonicalize(item), sort_keys=True))
            return [canonicalize(item) for item in keyed]
        return [canonicalize(item) for item in value]
    return value


def fail(message: str, failures: list[str]):
    failures.append(message)


def main() -> int:
    failures: list[str] = []

    catalog_json = load_json(CATALOG_JSON_PATH)
    catalog_yaml = load_yaml(CATALOG_YAML_PATH)

    if canonicalize(catalog_json) != canonicalize(catalog_yaml):
        fail("Catalog JSON and YAML are not semantically equivalent.", failures)

    controls = catalog_json.get("controls", [])
    control_ids = [control.get("id") for control in controls]
    duplicate_control_ids = sorted(control_id for control_id, count in Counter(control_ids).items() if count > 1)
    if duplicate_control_ids:
        fail(f"Duplicate control IDs in catalog: {', '.join(duplicate_control_ids)}", failures)

    control_index = {control["id"]: control for control in controls}
    valid_control_ids = set(control_index.keys())

    for level in VALID_LEVELS:
        overlay_path = OVERLAY_DIR / f"{level}-overlay.json"
        overlay = load_json(overlay_path)

        if overlay.get("assurance_level") != level:
            fail(f"Overlay {overlay_path.name} declares assurance_level={overlay.get('assurance_level')} instead of {level}.", failures)

        if overlay.get("version") != catalog_json.get("version"):
            fail(f"Overlay {overlay_path.name} version {overlay.get('version')} does not match catalog version {catalog_json.get('version')}.", failures)

        applicable_controls = overlay.get("applicable_controls", [])
        overlay_ids = [item.get("control_id") for item in applicable_controls]
        duplicate_overlay_ids = sorted(control_id for control_id, count in Counter(overlay_ids).items() if count > 1)
        if duplicate_overlay_ids:
            fail(f"Overlay {overlay_path.name} contains duplicate control IDs: {', '.join(duplicate_overlay_ids)}", failures)

        applicable_true_ids = set()
        for item in applicable_controls:
            control_id = item.get("control_id")
            if control_id not in valid_control_ids:
                fail(f"Overlay {overlay_path.name} references unknown control ID {control_id}.", failures)
                continue
            if item.get("applicable"):
                applicable_true_ids.add(control_id)

            for dep_id in item.get("dependency_rules", []):
                if dep_id not in valid_control_ids:
                    fail(f"Overlay {overlay_path.name} dependency rule {dep_id} for {control_id} is not a valid control ID.", failures)
                else:
                    dep_entry = next((entry for entry in applicable_controls if entry.get("control_id") == dep_id), None)
                    if dep_entry is None or not dep_entry.get("applicable"):
                        fail(f"Overlay {overlay_path.name} dependency rule {dep_id} for {control_id} is not applicable at {level}.", failures)

        for mandatory_id in overlay.get("mandatory_control_ids", []):
            if mandatory_id not in valid_control_ids:
                fail(f"Overlay {overlay_path.name} mandatory control {mandatory_id} is not defined in the catalog.", failures)
            elif mandatory_id not in applicable_true_ids:
                fail(f"Overlay {overlay_path.name} mandatory control {mandatory_id} is not marked applicable.", failures)

    bundle = load_json(BUNDLE_SAMPLE_PATH)
    result = load_json(RESULT_SAMPLE_PATH)

    if bundle.get("assurance_level") != "EAP-L1":
        fail("Sample evidence bundle assurance_level must be EAP-L1.", failures)
    if result.get("assurance_level") != "EAP-L1":
        fail("Sample assessment result assurance_level must be EAP-L1.", failures)

    bundle_control_ids = [item.get("control_id") for item in bundle.get("control_evidence_items", [])]
    duplicate_bundle_ids = sorted(control_id for control_id, count in Counter(bundle_control_ids).items() if count > 1)
    if duplicate_bundle_ids:
        fail(f"Sample evidence bundle contains duplicate control IDs: {', '.join(duplicate_bundle_ids)}", failures)

    result_control_ids = [item.get("control_id") for item in result.get("control_results", [])]
    duplicate_result_ids = sorted(control_id for control_id, count in Counter(result_control_ids).items() if count > 1)
    if duplicate_result_ids:
        fail(f"Sample assessment result contains duplicate control IDs: {', '.join(duplicate_result_ids)}", failures)

    unknown_bundle_ids = sorted(set(bundle_control_ids) - valid_control_ids)
    if unknown_bundle_ids:
        fail(f"Sample evidence bundle references unknown control IDs: {', '.join(unknown_bundle_ids)}", failures)

    unknown_result_ids = sorted(set(result_control_ids) - valid_control_ids)
    if unknown_result_ids:
        fail(f"Sample assessment result references unknown control IDs: {', '.join(unknown_result_ids)}", failures)

    l1_overlay = load_json(OVERLAY_DIR / "EAP-L1-overlay.json")
    l1_mandatory = set(l1_overlay.get("mandatory_control_ids", []))
    bundle_ids = set(bundle_control_ids)
    result_ids = set(result_control_ids)

    missing_mandatory_in_bundle = sorted(l1_mandatory - bundle_ids)
    if missing_mandatory_in_bundle:
        fail(f"Sample evidence bundle is missing mandatory EAP-L1 controls: {', '.join(missing_mandatory_in_bundle)}", failures)

    missing_mandatory_in_result = sorted(l1_mandatory - result_ids)
    if missing_mandatory_in_result:
        fail(f"Sample assessment result is missing mandatory EAP-L1 controls: {', '.join(missing_mandatory_in_result)}", failures)

    if bundle_ids != result_ids:
        only_bundle = sorted(bundle_ids - result_ids)
        only_result = sorted(result_ids - bundle_ids)
        detail_parts = []
        if only_bundle:
            detail_parts.append(f"only in bundle: {', '.join(only_bundle)}")
        if only_result:
            detail_parts.append(f"only in result: {', '.join(only_result)}")
        fail("Sample evidence bundle and assessment result cover different control sets (" + "; ".join(detail_parts) + ").", failures)

    if failures:
        print("✗ Repository integrity validation FAILED:\n", file=sys.stderr)
        for index, message in enumerate(failures, start=1):
            print(f"  [{index}] {message}", file=sys.stderr)
        return 1

    print("✓ Repository integrity validation passed.")
    print(f"  Catalog version: {catalog_json.get('version', 'N/A')}")
    print(f"  Catalog controls: {len(controls)}")
    print(f"  Checked overlays: {len(VALID_LEVELS)}")
    print(f"  Sample controls: {len(bundle_control_ids)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
