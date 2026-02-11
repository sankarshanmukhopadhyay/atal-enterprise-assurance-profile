# ATAL → EAP Traceability (Draft)

Purpose: document how each EAP control family addresses a specific enterprise assurance gap while staying aligned to ATAL.

## Evidence Integrity
- Gap addressed: “Integrity-protected” evidence is ambiguous without custody, rotation, and verifier independence.
- EAP response: CRYPTO-1/2/3 define minimum assurance expectations and verification artifacts.

## Time & Ordering
- Gap addressed: reconstructability depends on ordering guarantees in distributed systems.
- EAP response: TIME-1/2/3 define minimum event fields and ordering model declarations.

## Non-bypassability
- Gap addressed: “non-bypassable” is threat-model-relative and often fails without network/identity controls.
- EAP response: NB-1/2/3 bind the claim to enterprise enforcement boundaries and change control.

## Privacy & Retention
- Gap addressed: logging without privacy controls creates new harm surfaces.
- EAP response: PRIV-1..4 establish protection, access governance, and retention-by-class.

## Control effectiveness testing
- Gap addressed: declarative controls degrade without adversarial testing and reconstruction drills.
- EAP response: TEST-1..3 require bypass tests, drills, and kill-switch exercises.

## Roles & separation of duties
- Gap addressed: approvals become ceremonial without SoD and dual-control.
- EAP response: ROLE-1/2 define separation and dual control expectations.
