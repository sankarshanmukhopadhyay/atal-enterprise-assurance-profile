# Normative: Roles & Separation of Duties

## Required roles (MUST L1+)
Deployments MUST define:
- Operator-of-Record (OOR)
- Approver-of-Record (AOR) for higher-risk actions
- Policy Owner
- Evidence Custodian
- Safety Kernel Operator (where applicable)

## EAP-ROLE-1 — Separation of duties
**MUST L2+.**
- OOR and AOR MUST be distinct identities for higher-risk actions.
- Evidence Custodian MUST be distinct from Policy Owner where feasible.
- L3 MUST separate Policy Owner, Safety Kernel Operator, and Evidence Custodian.

## EAP-ROLE-2 — Dual control (MUST L3)
L3 deployments MUST enforce dual control for:
- kill-switch actions,
- high-impact policy changes,
- registry or enforcement configuration changes.
