# Governance

This repository maintains an assurance profile that is designed to remain **compatible with ATAL** while making assurance claims **testable and comparable** in enterprise contexts.

## Principles
- **Assurance-first**: requirements must be auditable, verifiable, and operationally enforceable.
- **Vendor-neutral**: no dependence on proprietary tooling to verify compliance evidence.
- **Profile-based**: the core stays lean; profiles encode deployment expectations.
- **Traceable**: every EAP requirement should map to ATAL concepts or close a clearly stated assurance gap.
- **Adversarial realism**: requirements must survive bypass attempts and operational abuse cases.

## Change process
- Propose changes via GitHub Issues or Pull Requests.
- Any normative change should include:
  1) rationale (what failure mode it prevents),
  2) assurance level impact (L1/L2/L3),
  3) mapping impact (how traceability changes),
  4) test harness impact (what new test is required).

## Versioning
- EAP versions track ATAL releases.
- A release notes entry is required for:
  - new or changed normative requirements,
  - changes to assurance level checklists,
  - changes to evidence or test expectations.

## Maintainer decisions
Decisions should aim for:
- clarity over flexibility when ambiguity breaks auditability,
- explicit threat model boundaries over implicit claims,
- structured evidence over narrative explanations.
