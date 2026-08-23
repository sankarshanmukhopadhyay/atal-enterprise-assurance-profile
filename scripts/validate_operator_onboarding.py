#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_PATHS = [
    "docs/getting-started.md",
    "examples/eap-l2-worked-example/README.md",
    "examples/eap-l2-worked-example/deployment-profile.json",
    "examples/eap-l2-worked-example/evidence-bundle.json",
    "examples/eap-l2-worked-example/assessment-result.json",
    "examples/eap-l2-worked-example/test-results/EAP-TEST-NB-001.json",
    "examples/eap-l2-worked-example/test-results/EAP-TEST-KS-001.json",
    "examples/eap-l3-worked-example/README.md",
    "examples/eap-l3-worked-example/deployment-profile.json",
    "scripts/derive_assurance_level.py",
    "scripts/generate_profile_checklist.py",
    "scripts/check_required_controls.py",
    "scripts/validate_l2_worked_example.py",
    "scripts/validate_l3_worked_example.py",
    "scripts/build_l2_assurance_claim.py",
    "scripts/build_l3_assurance_claim.py",
    "scripts/build_assessor_handoff.py",
    "scripts/verify_assessor_handoff.py",
]

REQUIRED_GETTING_STARTED_TEXT = [
    "examples/eap-l2-worked-example/deployment-profile.json",
    "first file to read",
    "derive_assurance_level.py",
    "generate_profile_checklist.py",
    "validate_l2_worked_example.py",
    "build_l2_assurance_claim.py",
    "Break it deliberately",
    "examples/eap-l3-worked-example/README.md",
]

REQUIRED_README_TEXT = [
    "Start Here",
    "examples/eap-l2-worked-example/deployment-profile.json",
    "docs/getting-started.md",
]


def main() -> int:
    failures: list[str] = []

    for rel in REQUIRED_PATHS:
        if not (ROOT / rel).exists():
            failures.append(f"missing onboarding path: {rel}")

    getting_started = (ROOT / "docs/getting-started.md").read_text(encoding="utf-8") if (ROOT / "docs/getting-started.md").exists() else ""
    for text in REQUIRED_GETTING_STARTED_TEXT:
        if text.lower() not in getting_started.lower():
            failures.append(f"getting-started guide missing required anchor: {text}")

    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    for text in REQUIRED_README_TEXT:
        if text.lower() not in readme.lower():
            failures.append(f"README missing first-use anchor: {text}")

    if failures:
        print("✗ operator onboarding validation FAILED", file=sys.stderr)
        for failure in failures:
            print(f"  - {failure}", file=sys.stderr)
        return 1

    print(f"✓ operator onboarding golden path valid ({len(REQUIRED_PATHS)} required paths)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
