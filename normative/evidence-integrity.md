# Normative: Evidence Integrity

## EAP-CRYPTO-1 — Signed evidence chain
**MUST for L2+; MUST for L1 with simplified chain.**

Evidence objects (decision records, trails, SML, EIT, CAG snapshots, manifests) MUST be covered by an integrity mechanism that provides:
- tamper evidence,
- append-only semantics (or equivalent), and
- deterministic verification steps.

### Minimum expectations
- Evidence objects MUST be hashed and referenced from a chain head.
- Forensic bundle manifests MUST include hashes for all included objects and the chain head.

## EAP-CRYPTO-2 — Key custody and rotation (MUST L1+)
- Signing keys MUST be managed by enterprise-grade key management (KMS/HSM).
- Rotation schedules MUST be documented.
- Compromise procedures MUST include: key revocation, trust discontinuity signaling, and chain re-anchoring guidance.

## EAP-CRYPTO-3 — Verifier independence (MUST L1+)
Evidence MUST be verifiable without proprietary vendor systems.
A verification guide MUST include:
- required inputs,
- verification steps,
- failure modes,
- interpretation of results.

## Notes (non-normative)
EAP intentionally does not mandate a single cryptographic algorithm suite here; future versions may introduce explicit suites or profiles.
