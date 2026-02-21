# ATAL Enterprise Assurance Profile (EAP)
## Compatibility and Versioning Policy

---

## 1. Normative Language

The key words **MUST**, **MUST NOT**, **REQUIRED**, **SHALL**, **SHALL NOT**,  
**SHOULD**, **SHOULD NOT**, **RECOMMENDED**, **MAY**, and **OPTIONAL** in this document are to be interpreted as described in:

- RFC 2119 — Key words for use in RFCs to Indicate Requirement Levels  
- RFC 8174 — Ambiguity of Uppercase vs Lowercase in RFC 2119 Key Words  

These terms are normative only when capitalized.

---

## 2. Purpose and Scope

This document defines how versions of the ATAL Enterprise Assurance Profile (EAP) relate to upstream ATAL Standard releases.

EAP is an assurance overlay. It does not replace, fork, or redefine ATAL.  
It profiles, constrains, and operationalizes ATAL for enterprise deployment contexts.

Version identifiers SHALL communicate:

- Assurance stability  
- Compatibility scope  
- Change risk  

---

## 3. Versioning Model

EAP SHALL follow Semantic Versioning (SemVer):

MAJOR.MINOR.PATCH

Version components SHALL be incremented as follows:

- MAJOR: Incompatible changes to assurance requirements or profile semantics.
- MINOR: Backward-compatible additions, new profiles, or expanded control mappings.
- PATCH: Corrections, documentation fixes, clarifications, or non-normative refinements.

EAP version numbers SHALL be independent of upstream ATAL version numbers.

EAP SHALL NOT mirror ATAL version identifiers solely for visual alignment.

---

## 4. Upstream Compatibility Declaration

Each EAP release MUST declare:

1. The upstream ATAL version it profiles.
2. The specific upstream tag or commit hash used as the normative baseline.
3. The compatibility class defined in Section 5.

This declaration SHALL be recorded in:

- UPSTREAM.md
- The GitHub Release Notes
- The repository compatibility matrix

Failure to declare upstream compatibility renders the release incomplete.

---

## 5. Compatibility Classes

EAP SHALL classify upstream alignment using one of the following classes:

### 5.1 Strict Compatible

EAP profiles ATAL without redefining, constraining, or extending normative behavior.  
All EAP controls map directly to ATAL constructs.

### 5.2 Constrained Compatible

EAP narrows optionality in ATAL (e.g., converting MAY to MUST for enterprise assurance).  
No ATAL normative requirement is contradicted.

### 5.3 Extended Compatible

EAP introduces additional enterprise assurance requirements not explicitly defined in ATAL, provided they do not conflict with ATAL normative behavior.

EAP SHALL NOT contradict upstream ATAL normative requirements under any compatibility class.

---

## 6. Version Advancement Policy

EAP version increments SHALL be governed as follows:

| Change Type | Version Increment |
|-------------|-------------------|
| Incompatible assurance requirement change | MAJOR |
| New enterprise assurance level | MINOR |
| New control family (backward compatible) | MINOR |
| Mapping updates without semantic change | PATCH |
| Clarification of requirement intent | PATCH |
| Upstream ATAL minor update with no impact | PATCH |
| Upstream ATAL update requiring control reinterpretation | MINOR |
| Upstream ATAL breaking normative change affecting EAP semantics | MAJOR |

If upstream ATAL introduces normative changes that alter EAP control semantics, EAP MUST increment MAJOR.

---

## 7. Compatibility Matrix

The repository SHALL maintain a compatibility matrix mapping EAP versions to upstream ATAL versions.

Example:

| EAP Version | Upstream ATAL | Compatibility Class |
|-------------|---------------|---------------------|
| v0.1.x | v0.9.x | Constrained Compatible |

The matrix MUST be updated as part of each release.

---

## 8. Upstream Pinning and Audit Requirements

For audit-grade deployments:

- Implementers SHOULD pin both the EAP version and the upstream ATAL tag/commit.
- Implementers SHOULD archive both artifacts as part of conformance evidence.
- Implementers MAY include the compatibility matrix in audit documentation.

Failure to pin upstream references introduces interpretive ambiguity and weakens assurance claims.

---

## 9. Forward Evolution

EAP MAY reach 1.0.0 independently of ATAL reaching 1.0.0 if:

- Enterprise assurance semantics are stable.
- Control mappings are mature.
- Test harness artifacts are reproducible.
- Compatibility behavior is predictable.

Conversely, EAP MAY remain pre-1.0.0 even if ATAL reaches 1.0.0 where assurance interpretation remains under active refinement.

Version numbers SHALL reflect assurance stability, not ecosystem symbolism.

---

## 10. Governance Principle

Version identifiers are risk indicators.

EAP versioning SHALL prioritize:

- Compatibility clarity  
- Assurance predictability  
- Auditor interpretability  
- Controlled evolution  

Version inflation for signaling alignment is prohibited.
