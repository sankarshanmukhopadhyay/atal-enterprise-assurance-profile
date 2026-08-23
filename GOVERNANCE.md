# Governance

This repository maintains an assurance profile designed to remain **compatible with ATAL** while making assurance claims **testable, reproducible, and comparable** in enterprise contexts.

## Principles

- **Assurance-first**: requirements must be auditable, verifiable, and operationally enforceable.
- **Vendor-neutral**: verification must not depend on proprietary tooling.
- **Profile-based**: the core stays lean; profiles encode deployment expectations.
- **Traceable**: every EAP requirement maps to ATAL concepts or closes a stated assurance gap.
- **Adversarial realism**: requirements must survive bypass attempts and operational abuse cases.
- **Explicit authority**: evidence, assessment, risk acceptance, independent verification, and regulatory authority are distinct.

## Authority model

EAP distinguishes:

1. **Profile Authority** — governs EAP schemas, controls, mappings, tests, handoff contracts, and claim semantics.
2. **System Authority** — remains accountable for the assessed deployment and deployment declarations.
3. **Assessment Authority** — evaluates evidence and issues the assessment result.
4. **Risk Acceptance Authority** — owns waivers and residual-risk acceptance.
5. **Independent Verifier** — verifies bounded integrity, completeness, reproducibility, authority references, and lifecycle semantics.

Independent verification does not confer certification, risk-acceptance authority, regulatory approval, or authority to redefine upstream ATAL.

## Change process

Changes are proposed through GitHub Issues and Pull Requests. A normative change should include:

1. rationale and failure mode;
2. assurance-level impact (L1/L2/L3);
3. mapping/compatibility impact;
4. executable-test or evidence impact;
5. authority/delegation impact where applicable.

Release changes are validated by the canonical quality gate before merge. Governed publication binds a release ledger to an exact immutable tag target.

## v0.9.5 governance freeze

`assurance/governance-freeze.yaml` freezes the following pre-v1 decision surfaces:

- release governance and immutable-tag behavior;
- authority boundaries;
- candidate-stable schema/identifier/state compatibility surface;
- assurance claim and independent-handoff lifecycle semantics.

Changes to a frozen surface before v1.0 require an explicit breaking-change disposition. Silent semantic drift is not permitted.

## v1.0 decision authority

A machine-generated result of `ready_for_v1_decision` is **evidence**, not an authorization to publish v1.0.

The v1.0 decision is explicitly governed by GitHub issue **#12** and a corresponding release PR. No workflow may infer or automatically perform a major-version promotion from readiness status alone.

The v1 decision must consider the frozen contract surface, outstanding non-blocking limitations, upstream compatibility, migration impact, and evidence from the complete 0.9.x hardening train.

## Maintainer decisions

Decisions should prioritize:

- clarity over flexibility when ambiguity breaks auditability;
- explicit threat-model boundaries over implicit claims;
- structured evidence over narrative assertion;
- machine-verifiable enforcement over undocumented convention;
- preserved audit history over rewriting prior states.
