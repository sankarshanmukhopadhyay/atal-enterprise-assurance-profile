# EAP-L3 — High Assurance (Checklist)

## Intended use
High-impact autonomy and environments requiring strong assurance (safety, security, finance, critical ops).

## Required control families

### Evidence Integrity
- MUST: append-only / hash-chained evidence log with signed manifests
- MUST: KMS/HSM custody + strict rotation + compromise playbook
- SHOULD: external witnessing or anchoring for evidence chain heads (transparency / timestamp)
- MUST: independent verification tooling/process documented

### Time & Ordering
- MUST: monotonic sequencing + declared cross-node ordering strategy
- MUST: replay detection strategy documented and tested

### Non-bypassability
- MUST: platform attestation expectations documented for safety kernel integrity (where feasible)
- MUST: strict network policy ensuring the enforcement layer is the only invocation path
- MUST: explicit threat model boundaries declared

### Privacy & Retention
- MUST: field-level encryption + redaction-by-class
- MUST: audited evidence access + export controls; watermarking recommended
- MUST: retention policy aligned to jurisdiction and criticality

### Control effectiveness testing
- MUST: quarterly adversarial bypass tests + registry tampering simulations
- MUST: semi-annual reconstruction drills; one drill must be “vendor tooling unavailable”
- MUST: kill-switch live-fire in controlled env; dual-control enforced

### Roles & Separation of Duties
- MUST: separation between Policy Owner, Safety Kernel Operator, and Evidence Custodian
- MUST: dual-control for kill-switch and high-impact policy changes
