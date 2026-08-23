# Operational Model

This document describes the current end-to-end EAP assurance workflow.

If you are using EAP for the first time, begin with [`getting-started.md`](getting-started.md) and the complete EAP-L2 worked example. This document explains the general model behind that walkthrough.

## Overview

EAP is a portable assurance workflow implemented through machine-readable artifacts and lightweight Python tooling. It does not require a proprietary platform or SaaS product.

The current workflow is:

```text
deployment declaration
        ↓
minimum assurance-level derivation
        ↓
profile overlay + mandatory controls
        ↓
evidence collection + strength grading
        ↓
portable executable tests
        ↓
assessment result
        ↓
bounded assurance claim
        ↓
L3: assessor handoff + independent verification
```

Each transition preserves a different authority boundary. Evidence collection does not itself make an assessment decision; an assessment does not itself accept enterprise risk; a valid EAP claim does not confer regulatory approval.

## Step 1 — Describe the deployment

Create a deployment profile using `schemas/deployment-profile.schema.json`.

The profile records:

- system and deployment identity;
- autonomy characteristics;
- impact characteristics;
- environment characteristics;
- System Authority;
- Assessment Authority;
- Risk Acceptance Authority.

Canonical learning example:

```text
examples/eap-l2-worked-example/deployment-profile.json
```

## Step 2 — Derive the minimum assurance level

Run:

```bash
python scripts/derive_assurance_level.py <deployment-profile.json>
```

The derivation is fail-closed with respect to declared high-impact signals:

- safety, rights-affecting, critical-operations, or self-modification signals require EAP-L3;
- tool use, persistent memory, external side effects, financial/regulated-data impact, production operation, or internet exposure require at least EAP-L2;
- otherwise the baseline is EAP-L1.

A deployment may deliberately select a higher level than the minimum.

## Step 3 — Generate the profile checklist

Generate a checklist for the selected level:

```bash
python scripts/generate_profile_checklist.py --level EAP-L2 --format all
```

The checklist is derived from:

```text
catalogs/atal-eap-control-catalog.json
catalogs/assurance-level-overlays/EAP-L2-overlay.json
```

The overlay determines applicability, mandatory controls, normative-strength changes, evidence tightening, and dependencies.

## Step 4 — Collect and grade evidence

Create an evidence bundle using `schemas/evidence-bundle.schema.json` and the templates under `evidence/templates/`.

Evidence entries should identify:

- control ID;
- status;
- artifact references;
- evidence grade;
- any waiver/exception references.

The evidence-strength model is defined in:

```text
evidence/evidence-strength-model.yaml
```

Grades range from assertion-only evidence to externally attested/reproducible evidence. Higher assurance levels impose stronger evidence expectations.

## Step 5 — Produce executable observations where required

Portable test definitions live under:

```text
tests/catalog/
```

Execution produces machine-readable test results that can be cited by evidence items. The current corpus includes non-bypassability, kill-switch, evidence-integrity, replay, reconstruction, dual-control, and delegation-boundary tests.

A valid result artifact may still record a `fail` outcome. That is intentionally different from a malformed result artifact.

## Step 6 — Validate evidence coverage

Use:

```bash
python scripts/check_required_controls.py \
  --level EAP-L2 \
  --bundle <evidence-bundle.json>
```

For the canonical examples, cross-artifact validators additionally check expected test bindings, assurance-level derivation, decision semantics, and stronger L3 evidence requirements:

```bash
python scripts/validate_l2_worked_example.py
python scripts/validate_l3_worked_example.py
```

## Step 7 — Assess controls

The Assessment Authority evaluates evidence against the applicable EAP control criteria and produces an assessment result using `schemas/assessment-result.schema.json`.

Check mandatory assessment coverage:

```bash
python scripts/check_required_controls.py \
  --level EAP-L2 \
  --result <assessment-result.json>
```

Assessment states and findings remain separate from risk acceptance.

## Step 8 — Compile the human-readable report

```bash
python scripts/compile_assessment_report.py \
  --level EAP-L2 \
  --bundle <evidence-bundle.json> \
  --result <assessment-result.json>
```

The generated report is a readable projection of machine-readable source artifacts, not a replacement source of truth.

## Step 9 — Build a bounded assurance claim

The sample claim builders create deployment-scoped claims:

```bash
python scripts/build_l2_assurance_claim.py
python scripts/build_l3_assurance_claim.py
```

Claims are versioned, time-bounded, authority-scoped, and digest-bound to supporting evidence and assessment artifacts. Claim lifecycle supports expiry and explicit revocation.

## Step 10 — Independently verify a high-assurance handoff

The L3 path can package a bounded assessor handoff:

```bash
python scripts/build_assessor_handoff.py
python scripts/verify_assessor_handoff.py --tamper-self-test
```

The handoff lets a separate verifier check source digests, required roles, deployment/subject scope, authorities, version, expiry, and revocation semantics. The tamper self-test proves a digest mutation is rejected.

Independent verification does not establish the truth of every underlying evidence assertion and does not inherit Assessment Authority or Risk Acceptance Authority.

## Step 11 — Run the repository assurance gate

Validation only:

```bash
python scripts/run_quality_gate.py --mode validate
```

Validation plus generated outputs:

```bash
python scripts/run_quality_gate.py --mode all
```

The canonical quality gate also protects repository invariants, contract compatibility, governance freeze requirements, conformance fixtures, and the operator onboarding golden path.

## Waivers and remediation

Where a control is failed, partial, or waived:

- record the finding in the assessment;
- create a waiver record where appropriate;
- identify compensating controls;
- record residual risk and the responsible Risk Acceptance Authority;
- include an expiry/review date;
- preserve remediation targets and evidence for reassessment.

Waivers do not increase evidence strength and do not automatically produce conformance.

## Authority model

The workflow intentionally keeps these roles logically separate:

| Authority | Owns |
|---|---|
| Profile Authority | EAP control/profile/claim semantics |
| System Authority | responsibility for the deployed system |
| Assessment Authority | evaluation against EAP requirements |
| Risk Acceptance Authority | acceptance or rejection of residual enterprise risk |
| Independent Verifier | verification of a bounded handoff and its declared integrity properties |

Evidence is not assessment. Assessment is not risk acceptance. Risk acceptance is not EAP conformance. EAP conformance is not regulatory approval. Independent verification is not certification.
