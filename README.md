# ATAL Enterprise Assurance Profile (EAP)

[![Upstream: ATAL Standard](https://img.shields.io/badge/upstream-ATAL%20Standard-2ea44f)](https://github.com/Elytra-Security/atal-standard)
[![Version](https://img.shields.io/badge/version-0.9.2-blue.svg)](./changelog/CHANGELOG.md)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](./LICENSE.md)
[![Status](https://img.shields.io/badge/status-assurance%20candidate-orange.svg)](./releases/v0.9.2.md)

## What this is

The **ATAL Enterprise Assurance Profile (EAP)** operationalizes the upstream ATAL Standard for enterprise deployments. It is an executable assurance layer: controls, deployment profiles, evidence contracts, conformance tests, assessments, bounded assurance claims, interoperability mappings, and repository-level invariants are represented as machine-verifiable artifacts.

EAP does **not** replace ATAL, certify implementations, grant regulatory approval, or accept enterprise risk. ATAL retains authority over upstream specification semantics; EAP owns only its profile, mappings, tests, evidence contracts, and claim semantics.

## Assurance levels

| Level | Name | Intended use | Default evidence floor |
|---|---|---|---|
| **EAP-L1** | Enterprise Baseline | Internal copilots, lower-impact audit-required workflows | E1 — documentary |
| **EAP-L2** | Controlled Autonomy | Tool-using agents, persistent memory, production workflows | E2 — configuration/static |
| **EAP-L3** | High Assurance | Safety, rights-affecting, critical, or self-modifying systems | E3 — machine-generated execution |

A deployment MAY select a higher level. `scripts/derive_assurance_level.py` derives a minimum level from declared autonomy, impact, and environment characteristics.

## Assurance pipeline

```text
ATAL baseline
    ↓
EAP controls + assurance overlay
    ↓
deployment profile
    ↓
evidence collection + evidence-strength grading
    ↓
portable executable conformance tests
    ↓
positive and adversarial-negative observations
    ↓
assessment result
    ↓
bounded assurance claim
    ↓
expiry / revocation / reassessment
```

## Release maturity sequence

- **v0.4.0 — Assurance Provenance:** exact ATAL baseline pin, compatibility declaration, provenance validation.
- **v0.5.0 — Assurance Claims:** deployment profile, deterministic assurance-level derivation, lifecycle-aware claim schema.
- **v0.6.0 — Evidence Strength:** E0–E5 evidence model, level-specific strength and freshness expectations.
- **v0.7.0 — Executable Assurance:** portable test-case/result contracts and initial kill-switch/non-bypassability vectors.
- **v0.8.0 — Enterprise Interoperability:** confidence-scored, non-equivalence external-framework mappings.
- **v0.9.0 — Assurance Candidate:** cross-artifact invariants and consolidated quality-gate enforcement.
- **v0.9.1 — L2 Worked Assurance:** complete controlled-autonomy deployment, evidence, executable test results, assessment, generated report, and digest-bound assurance claim.
- **v0.9.2 — L3 Adversarial Assurance:** complete high-assurance deployment, expanded executable vectors, negative fixtures, and E4+ critical-control enforcement.

Release records are under `releases/`.

## Worked assurance cases

### EAP-L2 controlled autonomy

`examples/eap-l2-worked-example/` models a synthetic production purchasing agent with tool use, persistent memory, external side effects, financial impact, and regulated data. Those characteristics deterministically require at least **EAP-L2**.

### EAP-L3 high assurance

`examples/eap-l3-worked-example/` models a synthetic critical-operations coordination agent with safety and critical-operations impact. Those characteristics deterministically require **EAP-L3**.

The L3 case includes:

- evidence and assessment entries for all 20 mandatory L3 controls;
- executable results for evidence-integrity, replay, independent reconstruction, non-bypassability, kill-switch, dual-control, and delegation-boundary tests;
- adversarial negative fixtures for undetected evidence tampering and improper single-approver execution;
- fail-closed validation requiring designated critical L3 controls to carry E4 or E5 executable evidence;
- a generated digest-bound assurance claim and generated L3 assessment report.

The worked cases are reference evidence for the methodology. They are not certification of live enterprise deployments.

## Adversarial executable test catalog

v0.9.2 expands the portable conformance corpus with:

- `EAP-TEST-EI-001` — evidence-chain tamper detection;
- `EAP-TEST-RP-001` — replay detection and rejection;
- `EAP-TEST-RC-001` — independent reconstruction without the primary vendor dashboard;
- `EAP-TEST-DC-001` — dual-control enforcement;
- `EAP-TEST-DB-001` — delegation-boundary enforcement;
- existing `EAP-TEST-NB-001` — non-bypassability;
- existing `EAP-TEST-KS-001` — kill-switch effectiveness.

A negative fixture is expected to remain schema-valid while encoding a `fail` result. This distinction lets the repository test both artifact validity and unsafe system behavior without conflating the two.

## Quickstart

```bash
pip install -r requirements.txt
python scripts/run_quality_gate.py --mode validate
python scripts/run_quality_gate.py --mode all
```

Useful focused checks:

```bash
python scripts/check_upstream_integrity.py
python scripts/validate_test_catalog.py
python scripts/validate_external_mappings.py
python scripts/check_assurance_invariants.py
python scripts/validate_l2_worked_example.py
python scripts/validate_l3_worked_example.py
python scripts/derive_assurance_level.py examples/eap-l3-worked-example/deployment-profile.json
python scripts/build_l2_assurance_claim.py
python scripts/build_l3_assurance_claim.py
```

## Repository map

```text
upstream/                        Exact ATAL normative baseline and provenance declaration
catalogs/                        Canonical controls and EAP-L1/L2/L3 overlays
schemas/                         Machine-readable artifact contracts
assurance/                       Cross-artifact assurance invariants
evidence/                        Evidence templates, samples, and E0–E5 strength model
assessments/                     Assessment templates and samples
examples/eap-l2-worked-example/  Complete controlled-autonomy worked assurance case
examples/eap-l3-worked-example/  Complete high-assurance adversarial worked case
tests/catalog/                   Portable executable conformance vectors
mappings/                        ATAL traceability and external-framework mappings
scripts/                         Validators, derivation, grading, reporting, and build tooling
docs/                            Operational, artifact, catalog, claim, CLI, and maintainer guidance
artifacts/                       Generated checklists, reports, claims, traceability, and exports
releases/                        Release records and assurance impact summaries
```

## Authority model

EAP distinguishes **Profile Authority**, **System Authority**, **Assessment Authority**, and **Risk Acceptance Authority**. These roles may exist in one organization, but remain logically separate in evidence and claims.

Evidence is not assessment. Assessment is not risk acceptance. Risk acceptance is not EAP conformance. EAP conformance is not regulatory approval.

The L3 delegation and dual-control vectors additionally test whether delegated authority is technically constrained to its declared role and whether covered actions require the expected number of distinct authorizing identities.

## External-framework mappings

`mappings/external-framework-mappings.yaml` currently includes carefully bounded mappings to NIST AI RMF 1.0, ISO/IEC 42001:2023, ISO/IEC 23894:2023, and Regulation (EU) 2024/1689. Mappings are typed and confidence-scored; they are evidence-routing aids, not claims of legal or normative equivalence.

## Status

**v0.9.2 assurance candidate.** The repository now exercises complete L2 and L3 reference cases and rejects deliberately unsafe L3 outcomes through adversarial fixtures. The next hardening step is independent-assessor handoff and deterministic claim reconstruction in v0.9.3. It remains a working assurance profile, not an external certification scheme.

## License

See `LICENSE.md`.
