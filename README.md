# ATAL Enterprise Assurance Profile (EAP)

[![Upstream: ATAL Standard](https://img.shields.io/badge/upstream-ATAL%20Standard-2ea44f)](https://github.com/Elytra-Security/atal-standard)
[![Version](https://img.shields.io/badge/version-0.9.4-blue.svg)](./changelog/CHANGELOG.md)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](./LICENSE.md)
[![Status](https://img.shields.io/badge/status-v1%20readiness%20candidate-orange.svg)](./releases/v0.9.4.md)

## What this is

The **ATAL Enterprise Assurance Profile (EAP)** operationalizes the upstream ATAL Standard for enterprise deployments. It is an executable assurance layer: controls, deployment profiles, evidence contracts, conformance tests, assessments, bounded assurance claims, interoperability mappings, repository-level invariants, independent-assessor handoffs, and release-readiness criteria are represented as machine-verifiable artifacts.

EAP does **not** replace ATAL, certify implementations, grant regulatory approval, or accept enterprise risk. ATAL retains authority over upstream specification semantics; EAP owns only its profile, mappings, tests, evidence contracts, handoff contracts, compatibility declarations, readiness criteria, and claim semantics.

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
candidate-stable compatibility checks
    ↓
v1.0 readiness report
    ↓
explicit governance decision
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
- **v0.9.4 — v1.0 Readiness Evidence:** candidate-stable contracts, positive/negative conformance corpus, and fail-closed readiness reporting.

Release records are under `releases/`.

## Worked assurance cases

### EAP-L2 controlled autonomy

`examples/eap-l2-worked-example/` models a synthetic production purchasing agent with tool use, persistent memory, external side effects, financial impact, and regulated data. Those characteristics deterministically require at least **EAP-L2**.

### EAP-L3 high assurance

`examples/eap-l3-worked-example/` models a synthetic critical-operations coordination agent with safety and critical-operations impact. Those characteristics deterministically require **EAP-L3**.

The L3 case includes all 20 mandatory controls, executable evidence-integrity/replay/reconstruction/non-bypassability/kill-switch/dual-control/delegation tests, adversarial negative fixtures, E4+ evidence requirements for designated critical controls, a digest-bound claim, and a generated assessment report.

The worked cases are reference evidence for the methodology. They are not certification of live enterprise deployments.

## Independent-assessor handoff

`assurance/handoff-source-set.yaml` declares the bounded source set. `scripts/build_assessor_handoff.py` hashes the declared sources into `artifacts/eap-l3-assessor-handoff.json`; `scripts/verify_assessor_handoff.py` checks source digests, required roles, subject, authorities, profile/version, expiry and revocation semantics. A deliberate digest-tamper fixture must be rejected.

Verification produces:

- `artifacts/eap-l3-handoff-verification.json`;
- `artifacts/eap-l3-handoff-tamper-verification.json`.

See `docs/independent-assessor-handoff.md`.

## Candidate-stable contracts and conformance corpus

v0.9.4 declares the intended pre-v1 stable surface in `assurance/stable-contracts.yaml`. The declaration includes candidate-stable schemas, control/test identifier syntax, assurance-claim states, and executable test-result states.

`scripts/check_contract_compatibility.py` fails if the declared surface disappears or loses required values. `tests/fixtures/conformance/manifest.yaml` then exercises positive and negative fixtures for core artifact classes; `scripts/validate_conformance_corpus.py` requires the expected accept/reject behavior.

## v1.0 readiness

`assurance/v1-readiness-criteria.yaml` defines blocking readiness criteria. `scripts/build_v1_readiness_report.py` generates:

- `artifacts/v1-readiness-report.json`;
- `artifacts/v1-readiness-report.md`.

The report is fail-closed: an unresolved blocking criterion prevents `ready_for_v1_decision`.

For **v0.9.4**, the expected state is **`not_ready`** because `V1-RDY-008`, the final governance and compatibility freeze, is intentionally pending v0.9.5. A successful v0.9.4 release therefore proves that readiness blockers are visible and enforced; it does not falsely claim that the repository is already ready for v1.0.

See `docs/v1-readiness.md`.

## Quickstart

```bash
pip install -r requirements.txt
python scripts/run_quality_gate.py --mode validate
python scripts/run_quality_gate.py --mode all
```

Useful focused checks:

```bash
python scripts/check_upstream_integrity.py
python scripts/check_assurance_invariants.py
python scripts/check_contract_compatibility.py
python scripts/validate_conformance_corpus.py
python scripts/validate_l2_worked_example.py
python scripts/validate_l3_worked_example.py
python scripts/build_l3_assurance_claim.py
python scripts/build_assessor_handoff.py
python scripts/verify_assessor_handoff.py --tamper-self-test
python scripts/build_v1_readiness_report.py
```

## Repository map

```text
upstream/                        Exact ATAL normative baseline and provenance declaration
catalogs/                        Canonical controls and EAP-L1/L2/L3 overlays
schemas/                         Machine-readable artifact and handoff contracts
assurance/                       Invariants, handoff source set, stable contracts, readiness criteria
evidence/                        Evidence templates, samples, and E0–E5 strength model
assessments/                     Assessment templates and samples
examples/eap-l2-worked-example/  Complete controlled-autonomy worked assurance case
examples/eap-l3-worked-example/  Complete high-assurance adversarial worked case
tests/catalog/                   Portable executable conformance vectors
tests/fixtures/                  Negative, tamper, and compatibility/conformance fixtures
mappings/                        ATAL traceability and external-framework mappings
scripts/                         Validators, builders, compatibility, handoff, readiness, and reporting tooling
docs/                            Operational and maintainer guidance
artifacts/                       Generated assurance, handoff, verification, readiness, and reporting evidence
releases/                        Release records and assurance impact summaries
```

## Authority model

EAP distinguishes **Profile Authority**, **System Authority**, **Assessment Authority**, and **Risk Acceptance Authority**. These roles may exist in one organization, but remain logically separate in evidence and claims.

Evidence is not assessment. Assessment is not risk acceptance. Risk acceptance is not EAP conformance. EAP conformance is not regulatory approval. Independent verification is not certification. Repository readiness is not automatic major-version promotion.

The explicit v1.0 decision remains a separate governance act after the readiness evidence is complete.

## External-framework mappings

`mappings/external-framework-mappings.yaml` contains bounded mappings to NIST AI RMF 1.0, ISO/IEC 42001:2023, ISO/IEC 23894:2023, and Regulation (EU) 2024/1689. Mappings are evidence-routing aids, not claims of legal or normative equivalence.

## Status

**v0.9.4 v1-readiness candidate.** The repository now tests its candidate-stable contract surface, core positive/negative conformance behavior, complete L2/L3 reference assurance paths, adversarial failures, and independently reproducible handoffs. Its readiness report intentionally remains `not_ready` until the v0.9.5 governance freeze is complete.

## License

See `LICENSE.md`.
