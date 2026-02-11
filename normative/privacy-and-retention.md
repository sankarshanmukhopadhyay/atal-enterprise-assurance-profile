# Normative: Privacy, Minimization & Retention

## EAP-PRIV-1 — Field-level protection
**MUST L2+; SHOULD L1.**

Evidence stores MUST support either:
- field-level encryption, or
- structured redaction with integrity-preserving references,
for sensitive data classes.

## EAP-PRIV-2 — Auditor access governance (MUST L1+)
Evidence access MUST enforce:
- least-privilege roles,
- time-bounded access sessions (where feasible),
- audited access logs,
- controlled export of forensic bundles.

## EAP-PRIV-3 — Retention-by-class
**MUST L2+; SHOULD L1.**
Retention MUST be defined as a function of:
- risk class,
- data classification,
- jurisdictional obligations,
with documented deletion and archival procedures.

## EAP-PRIV-4 — Evidence store incident posture
**MUST L3.**
L3 deployments MUST document breach impact, mitigation, and incident response for evidence stores.
