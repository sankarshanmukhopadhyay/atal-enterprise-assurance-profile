# EAP-L2 — Controlled Autonomy (Checklist)

## Intended use
Tool-using agents, routing, persistent memory, and production workflows.

## Required control families

### Evidence Integrity
- MUST: append-only / hash-chained evidence log with signed bundle manifests
- MUST: KMS/HSM key custody + documented rotation and compromise procedure
- MUST: vendor-independent verification steps documented

### Time & Ordering
- MUST: `sequence_number` per producer + monotonic time included
- MUST: declared ordering strategy (centralized or hybrid) and reconciliation rules

### Non-bypassability
- MUST: network-level and identity-level controls prevent direct endpoint access
- MUST: change control on gateways, registries, evaluators, safety kernel configs

### Privacy & Retention
- MUST: field-level encryption or structured redaction for sensitive classes
- MUST: least-privilege, audited evidence access; time-boxed auditor sessions
- MUST: retention-by-risk-class policy

### Control effectiveness testing
- MUST: quarterly bypass test suite (gateway bypass, memory side-channel, delegation)
- MUST: evidence reconstruction drill every 6 months
- MUST: kill-switch tabletop + controlled exercise annually

### Roles & Separation of Duties
- MUST: Approver-of-Record for higher-risk actions is distinct from Operator-of-Record
- MUST: Evidence Custodian role defined with access governance
