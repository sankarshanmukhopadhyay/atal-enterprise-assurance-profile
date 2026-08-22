# Changelog

## 0.9.2 (2026-08-22)

Release theme: **L3 Adversarial Assurance**

### Added

- complete synthetic EAP-L3 high-assurance worked deployment under `examples/eap-l3-worked-example/`
- five new executable vectors for evidence integrity, replay rejection, independent reconstruction, dual control, and delegation boundaries
- positive L3 executable fixtures for the expanded test catalog plus existing non-bypassability and kill-switch vectors
- negative adversarial fixtures for undetected evidence tampering and improper single-approver execution
- `scripts/validate_l3_worked_example.py` with mandatory-control, test-binding, negative-fixture, derived-level, and E4+ critical-evidence enforcement
- `scripts/build_l3_assurance_claim.py` for deterministic digest-bound L3 claim generation

### Changed

- canonical quality gate now validates complete EAP-L3 evidence/assessment coverage and generates an L3 assessment report and assurance claim
- README, `PROJECT-STATUS.yaml`, and upstream EAP release version updated to v0.9.2

### Operational impact

v0.9.2 demonstrates that the reference assurance system can both accept valid high-assurance evidence and represent deliberately unsafe outcomes as explicit failures. Designated critical L3 controls require E4+ executable evidence before a conformant reference outcome is accepted.

---

## 0.9.1 (2026-08-22)

Release theme: **L2 Worked Assurance**

### Added

- complete synthetic EAP-L2 controlled-autonomy worked deployment under `examples/eap-l2-worked-example/`
- executable non-bypassability and kill-switch test results bound to L2 controls
- `scripts/validate_l2_worked_example.py` for cross-artifact L2 validation
- `scripts/build_l2_assurance_claim.py` for deterministic digest-bound claim generation

### Changed

- canonical quality gate now validates L2 mandatory-control coverage and executable test bindings
- build path now generates an L2 assessment report and assurance claim
- README, `PROJECT-STATUS.yaml`, and upstream EAP release version updated to v0.9.1

### Operational impact

v0.9.1 demonstrates a complete EAP-L2 flow from deployment declaration through evidence, executable tests, assessment, and bounded assurance claim. The worked case is synthetic reference evidence and is not an external certification.

---

## 0.9.0 (2026-08-22)

Release theme: **Assurance Candidate**

### Added

- `assurance/invariants.yaml` — cross-artifact invariants for provenance, mapping resolution, executable tests, claim lifecycle, evidence-strength progression, and quality-gate coverage
- `scripts/check_assurance_invariants.py` — fail-closed adversarial consistency checks

### Changed

- `scripts/run_quality_gate.py` now includes provenance, test-catalog, external-mapping, evidence-strength, and invariant validation
- `README.md` and `PROJECT-STATUS.yaml` now describe the repository as a pre-1.0 assurance candidate

### Operational impact

v0.9.0 consolidates the v0.4–v0.8 work into a candidate that can be pressure-tested as an executable assurance system. It remains explicitly non-certifying and requires broader L2/L3 implementation evidence before v1.0.

---

## 0.8.0 (2026-08-22)

Release theme: **Enterprise Interoperability**

### Added

- `mappings/external-framework-mappings.yaml` — typed and confidence-scored mappings to NIST AI RMF 1.0, ISO/IEC 42001:2023, ISO/IEC 23894:2023, and Regulation (EU) 2024/1689
- `schemas/external-framework-mapping.schema.json`
- `scripts/validate_external_mappings.py`

### Operational impact

External-framework mappings are now auditable evidence-routing assertions rather than unqualified equivalence claims.

---

## 0.7.0 (2026-08-22)

Release theme: **Executable Assurance**

### Added

- `schemas/test-case.schema.json`
- `schemas/test-result.schema.json`
- `tests/catalog/EAP-TEST-KS-001.yaml`
- `tests/catalog/EAP-TEST-NB-001.yaml`
- `scripts/validate_test_catalog.py`

### Operational impact

Selected controls now have adapter-neutral, machine-readable conformance vectors with explicit stimuli, observations, pass conditions, control bindings, and evidence-grade expectations.

---

## 0.6.0 (2026-08-22)

Release theme: **Evidence Strength**

### Added

- `evidence/evidence-strength-model.yaml` — E0–E5 evidence taxonomy with level-specific minimums and freshness expectations
- `scripts/grade_evidence_bundle.py` — evidence-strength report and optional strict enforcement

### Operational impact

A passing control can now be distinguished from a passing control supported by sufficiently strong evidence.

---

## 0.5.0 (2026-08-22)

Release theme: **Assurance Claims**

### Added

- `schemas/deployment-profile.schema.json`
- `schemas/assurance-claim.schema.json`
- `scripts/derive_assurance_level.py`
- `docs/assurance-claim-model.md`

### Operational impact

EAP assurance is now scoped to a declared deployment and explicit authority set. Claims support expiry and revocation, and minimum assurance level can be derived from deployment characteristics.

---

## 0.4.0 (2026-08-22)

Release theme: **Assurance Provenance**

### Added

- `upstream/atal-baseline.yaml` — exact ATAL v0.9 baseline pinned to commit `bafb65d716ddf71d2a90defbd4bfb5064c6aee0e`
- `schemas/upstream-baseline.schema.json`
- `scripts/check_upstream_integrity.py`

### Changed

- `UPSTREAM.md` replaced unresolved release placeholders with a concrete compatibility declaration
- `PROJECT-STATUS.yaml` now reports actual validation commands and evidence outputs

