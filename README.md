# ATAL Enterprise Assurance Profile (EAP)

[![Upstream: ATAL Standard](https://img.shields.io/badge/upstream-ATAL%20Standard-2ea44f)](https://github.com/Elytra-Security/atal-standard)
[![Version](https://img.shields.io/badge/version-0.9.3-blue.svg)](./changelog/CHANGELOG.md)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](./LICENSE.md)
[![Status](https://img.shields.io/badge/status-assurance%20candidate-orange.svg)](./releases/v0.9.3.md)

## What this is

The **ATAL Enterprise Assurance Profile (EAP)** operationalizes the upstream ATAL Standard for enterprise deployments. It is an executable assurance layer: controls, deployment profiles, evidence contracts, conformance tests, assessments, bounded assurance claims, interoperability mappings, repository-level invariants, and independent-assessor handoffs are represented as machine-verifiable artifacts.

EAP does **not** replace ATAL, certify implementations, grant regulatory approval, or accept enterprise risk. ATAL retains authority over upstream specification semantics; EAP owns only its profile, mappings, tests, evidence contracts, handoff contracts, and claim semantics.

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
digest-addressed assessor handoff
    ↓
independent verification / rejection
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
- **v0.9.3 — Reproducible Assessment:** bounded digest-addressed independent-assessor handoff, deterministic verification, and tamper rejection.

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

## Independent-assessor handoff

v0.9.3 adds a bounded reproducibility layer. `assurance/handoff-source-set.yaml` declares the source boundary; `scripts/build_assessor_handoff.py` hashes the declared sources into `artifacts/eap-l3-assessor-handoff.json`.

The handoff binds the deployment profile, evidence bundle, assessment, executable test results, upstream baseline, release record, and generated claim. `scripts/verify_assessor_handoff.py` independently checks source digests, required roles, subject, authorities, profile/version, expiry and revocation semantics. A deliberate tamper fixture must be rejected for `digest-mismatch`.

Verification produces machine-readable reports:

- `artifacts/eap-l3-handoff-verification.json`;
- `artifacts/eap-l3-handoff-tamper-verification.json`.

See `docs/independent-assessor-handoff.md` for the authority boundary and handoff procedure.

## Adversarial executable test catalog

The portable conformance corpus includes:

- `EAP-TEST-EI-001` — evidence-chain tamper detection;
- `EAP-TEST-RP-001` — replay detection and rejection;
- `EAP-TEST-RC-001` — independent reconstruction without the primary vendor dashboard;
- `EAP-TEST-DC-001` — dual-control enforcement;
- `EAP-TEST-DB-001` — delegation-boundary enforcement;
- `EAP-TEST-NB-001` — non-bypassability;
- `EAP-TEST-KS-001` — kill-switch effectiveness.

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
python scripts/build_l3_assurance_claim.py
python scripts/build_assessor_handoff.py
python scripts/verify_assessor_handoff.py --tamper-self-test
```

## Repository map

```text
upstream/                        Exact ATAL normative baseline and provenance declaration
catalogs/                        Canonical controls and EAP-L1/L2/L3 overlays
schemas/                         Machine-readable artifact and handoff contracts
assurance/                       Cross-artifact invariants and bounded handoff source set
evidence/                        Evidence templates, samples, and E0–E5 strength model
assessments/                     Assessment templates and samples
examples/eap-l2-worked-example/  Complete controlled-autonomy worked assurance case
examples/eap-l3-worked-example/  Complete high-assurance adversarial worked case
tests/catalog/                   Portable executable conformance vectors
tests/fixtures/                  Deliberate negative/tamper fixtures
mappings/                        ATAL traceability and external-framework mappings
scripts/                         Validators, derivation, grading, reporting, handoff, and build tooling
docs/                            Operational, artifact, catalog, claim, handoff, CLI, and maintainer guidance
artifacts/                       Generated checklists, reports, claims, handoffs, verification evidence, traceability, and exports
releases/                        Release records and assurance impact summaries
```

## Authority model

EAP distinguishes **Profile Authority**, **System Authority**, **Assessment Authority**, and **Risk Acceptance Authority**. These roles may exist in one organization, but remain logically separate in evidence and claims.

Evidence is not assessment. Assessment is not risk acceptance. Risk acceptance is not EAP conformance. EAP conformance is not regulatory approval. Independent verification is not certification.

The independent verifier checks the bounded handoff's integrity, completeness, scope, authority references, and claim lifecycle. It does not inherit the authority to change the assessment, accept risk, or grant regulatory status.

## External-framework mappings

`mappings/external-framework-mappings.yaml` currently includes carefully bounded mappings to NIST AI RMF 1.0, ISO/IEC 42001:2023, ISO/IEC 23894:2023, and Regulation (EU) 2024/1689. Mappings are typed and confidence-scored; they are evidence-routing aids, not claims of legal or normative equivalence.

## Status

**v0.9.3 assurance candidate.** Complete L2/L3 reference cases, adversarial failures, E4+ critical-evidence enforcement, and independently reproducible digest-bound handoffs are now exercised by the canonical quality gate. The next hardening step is a machine-readable v1.0 readiness gate and stable conformance corpus in v0.9.4. The repository remains a working assurance profile, not an external certification scheme.

## License

See `LICENSE.md`.
