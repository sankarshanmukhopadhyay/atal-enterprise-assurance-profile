# ATAL Enterprise Assurance Profile (EAP)

[![Upstream: ATAL Standard](https://img.shields.io/badge/upstream-ATAL%20Standard-2ea44f)](https://github.com/Elytra-Security/atal-standard)
[![Version](https://img.shields.io/badge/version-0.9.5-blue.svg)](./changelog/CHANGELOG.md)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](./LICENSE.md)
[![Status](https://img.shields.io/badge/status-final%20pre--v1%20candidate-orange.svg)](./releases/v0.9.5.md)

## What this is

The **ATAL Enterprise Assurance Profile (EAP)** operationalizes the upstream ATAL Standard for enterprise deployments. It represents controls, deployment profiles, evidence contracts, executable conformance tests, assessments, bounded assurance claims, interoperability mappings, repository invariants, independent-assessor handoffs, compatibility contracts, and release-readiness criteria as machine-verifiable artifacts.

EAP does **not** replace ATAL, certify implementations, grant regulatory approval, establish legal-compliance equivalence, or accept enterprise risk. ATAL retains authority over upstream specification semantics. EAP owns its profile, mappings, tests, evidence/handoff contracts, compatibility declarations, readiness criteria, and claim semantics.

## Start Here — run one complete example first

If you are new to EAP, **start with the EAP-L2 worked example**. Do not begin with the schemas or control catalog.

The first file to read is:

```text
examples/eap-l2-worked-example/deployment-profile.json
```

It describes the system being assessed, its autonomy and impact characteristics, its environment, and the authorities responsible for the deployment, assessment, and risk acceptance.

Then follow the complete guided path in **[`docs/getting-started.md`](docs/getting-started.md)**.

The learning sequence is:

```text
deployment-profile.json
        ↓
derive minimum assurance level
        ↓
profile overlay + mandatory controls
        ↓
evidence-bundle.json
        ↓
executable test-results/
        ↓
assessment-result.json
        ↓
assessment report
        ↓
bounded assurance claim
        ↓
L3: independent-assessor handoff + verification
```

### Fast first run

```bash
python -m pip install -r requirements.txt

python scripts/derive_assurance_level.py \
  examples/eap-l2-worked-example/deployment-profile.json

python scripts/validate_l2_worked_example.py
python scripts/build_l2_assurance_claim.py
```

Then inspect:

```text
examples/eap-l2-worked-example/README.md
examples/eap-l2-worked-example/evidence-bundle.json
examples/eap-l2-worked-example/assessment-result.json
artifacts/eap-l2-assurance-claim.json
```

Once the L2 flow makes sense, continue to **[`examples/eap-l3-worked-example/README.md`](examples/eap-l3-worked-example/README.md)** for the complete high-assurance/adversarial path.

> **Learning rule:** L2 teaches the tooling. L3 demonstrates the full high-assurance system.

The repository intentionally does not collapse deployment facts, evidence, assessment, risk acceptance, and assurance claims into one monolithic file. Their separation is what allows each authority decision and evidence transition to be tested and audited independently.

## Assurance levels

| Level | Name | Intended use | Default evidence floor |
|---|---|---|---|
| **EAP-L1** | Enterprise Baseline | Internal copilots and lower-impact auditable workflows | E1 — documentary |
| **EAP-L2** | Controlled Autonomy | Tool-using agents, persistent memory, production workflows | E2 — configuration/static |
| **EAP-L3** | High Assurance | Safety, rights-affecting, critical, or self-modifying systems | E3 — machine-generated execution |

A deployment MAY select a higher level. `scripts/derive_assurance_level.py` derives the minimum level from declared autonomy, impact, and environment characteristics.

## Executable assurance pipeline

```text
ATAL baseline
    ↓
EAP controls + assurance overlay
    ↓
deployment profile
    ↓
evidence + evidence-strength grading
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
contract compatibility + conformance corpus
    ↓
v1.0 readiness report
    ↓
governance freeze
    ↓
explicit v1.0 decision (#12)
```

## Worked assurance examples

### EAP-L2 — canonical learning example

`examples/eap-l2-worked-example/` models a synthetic controlled-autonomy production purchasing agent. It contains:

- `deployment-profile.json` — **start here**;
- `evidence-bundle.json` — structured control evidence;
- `test-results/` — executable non-bypassability and kill-switch observations;
- `assessment-result.json` — assessor decision over the evidence;
- generated assessment report and digest-bound assurance claim.

See [`examples/eap-l2-worked-example/README.md`](examples/eap-l2-worked-example/README.md).

### EAP-L3 — full adversarial/high-assurance example

`examples/eap-l3-worked-example/` models a synthetic critical-operations agent whose safety/critical impact requires EAP-L3. It adds all 20 mandatory controls, E4/E5 critical evidence, seven positive executable test results, adversarial negative fixtures, independent-assessor handoff, and tamper rejection.

See [`examples/eap-l3-worked-example/README.md`](examples/eap-l3-worked-example/README.md).

These examples are reference artifacts for the method, not certification of live systems.

## Canonical quality gate

Run validation only:

```bash
python scripts/run_quality_gate.py --mode validate
```

Run validation and regenerate derived artifacts:

```bash
python scripts/run_quality_gate.py --mode all
```

The validation stage also checks that the operator onboarding golden path remains intact through `scripts/validate_operator_onboarding.py`.

## Independent-assessor handoff

`assurance/handoff-source-set.yaml` defines a bounded source set. `scripts/build_assessor_handoff.py` digest-binds deployment, evidence, assessment, executable results, upstream baseline, current release ledger, and generated claim. `scripts/verify_assessor_handoff.py` verifies integrity, required roles, profile/version, subject, authorities, expiry, and revocation semantics.

Generated evidence includes:

- `artifacts/eap-l3-assessor-handoff.json`
- `artifacts/eap-l3-handoff-verification.json`
- `artifacts/eap-l3-handoff-tamper-verification.json`

A deliberate digest mutation must be rejected for `digest-mismatch`.

## Frozen compatibility surface

`assurance/stable-contracts.yaml` identifies the pre-v1 frozen contract surface:

- declared core schemas;
- `EAP-CTRL-NNN` control identifiers;
- `EAP-TEST-*` test identifiers;
- assurance-claim lifecycle states;
- executable test-result states.

`scripts/check_contract_compatibility.py` and `tests/fixtures/conformance/` protect both compatibility and expected positive/negative artifact behavior. `assurance/governance-freeze.yaml` freezes the associated release-governance, authority, compatibility, and assurance-lifecycle rules for the v1 decision.

## v1.0 readiness and decision

`assurance/v1-readiness-criteria.yaml` defines blocking readiness criteria. `scripts/build_v1_readiness_report.py` emits:

- `artifacts/v1-readiness-report.json`
- `artifacts/v1-readiness-report.md`

In v0.9.5 the expected result is **`ready_for_v1_decision` with zero blockers**. CI must prove that result; the README does not substitute for it.

**Readiness is evidence, not release authority.** Issue **#12** is the explicit v1.0 governance decision point. No workflow may infer or automatically perform a major-version promotion from readiness status alone.

See `docs/v1-readiness.md`, `docs/v1-migration-and-freeze.md`, `GOVERNANCE.md`, and `COMPATIBILITY.md`.

## Repository map

```text
upstream/                        Exact ATAL provenance and compatibility baseline
catalogs/                        Canonical controls and L1/L2/L3 overlays
schemas/                         Machine-readable artifact/handoff contracts
assurance/                       Invariants, stable contracts, readiness criteria, governance freeze
evidence/                        Evidence templates, samples, E0–E5 model
assessments/                     Assessment templates and samples
examples/eap-l2-worked-example/  Start-here controlled-autonomy learning path
examples/eap-l3-worked-example/  High-assurance/adversarial progression
tests/catalog/                   Portable executable conformance vectors
tests/fixtures/                  Negative, tamper, and core conformance fixtures
mappings/                        ATAL traceability and bounded external mappings
scripts/                         Validation, build, compatibility, handoff, readiness, release tooling
docs/getting-started.md          Canonical first-use walkthrough
docs/                            Operator, assessor, maintainer, migration and governance guidance
artifacts/                       Generated assurance and readiness evidence
releases/                        Governed release ledgers
```

## Pre-v1 hardening sequence

- **v0.4.0 — Assurance Provenance:** exact upstream baseline and compatibility declaration.
- **v0.5.0 — Assurance Claims:** deployment-scoped claims with expiry/revocation and explicit authorities.
- **v0.6.0 — Evidence Strength:** E0–E5 evidence model and minimum evidence expectations.
- **v0.7.0 — Executable Assurance:** portable test contracts and initial enforcement vectors.
- **v0.8.0 — Enterprise Interoperability:** bounded, confidence-scored external-framework mappings.
- **v0.9.0 — Assurance Candidate:** cross-artifact invariants and consolidated quality gate.
- **v0.9.1 — L2 Worked Assurance:** complete controlled-autonomy evidence → assessment → claim path.
- **v0.9.2 — L3 Adversarial Assurance:** complete high-assurance path, negative fixtures, E4+ critical evidence.
- **v0.9.3 — Reproducible Assessment:** digest-addressed independent-assessor handoff and tamper rejection.
- **v0.9.4 — v1.0 Readiness Evidence:** candidate-stable contracts, positive/negative corpus, fail-closed readiness report.
- **v0.9.5 — Governance Freeze:** frozen pre-v1 authority, compatibility, lifecycle, and release-governance surfaces.

Release ledgers are under `releases/`.

## Authority model

EAP distinguishes **Profile Authority**, **System Authority**, **Assessment Authority**, **Risk Acceptance Authority**, and **Independent Verifier**. These may exist within one organization but remain logically distinct in the evidence model.

Evidence is not assessment. Assessment is not risk acceptance. Risk acceptance is not EAP conformance. EAP conformance is not regulatory approval. Independent verification is not certification. Repository readiness is not automatic major-version promotion.

## Status

**v0.9.5 — final pre-v1 release candidate.** The planned 0.9.x hardening sequence is complete. The repository is machine-verifiable as ready to enter the separate v1.0 decision gate, while preserving explicit non-claims and authority boundaries.

## License

See `LICENSE.md`.
