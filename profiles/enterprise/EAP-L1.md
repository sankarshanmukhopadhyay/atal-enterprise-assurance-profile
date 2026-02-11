# EAP-L1 — Enterprise Baseline (Checklist)

## Intended use
Internal copilots and constrained workflow assistance where:
- actions are low-to-medium impact,
- enterprise audit readiness is required,
- autonomy is bounded and tool access is limited.

## Required control families

### Evidence Integrity
- MUST: evidence objects are integrity-protected and tamper-evident (see `normative/evidence-integrity.md`)
- MUST: signing keys are managed outside application code (enterprise KMS/HSM)

### Time & Ordering
- SHOULD: per-producer `sequence_number` for evidence objects
- MUST: consistent timestamps with documented tolerance assumptions

### Non-bypassability
- MUST: tool/API/memory invocations route through ATAL enforcement layer
- MUST: policy/config changes are versioned and auditable

### Privacy & Retention
- SHOULD: structured redaction for sensitive input fields
- MUST: documented retention policy aligned to data classification

### Control effectiveness testing
- SHOULD: quarterly bypass attempts for direct tool invocation
- SHOULD: annual evidence reconstruction drill (internal)

### Roles & Separation of Duties
- MUST: Operator-of-Record identity captured on high-impact actions
- SHOULD: basic separation between Policy Owner and Evidence Custodian
