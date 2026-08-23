# v1.0 Migration and Governance Freeze

## Status

v0.9.5 is the final planned pre-v1 hardening candidate. It freezes the contract and governance surfaces needed to enter the separate v1.0 decision gate; it is **not** v1.0 and does not authorize automatic promotion.

## What is frozen

The machine-readable freeze is `assurance/governance-freeze.yaml`. Together with `assurance/stable-contracts.yaml`, it freezes:

- release publication and immutable-tag behavior;
- Profile/System/Assessment/Risk-Acceptance/Independent-Verifier authority boundaries;
- core schema contracts declared candidate-stable;
- control/test identifier syntax;
- assurance-claim lifecycle states;
- executable test-result states;
- digest-addressed assessor-handoff lifecycle semantics.

## Migration expectation for 0.9.x implementers

Implementers using v0.9.5 should be able to carry conformant artifacts into a v1.0 decision without gratuitous identifier or state renaming. If the v1.0 decision requires an incompatible contract change, that change must be explicitly documented, tested, and accompanied by migration guidance in the v1 release PR.

No compatibility promise extends beyond the surfaces enumerated in `assurance/stable-contracts.yaml`.

## Evidence to bring into the v1 decision

The v1 decision should review at least:

1. exact upstream ATAL provenance and compatibility class;
2. L1/L2/L3 quality-gated reference paths;
3. adversarial positive and negative executable evidence;
4. E4+ critical L3 evidence requirements;
5. independent handoff verification and tamper rejection;
6. positive/negative core conformance corpus;
7. stable-contract compatibility results;
8. the generated `artifacts/v1-readiness-report.json`;
9. the non-blocking limitations recorded in the governance freeze.

## Authority and release rule

`ready_for_v1_decision` means that the evidence gate is satisfied. It does not grant permission to publish v1.0.

Issue #12 is the explicit governance decision point. A v1.0 release requires a dedicated issue disposition and release PR. Existing publication automation may publish an explicitly authored v1.0 release ledger after that decision; it must not invent the major-version transition itself.

## Non-claims

Neither v0.9.5 nor a future v1.0 version number by itself establishes deployment certification, regulatory approval, legal-compliance equivalence, independent third-party assurance, or enterprise risk acceptance.
