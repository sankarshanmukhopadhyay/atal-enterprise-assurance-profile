# Changelog

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
