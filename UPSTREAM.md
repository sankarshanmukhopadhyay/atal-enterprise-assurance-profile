# Upstream tracking: ATAL Standard

This repository profiles and extends the upstream ATAL Standard.

- Upstream repository: https://github.com/Elytra-Security/atal-standard
- Machine-readable baseline: `upstream/atal-baseline.yaml`

## Version pinning

Each EAP release MUST identify the ATAL specification version, exact upstream commit, and compatibility class used as its normative baseline.

| EAP release | ATAL version | ATAL commit | Compatibility class | Notes |
|---|---|---|---|---|
| v0.4.0 | Public Review Draft v0.9 | `bafb65d716ddf71d2a90defbd4bfb5064c6aee0e` | Extended Compatible | First machine-enforced provenance baseline; profiles `docs/ATAL_Specification_v0.9.md`. |

## Sync policy

- Prefer released ATAL tags where available; otherwise pin an exact upstream commit and record the normative document version.
- For each upstream update, capture:
  - what changed upstream;
  - which EAP controls, mappings, tests, or claims are impacted;
  - whether the compatibility class changes;
  - whether existing assurance claims require re-assessment.
- `python scripts/check_upstream_integrity.py` MUST pass before release.
- A changed upstream normative baseline makes prior mappings stale until explicitly reviewed.

## Authority boundary

ATAL retains authority over upstream specification semantics. EAP owns only the enterprise assurance profile, mappings, tests, evidence contracts, and EAP claim semantics. EAP conformance does not imply ATAL certification, regulatory approval, or enterprise risk acceptance.
