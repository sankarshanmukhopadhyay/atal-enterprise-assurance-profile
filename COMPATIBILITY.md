# ATAL Enterprise Assurance Profile (EAP)
## Compatibility and Versioning Policy

## 1. Normative language

The key words **MUST**, **MUST NOT**, **REQUIRED**, **SHALL**, **SHALL NOT**, **SHOULD**, **SHOULD NOT**, **RECOMMENDED**, **MAY**, and **OPTIONAL** are interpreted as described by RFC 2119 and RFC 8174 when capitalized.

## 2. Purpose and scope

EAP is an assurance overlay for the ATAL Standard. It does not replace, fork, or redefine ATAL. It profiles, constrains, and operationalizes ATAL for enterprise assurance contexts.

Version identifiers communicate assurance stability, compatibility scope, and change risk.

## 3. Versioning model

EAP follows Semantic Versioning (`MAJOR.MINOR.PATCH`) independently of upstream ATAL version numbers.

- **MAJOR**: incompatible assurance requirements or profile semantics.
- **MINOR**: backward-compatible capabilities, profiles, or control families.
- **PATCH**: compatible hardening, clarifications, evidence/test additions, and operational improvements.

EAP SHALL NOT mirror ATAL version identifiers merely for visual alignment.

## 4. Upstream compatibility declaration

Every EAP release MUST declare:

1. the upstream ATAL version profiled;
2. the exact upstream tag or commit used as the normative baseline;
3. the compatibility class.

The machine-readable authority is `upstream/atal-baseline.yaml`. Missing upstream provenance renders a release incomplete.

## 5. Compatibility classes

- **Strict Compatible** — EAP profiles ATAL without additional normative constraint or extension.
- **Constrained Compatible** — EAP narrows ATAL optionality without contradiction.
- **Extended Compatible** — EAP adds enterprise assurance requirements without contradicting ATAL.

EAP SHALL NOT contradict upstream ATAL normative requirements under any compatibility class.

## 6. Version advancement policy

| Change type | Increment |
|---|---|
| Incompatible assurance requirement/profile change | MAJOR |
| New enterprise assurance level | MINOR |
| Backward-compatible new control family | MINOR |
| Compatible mapping/evidence/test hardening | PATCH |
| Clarification without semantic break | PATCH |
| Upstream change requiring incompatible EAP reinterpretation | MAJOR |

## 7. Candidate-stable pre-v1 surface

As of v0.9.5, `assurance/stable-contracts.yaml` is frozen for the explicit v1.0 decision. The frozen surface includes:

- the declared core schemas;
- `EAP-CTRL-NNN` control identifier syntax;
- `EAP-TEST-*` executable-test identifier syntax;
- assurance-claim states;
- test-result states.

`scripts/check_contract_compatibility.py` is the executable compatibility check for this surface.

Before the explicit v1.0 decision, a frozen identifier, state, or required core-field contract MUST NOT be incompatibly changed without a documented breaking-change disposition. A change that would make existing conformant artifacts invalid MUST be treated as a compatibility event, not a routine patch.

## 8. Upstream pinning and audit requirements

For audit-grade use, implementers SHOULD archive both the EAP release and exact upstream ATAL baseline. Assurance handoffs SHOULD preserve digest-addressed source references and version information.

Failure to pin upstream references introduces interpretive ambiguity and weakens assurance claims.

## 9. Forward evolution and v1.0

EAP MAY reach 1.0 independently of ATAL if enterprise assurance semantics, control mappings, executable conformance behavior, handoff reproducibility, and compatibility behavior are sufficiently stable.

A `ready_for_v1_decision` readiness result does not itself change the version. Major-version promotion requires the explicit governance process identified in issue #12 and a dedicated release PR.

No automated release workflow is authorized to infer v1.0 solely from readiness evidence.

## 10. Governance principle

Version identifiers are risk indicators. EAP versioning prioritizes compatibility clarity, assurance predictability, auditor interpretability, controlled evolution, and preserved evidence history. Version inflation or silent compatibility breaks are prohibited.
