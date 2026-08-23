# Artifact Model

This document explains how EAP artifacts relate to each other and which artifact is authoritative at each stage.

For a first-time walkthrough, see [`getting-started.md`](getting-started.md).

## Current artifact graph

```text
upstream/atal-baseline.yaml
          │
          ▼
catalogs/atal-eap-control-catalog.json
          │
          ├── catalogs/assurance-level-overlays/EAP-L1-overlay.json
          ├── catalogs/assurance-level-overlays/EAP-L2-overlay.json
          └── catalogs/assurance-level-overlays/EAP-L3-overlay.json
                          │
                          ▼
                 deployment-profile.json
                          │
                          ├── derive_assurance_level.py
                          ▼
                 generated checklist
                          │
                          ▼
                   evidence-bundle.json
                     │              │
                     │              └── executable test-results/*.json
                     ▼
                assessment-result.json
                     │
                     ├── assessment report (human-readable projection)
                     ▼
                assurance claim
                     │
                     ▼
          L3 independent-assessor handoff
                     │
                     ▼
           verification / rejection report
```

The repository intentionally keeps these artifacts separate. A single monolithic file would blur authority boundaries and make evidence transitions harder to verify independently.

## Upstream baseline

**File:** `upstream/atal-baseline.yaml`

Records the exact upstream ATAL specification version, commit, compatibility class, and EAP release version. It establishes what normative upstream state the EAP release claims to profile.

## Control catalog

**File:** `catalogs/atal-eap-control-catalog.json` (canonical) and YAML mirror.

Defines controls once, including IDs, titles, families, normative statements, evidence requirements, criticality, and ATAL traceability.

## Assurance-level overlays

**Files:** `catalogs/assurance-level-overlays/EAP-L{1,2,3}-overlay.json`

Overlays determine:

- applicability;
- mandatory control IDs;
- normative-strength overrides;
- evidence tightening;
- dependency rules.

They do not duplicate the canonical control definition.

## Deployment profile

**Schema:** `schemas/deployment-profile.schema.json`

This is the preferred entry artifact for a new assessment. It states what deployment is being assessed and records autonomy, impact, environment, and authority declarations.

Canonical first-use example:

```text
examples/eap-l2-worked-example/deployment-profile.json
```

`scripts/derive_assurance_level.py` uses these declared characteristics to derive a minimum EAP level.

## Generated checklist

**Produced by:** `scripts/generate_profile_checklist.py`

Generated JSON, CSV, and Markdown checklists project the catalog + overlay into a working assessment surface. They are derived artifacts, not the normative source of control semantics.

## Evidence bundle

**Schema:** `schemas/evidence-bundle.schema.json`

The evidence bundle contains control-level evidence entries, including statuses, evidence grades, artifact references, and exception/waiver references.

Evidence strength is governed by `evidence/evidence-strength-model.yaml`.

Evidence is input to assessment; it does not itself declare the formal assessment outcome.

## Executable test definition

**Schema:** `schemas/test-case.schema.json`

**Location:** `tests/catalog/`

Defines a portable conformance/adversarial test: stimuli, observations, pass conditions, control bindings, and expected evidence grade. Test definitions should remain adapter-neutral where possible.

## Executable test result

**Schema:** `schemas/test-result.schema.json`

A test result records what happened when a test was executed. A structurally valid result may record `pass`, `fail`, `indeterminate`, or `error` according to the stable result-state contract.

This distinction matters:

```text
invalid result artifact
        ≠
valid result artifact describing unsafe behavior
```

L3 negative fixtures deliberately exercise the second case.

## Assessment result

**Schema:** `schemas/assessment-result.schema.json`

Records the Assessment Authority's evaluation of controls against the applicable profile and evidence. It contains control results, findings, residual risks, and an overall assessment decision.

Assessment does not itself constitute enterprise risk acceptance.

## Waiver

**Schema:** `schemas/exception-waiver.schema.json`

A waiver records a bounded exception, compensating measures, approval, residual risk, and expiry/review expectations. A waiver does not increase evidence strength and must not silently convert a failed control into unconditional conformance.

## Human-readable assessment report

**Produced by:** `scripts/compile_assessment_report.py`

The Markdown report is a readable projection of the overlay, evidence bundle, and assessment. It is useful to operators and auditors but should not replace the machine-readable source artifacts.

## Assurance claim

**Schema:** `schemas/assurance-claim.schema.json`

A claim is a bounded statement derived from a deployment-scoped assessment. It binds:

- system and deployment subject;
- EAP profile/version;
- claim lifecycle state;
- control summary;
- evidence and assessment digests;
- validity/expiry/revocation information;
- Profile, System, Assessment, and Risk Acceptance authorities.

A claim is not a regulator approval or a general certification of the vendor/system outside its declared scope.

## Independent-assessor handoff

**Schema:** `schemas/assessor-handoff.schema.json`

**Source boundary:** `assurance/handoff-source-set.yaml`

The L3 handoff digest-binds the bounded artifact set needed for independent verification, including deployment, evidence, assessment, executable results, upstream baseline, current release record, and assurance claim.

`scripts/verify_assessor_handoff.py` checks declared integrity and lifecycle/authority consistency. It does not establish the truth of every underlying evidence assertion or inherit assessment/risk-acceptance authority.

## Verification reports

Generated machine-readable evidence includes:

```text
artifacts/eap-l3-handoff-verification.json
artifacts/eap-l3-handoff-tamper-verification.json
```

The tamper report is expected evidence that a deliberately changed digest is rejected.

## Repository-level assurance artifacts

The repository also contains assurance over its own contracts and release state:

- `assurance/invariants.yaml` — cross-artifact invariants;
- `assurance/stable-contracts.yaml` — frozen pre-v1 contract surface;
- `assurance/v1-readiness-criteria.yaml` — blocking release-readiness criteria;
- `assurance/governance-freeze.yaml` — authority/compatibility/release-governance freeze;
- `artifacts/v1-readiness-report.{json,md}` — generated readiness result.

These artifacts describe repository/profile readiness. They do not certify external deployments.

## Golden-path example map

### Learn the tooling

```text
examples/eap-l2-worked-example/
├── deployment-profile.json      ← start here
├── evidence-bundle.json
├── test-results/
└── assessment-result.json
```

### Understand the full assurance system

```text
examples/eap-l3-worked-example/
├── deployment-profile.json
├── evidence-bundle.json
├── test-results/
├── negative-fixtures/
├── reference/
└── assessment-result.json
```

See the README inside each example directory for the exact reading and execution order.

## Authority summary

| Artifact transition | Responsible authority / function |
|---|---|
| deployment declaration | System Authority |
| control/profile semantics | Profile Authority |
| evidence evaluation | Assessment Authority |
| residual risk decision | Risk Acceptance Authority |
| bounded handoff integrity verification | Independent Verifier |

Machine verifiability should make these transitions auditable without collapsing their authority boundaries.
