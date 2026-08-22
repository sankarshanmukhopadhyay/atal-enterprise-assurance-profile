# Assurance Claim Model

EAP assurance is expressed as a bounded claim about a specific deployment, not as a universal property of a model or organization.

## Authority separation

EAP distinguishes four authorities:

1. **Profile authority** — maintains EAP controls, schemas, tests, and claim semantics.
2. **System authority** — owns the evaluated deployment and its declared operating context.
3. **Assessment authority** — determines whether supplied evidence satisfies EAP controls.
4. **Risk acceptance authority** — may accept explicitly documented residual risk or waivers.

These authorities MAY be held by the same organization, but the roles MUST remain logically distinguishable in assurance records.

Evidence is not assessment. Assessment is not risk acceptance. Risk acceptance is not EAP conformance. EAP conformance is not regulatory approval.

## Deployment-derived assurance level

A deployment is described using `schemas/deployment-profile.schema.json`. `scripts/derive_assurance_level.py` derives a minimum level from autonomy, impact, and environment signals.

The derivation is intentionally conservative:

- safety, rights-affecting, critical-operations, or self-modifying deployments require EAP-L3;
- tool use, persistent memory, external side effects, financial impact, regulated data, production use, or internet exposure require at least EAP-L2;
- deployments without those signals may use EAP-L1.

An enterprise MAY choose a higher level. It MUST NOT claim a lower level than the deterministic derivation without recording an explicit profile exception, authority, rationale, and expiry.

## Claim states

- `CONFORMANT`
- `CONFORMANT-WITH-EXCEPTIONS`
- `PARTIALLY-CONFORMANT`
- `NON-CONFORMANT`
- `INDETERMINATE`
- `EXPIRED`
- `REVOKED`

A claim MUST identify its subject deployment, profile version, control result summary, evidence bundle digest, assessment digest, validity interval, and responsible authorities.

## Lifecycle

A claim becomes stale when its evidence expires, its deployment changes materially, its upstream/profile baseline changes in a way that affects mapped controls, or a required waiver expires. A stale claim MUST be reassessed before it is represented as current.

Revocation is explicit and auditable: a revoked claim records the revocation time and reason while preserving the prior state for reconstruction.
