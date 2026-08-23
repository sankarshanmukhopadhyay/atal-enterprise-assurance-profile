# v1.0 Readiness Evidence

## Purpose

The repository does not infer v1.0 readiness from a green CI run. v0.9.4 introduces an explicit readiness model that separates tested repository properties from the later governance decision to publish v1.0.

## Candidate-stable surface

`assurance/stable-contracts.yaml` declares the schema and identifier surface intended to remain compatible through the remainder of the 0.9.x line. `scripts/check_contract_compatibility.py` fails if declared schemas disappear, canonical identifier forms stop matching, or required claim/test-result states are removed.

## Conformance corpus

`tests/fixtures/conformance/manifest.yaml` contains positive and negative fixtures for assurance claims, executable test results, and assessor handoffs. `scripts/validate_conformance_corpus.py` requires both acceptance and rejection behavior to match the fixture declaration.

## Readiness report

`assurance/v1-readiness-criteria.yaml` defines blocking criteria. `scripts/build_v1_readiness_report.py` evaluates those criteria and emits:

- `artifacts/v1-readiness-report.json`
- `artifacts/v1-readiness-report.md`

A failed blocking criterion prevents the report from claiming `ready_for_v1_decision`.

For v0.9.4, the expected result is `not_ready` because the final governance and compatibility freeze is intentionally deferred to v0.9.5. This is an expected, machine-visible blocker rather than a CI failure.

## Authority boundary

`ready_for_v1_decision` means the repository has produced the evidence required to enter the explicit v1.0 governance decision gate. It does not automatically publish v1.0 and does not certify any deployment, establish legal compliance, grant regulator approval, or accept enterprise risk.
