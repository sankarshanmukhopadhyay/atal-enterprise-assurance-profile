# Changelog

## 0.9.5 (2026-08-23)

Release theme: **Governance Freeze**

### Added

- `assurance/governance-freeze.yaml` — machine-readable freeze of release-governance, authority, compatibility, and assurance-lifecycle surfaces
- `scripts/check_governance_freeze.py` — executable validation of the freeze and explicit v1 decision authority
- `docs/v1-migration-and-freeze.md` — migration expectations and v1 decision inputs

### Changed

- candidate-stable contracts advance to `frozen-for-v1-decision` without changing the declared contract members
- L2 and L3 claim/handoff builders derive the active repository version rather than embedding historical patch versions
- `GOVERNANCE.md` and `COMPATIBILITY.md` explicitly separate readiness evidence from authority to publish v1.0
- canonical quality gate validates the governance freeze before generating readiness evidence
- README, `PROJECT-STATUS.yaml`, and upstream EAP release version updated to v0.9.5

### Operational impact

v0.9.5 resolves the final blocking readiness criterion. A successful release must generate `ready_for_v1_decision` with zero blockers while preserving issue #12 as the mandatory explicit major-version decision gate.

---

## 0.9.4 (2026-08-23)

Release theme: **v1.0 Readiness Evidence**

### Added

- candidate-stable schema, identifier, claim-state, and test-result declarations
- compatibility enforcement and positive/negative core conformance fixtures
- blocking readiness criteria and deterministic JSON/Markdown readiness reports

### Operational impact

v0.9.4 made v1.0 readiness a fail-closed machine-verifiable property and intentionally reported `not_ready` while the final governance freeze remained outstanding.

---

## 0.9.3 (2026-08-23)

Release theme: **Reproducible Assessment**

### Added

- independent-assessor handoff schema and bounded digest-addressed source set
- deterministic handoff construction/verification and tamper-rejection evidence
- independent-assessor authority-boundary documentation

### Operational impact

v0.9.3 made a bounded EAP-L3 claim independently integrity-verifiable without undocumented repository state.

---

## 0.9.2 (2026-08-22)

Release theme: **L3 Adversarial Assurance**

### Added

- complete synthetic EAP-L3 worked deployment
- executable vectors for evidence integrity, replay, reconstruction, dual control, delegation boundaries, non-bypassability, and kill-switch behavior
- positive and negative adversarial fixtures
- E4+ executable evidence requirements for designated critical L3 controls

### Operational impact

v0.9.2 demonstrated both acceptance of valid high-assurance evidence and explicit failure representation for deliberately unsafe behavior.

---

## 0.9.1 (2026-08-22)

Release theme: **L2 Worked Assurance**

### Added

- complete synthetic EAP-L2 controlled-autonomy worked deployment
- executable non-bypassability and kill-switch results
- deterministic digest-bound L2 assurance claim and generated report

### Operational impact

v0.9.1 demonstrated a complete L2 deployment → evidence → executable test → assessment → claim path.

---

## 0.9.0 (2026-08-22)

Release theme: **Assurance Candidate**

### Added

- cross-artifact invariants for provenance, mappings, executable tests, claim lifecycle, evidence strength, and quality-gate coverage
- fail-closed adversarial consistency checks

### Operational impact

v0.9.0 consolidated the earlier work into a pre-v1 executable assurance candidate.

---

## 0.8.0 (2026-08-22)

Release theme: **Enterprise Interoperability**

- Added typed, confidence-scored mappings to NIST AI RMF 1.0, ISO/IEC 42001:2023, ISO/IEC 23894:2023, and Regulation (EU) 2024/1689.
- Mappings are evidence-routing assertions, not legal or normative equivalence claims.

---

## 0.7.0 (2026-08-22)

Release theme: **Executable Assurance**

- Added portable test-case/result schemas, kill-switch and non-bypassability test vectors, and executable-test catalog validation.

---

## 0.6.0 (2026-08-22)

Release theme: **Evidence Strength**

- Added E0–E5 evidence taxonomy, level-specific minimums, freshness expectations, and evidence-strength grading.

---

## 0.5.0 (2026-08-22)

Release theme: **Assurance Claims**

- Added deployment-profile and assurance-claim schemas, deterministic minimum-level derivation, explicit authority roles, expiry, and revocation semantics.

---

## 0.4.0 (2026-08-22)

Release theme: **Assurance Provenance**

- Added exact upstream ATAL baseline pinning, compatibility declaration, provenance validation, and concrete upstream release metadata.

---

## 0.3.0 (2026-03-23)

Release theme: **Operational Integrity and Quality Gates**

- Added canonical dependency/build entrypoints, GitHub Actions validation, repository integrity checks, and maintainer release hygiene.

---

## 0.2.0 (2026-03-18)

Release theme: **Operational Assurance Core**

- Added the 20-control canonical catalog, L1/L2/L3 overlays, core schemas, evidence/assessment templates, the initial L1 worked example, validation/reporting/export tooling, and operator documentation.

---

## 0.1.0 (2026-02-11)

- Initial repository scaffold for ATAL Enterprise Assurance Profile (EAP).
- Added enterprise profile/checklists, normative requirement families, ATAL mapping, test-harness material, and sample artifacts.
