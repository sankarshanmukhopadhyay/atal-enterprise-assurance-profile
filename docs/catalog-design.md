# Catalog Design

This document explains the design decisions behind the EAP control catalog introduced in v0.2.0.

## Control ID format

Control IDs follow the pattern:

```
EAP-CTRL-NNN
```

where `NNN` is a zero-padded three-digit integer. Examples: `EAP-CTRL-001`, `EAP-CTRL-012`.

IDs are stable across versions. Once assigned, a control ID is never reused or reassigned, even if the control is deprecated. This ensures that historical assessment records remain traceable.

A deprecated control should be marked with a `status: deprecated` field rather than removed from the catalog.

---

## Family taxonomy

Controls are organized into eight families:

| Family | Description |
|---|---|
| **Governance** | Policy, declaration, threat model, and ordering model controls |
| **Enforcement** | Non-bypassability and change control at the enforcement boundary |
| **Oversight** | Role definitions, separation of duties, and dual control |
| **Security** | Field-level protection, replay detection, and data classification |
| **Resilience** | Kill-switch readiness, incident posture, and continuity of evidence |
| **Forensics and Reconstruction** | Bypass testing, reconstruction drills, and evidence exercises |
| **Vendor and Integration** | Vendor dependency documentation and supply chain assurance |
| **Evidence and Assurance** | Evidence chain integrity, key custody, and verifier independence |

Families are used for grouping in checklists and reports. A control belongs to exactly one family.

---

## Normative strength model

EAP inherits its normative vocabulary from the ATAL upstream standard:

| Term | Meaning |
|---|---|
| **MUST** / **SHALL** | Mandatory. Absence is a conformance failure. |
| **SHOULD** | Strongly recommended. Non-compliance must be documented with rationale. |
| **MAY** | Optional. No conformance implication. |

The catalog records the baseline normative strength per control. Overlays may tighten the strength for a specific assurance level (e.g. a `SHOULD` at EAP-L1 may become a `MUST` at EAP-L2).

Overlays never relax normative strength — they only tighten.

---

## Overlay design

Overlays implement the principle: *define controls once, apply them many ways.*

The master catalog defines all controls with their baseline strength. Each assurance-level overlay (`EAP-L1-overlay.json`, `EAP-L2-overlay.json`, `EAP-L3-overlay.json`) specifies:

- which controls are applicable at that level
- any tightening of normative strength
- any additional evidence requirements beyond the catalog baseline
- dependency rules (controls that must also be assessed if this one is applicable)

The set of mandatory control IDs for each level is explicitly listed in the overlay's `mandatory_control_ids` array. This list drives `check_required_controls.py`.

### Adding controls

To add a new control:
1. Add it to the catalog with a new stable ID.
2. Update each overlay to include an entry for the new control, marking it applicable or not as appropriate.
3. Update `mandatory_control_ids` in any overlays where the control is mandatory.

---

## Traceability rules

Every control must have:

- at least one `mapped_atal_references` entry pointing back to an ATAL concept
- at least one `mapped_repo_sources` entry pointing to an existing normative or test-harness document in this repository

Controls without ATAL traceability must be justified in the PR that adds them.

Traceability is generated as a matrix by `scripts/build_traceability_matrix.py`.

---

## Automation candidacy

The `automation_candidate` boolean flags controls where automated evidence collection or validation is feasible in principle. This does not mean automation is required — it is a signal for future CI integration work.

Controls with `automation_candidate: true` in v0.2.0 include:
- EAP-CTRL-001 (hash verification)
- EAP-CTRL-004 (schema validation for event fields)
- EAP-CTRL-006 (replay detection test)
- EAP-CTRL-007 (network policy inspection)
- EAP-CTRL-008 (change log audit)
- EAP-CTRL-010 (field-level protection check)
- EAP-CTRL-014 (bypass test suite)
- EAP-CTRL-019 (dual control configuration inspection)