### Operational impact

A release is no longer complete while its upstream normative baseline is unresolved.

---

## 0.3.0 (2026-03-23)

Release theme: **Operational Integrity and Quality Gates**

### Added

- `requirements.txt` — canonical dependency file for local and CI execution
- `Makefile` — reproducible maintainer targets for `validate`, `build`, and `all`
- `.github/workflows/validate.yml` — GitHub Actions quality gate on push and pull request
- `scripts/validate_repo_integrity.py` — semantic repository integrity checks across catalog, overlays, dependency rules, and samples
- `scripts/run_quality_gate.py` — single entrypoint to run validation and artifact regeneration
- `docs/maintainer-release-checklist.md` — release hygiene and packaging checklist for maintainers

### Changed

- `README.md` — refreshed for the v0.3.0 quality-gate workflow and updated quickstart
- `docs/cli-usage.md` — documented the canonical quality gate, Make targets, and semantic integrity validator
- `catalogs/atal-eap-control-catalog.json` — version updated to `0.3.0`
- `catalogs/atal-eap-control-catalog.yaml` — regenerated from the canonical JSON catalog at `0.3.0`
- `catalogs/assurance-level-overlays/*.json` — version updated to `0.3.0`
- `artifacts/` — regenerated checklists, traceability matrix, assessment report, and CSV/XLSX exports through the new quality gate

### Operational impact

v0.3.0 turns the repository into a self-checking assurance toolkit. Future changes now have an explicit validation path, CI enforcement, semantic consistency checks, and a release-ready build routine.

---

## 0.2.0 (2026-03-18)

Release theme: **Operational Assurance Core**

### Added

**Canonical control catalog**
- `catalogs/atal-eap-control-catalog.json` — 20 controls across 8 families (Governance, Enforcement, Oversight, Security, Resilience, Forensics and Reconstruction, Vendor and Integration, Evidence and Assurance), seeded from existing normative, mapping, and test-harness material
- `catalogs/atal-eap-control-catalog.yaml` — YAML mirror of the catalog
- Stable control ID format: `EAP-CTRL-001` through `EAP-CTRL-020`

**Assurance-level overlays**
- `catalogs/assurance-level-overlays/EAP-L1-overlay.json`
- `catalogs/assurance-level-overlays/EAP-L2-overlay.json`
- `catalogs/assurance-level-overlays/EAP-L3-overlay.json`
- Each overlay defines applicable controls, normative strength overrides, evidence tightening, dependency rules, mandatory control ID lists, and pass criteria

**JSON Schemas**
- `schemas/control-catalog.schema.json`
- `schemas/assurance-profile.schema.json`
- `schemas/evidence-bundle.schema.json`
- `schemas/assessment-result.schema.json`
- `schemas/deployment-context.schema.json`
- `schemas/exception-waiver.schema.json`

**Evidence and assessment templates**
- `evidence/templates/evidence-bundle.template.json`
- `evidence/templates/control-evidence-item.template.json`
- `evidence/templates/waiver.template.json`
- `assessments/templates/assessment-result.template.json`

**EAP-L1 worked example**
- `examples/eap-l1-worked-example/deployment-context.json` — HR workflow assistant deployment context
- `evidence/samples/eap-l1-sample-evidence-bundle.json` — complete evidence bundle covering all 20 controls
- `assessments/samples/eap-l1-sample-assessment.json` — conformant assessment result for EAP-L1

**Script tooling**
- `scripts/validate_catalog.py` — validate catalog JSON or YAML against schema
- `scripts/validate_evidence_bundle.py` — validate evidence bundle against schema
- `scripts/validate_assessment_result.py` — validate assessment result against schema
- `scripts/generate_profile_checklist.py` — generate JSON, CSV, and Markdown checklists per level
- `scripts/check_required_controls.py` — check mandatory control coverage in bundle or result
- `scripts/compile_assessment_report.py` — compile Markdown assessment report from artifacts
- `scripts/build_traceability_matrix.py` — generate traceability matrix from control catalog
- `scripts/export_csv_xlsx.py` — export catalog or assessment summary to CSV and XLSX

**Documentation**
- `docs/operational-model.md` — end-to-end 7-step assurance workflow
- `docs/artifact-model.md` — how all artifacts relate and how to verify them independently
- `docs/catalog-design.md` — control ID format, family taxonomy, normative strength model, overlay design, traceability rules
- `docs/cli-usage.md` — usage examples for all 8 scripts including end-to-end EAP-L1 sample run

### Changed

- `README.md` — rewritten to reflect the v0.2.0 operational assurance pack positioning; added quickstart commands, repository map, and assessment workflow summary
- `UPSTREAM.md` — version pinning table preserved; no upstream version change in this release

### Preserved

All v0.1.0 material is preserved unchanged:
- `profiles/enterprise/` — human-readable EAP profile and L1/L2/L3 checklists
- `normative/` — normative requirement documents by control family
- `mappings/` — ATAL to EAP traceability and control mapping (MD + CSV)
- `test-harness/` — required test activity descriptions
- `examples/sample-forensic-bundle/` — v0.1.0 sample forensic bundle
- `examples/ordering-models/` — ordering model examples
- `examples/role-models/` — role model examples

---

## 0.1.0 (2026-02-11)

- Initial repository scaffold for ATAL Enterprise Assurance Profile (EAP)
- Added EAP umbrella profile + L1/L2/L3 checklists
- Added normative requirement families (integrity, ordering, non-bypassability, privacy, testing, roles)
- Added ATAL to EAP mapping and sample artifacts
