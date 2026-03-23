#!/usr/bin/env python3
"""
run_quality_gate.py — Canonical entrypoint for repository validation and
artifact generation.

Modes:
- validate: schema + semantic checks only
- build: regenerate generated artifacts only
- all: validate first, then regenerate artifacts
"""

from __future__ import annotations

import argparse
import pathlib
import subprocess
import sys

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
PYTHON = sys.executable

VALIDATION_COMMANDS = [
    [PYTHON, "scripts/validate_catalog.py", "catalogs/atal-eap-control-catalog.json"],
    [PYTHON, "scripts/validate_catalog.py", "catalogs/atal-eap-control-catalog.yaml"],
    [PYTHON, "scripts/validate_repo_integrity.py"],
    [PYTHON, "scripts/validate_evidence_bundle.py", "evidence/samples/eap-l1-sample-evidence-bundle.json"],
    [PYTHON, "scripts/validate_assessment_result.py", "assessments/samples/eap-l1-sample-assessment.json"],
    [PYTHON, "scripts/check_required_controls.py", "--level", "EAP-L1", "--bundle", "evidence/samples/eap-l1-sample-evidence-bundle.json"],
    [PYTHON, "scripts/check_required_controls.py", "--level", "EAP-L1", "--result", "assessments/samples/eap-l1-sample-assessment.json"],
]

BUILD_COMMANDS = [
    [PYTHON, "scripts/generate_profile_checklist.py", "--level", "EAP-L1"],
    [PYTHON, "scripts/generate_profile_checklist.py", "--level", "EAP-L2"],
    [PYTHON, "scripts/generate_profile_checklist.py", "--level", "EAP-L3"],
    [PYTHON, "scripts/build_traceability_matrix.py"],
    [PYTHON, "scripts/compile_assessment_report.py", "--level", "EAP-L1", "--bundle", "evidence/samples/eap-l1-sample-evidence-bundle.json", "--result", "assessments/samples/eap-l1-sample-assessment.json"],
    [PYTHON, "scripts/export_csv_xlsx.py", "--source", "catalog"],
    [PYTHON, "scripts/export_csv_xlsx.py", "--source", "assessment", "--result", "assessments/samples/eap-l1-sample-assessment.json"],
]


def run_commands(commands: list[list[str]], stage_name: str) -> int:
    print(f"== {stage_name} ==")
    for command in commands:
        printable = " ".join(command)
        print(f"\n$ {printable}")
        completed = subprocess.run(command, cwd=REPO_ROOT)
        if completed.returncode != 0:
            print(f"\n✗ Stage failed while running: {printable}", file=sys.stderr)
            return completed.returncode
    print(f"\n✓ {stage_name} completed.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the repository quality gate.")
    parser.add_argument("--mode", default="all", choices=["validate", "build", "all"])
    args = parser.parse_args()

    if args.mode in ("validate", "all"):
        code = run_commands(VALIDATION_COMMANDS, "Validation")
        if code != 0:
            return code

    if args.mode in ("build", "all"):
        code = run_commands(BUILD_COMMANDS, "Artifact generation")
        if code != 0:
            return code

    print("\nQuality gate completed successfully.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
