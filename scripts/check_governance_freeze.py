#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import sys
import yaml

ROOT = Path(__file__).resolve().parents[1]
FREEZE = ROOT / "assurance/governance-freeze.yaml"


def main() -> int:
    failures: list[str] = []
    if not FREEZE.exists():
        print("ERROR: governance freeze is missing", file=sys.stderr)
        return 1
    freeze = yaml.safe_load(FREEZE.read_text(encoding="utf-8"))
    status = yaml.safe_load((ROOT / "PROJECT-STATUS.yaml").read_text(encoding="utf-8"))
    version = str(status["project"]["version"])
    if freeze.get("profile_version") != version:
        failures.append(f"freeze version {freeze.get('profile_version')} != repository version {version}")
    if freeze.get("status") != "frozen-for-v1-decision":
        failures.append("freeze status must be frozen-for-v1-decision")

    required_surfaces = {"release_governance", "authority_model", "compatibility_surface", "assurance_lifecycle"}
    surfaces = freeze.get("frozen_surfaces", {})
    missing_surfaces = sorted(required_surfaces - set(surfaces))
    if missing_surfaces:
        failures.append("missing frozen surfaces: " + ", ".join(missing_surfaces))
    for name, surface in surfaces.items():
        evidence = surface.get("evidence", [])
        if not evidence:
            failures.append(f"{name} has no freeze evidence")
        for rel in evidence:
            if not (ROOT / rel).exists():
                failures.append(f"{name} references missing evidence: {rel}")
        if not surface.get("rule"):
            failures.append(f"{name} has no frozen rule")

    disposition = freeze.get("blocker_disposition", {}).get("V1-RDY-008", {})
    if disposition.get("status") != "resolved" or disposition.get("evidence") != "assurance/governance-freeze.yaml":
        failures.append("V1-RDY-008 is not explicitly resolved by the freeze")

    decision = freeze.get("v1_decision", {})
    if decision.get("issue") != 12 or decision.get("required") is not True:
        failures.append("v1 decision must remain explicitly bound to issue #12")
    if decision.get("automatic_promotion") is not False:
        failures.append("automatic v1 promotion must be prohibited")

    stable = yaml.safe_load((ROOT / "assurance/stable-contracts.yaml").read_text(encoding="utf-8"))
    if str(stable.get("profile_version")) != version:
        failures.append("candidate-stable contract declaration version does not match repository version")

    workflow = (ROOT / ".github/workflows/publish-release.yml").read_text(encoding="utf-8")
    required_release_safeguards = [
        "Refuse to move an existing tag",
        "git tag -a",
        "refusing to move it",
        "leaving tag immutable",
    ]
    missing_safeguards = [text for text in required_release_safeguards if text not in workflow]
    if missing_safeguards:
        failures.append("release workflow lost immutable-tag safeguards: " + ", ".join(missing_safeguards))

    if failures:
        print("✗ governance freeze validation FAILED", file=sys.stderr)
        for failure in failures:
            print(f"  - {failure}", file=sys.stderr)
        return 1
    print(f"✓ governance freeze valid for v{version}; v1 promotion remains explicit via issue #12")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
