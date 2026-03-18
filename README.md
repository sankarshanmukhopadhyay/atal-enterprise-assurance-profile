# ATAL Enterprise Assurance Profile (EAP)

[![Upstream: ATAL Standard](https://img.shields.io/badge/upstream-ATAL%20Standard-2ea44f)](https://github.com/Elytra-Security/atal-standard)
[![Version](https://img.shields.io/badge/version-0.2.0-blue.svg)](./changelog/CHANGELOG.md)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](./LICENSE.md)
[![Status](https://img.shields.io/badge/status-draft-yellow.svg)](./README.md)

## What this is

This repository is an **Enterprise Assurance Profile (EAP)** that profiles and operationalizes the upstream [ATAL Standard](https://github.com/Elytra-Security/atal-standard) for enterprise deployments. It is designed for multi-team, multi-vendor, audit-driven environments where ATAL controls must be verifiable, portable, and repeatable.

**What this is:**
- A canonical machine-readable control catalog derived from ATAL
- Three assurance levels (EAP-L1/L2/L3) with machine-readable overlays
- JSON Schemas for all core assurance artifacts
- Evidence and assessment templates for practical use
- Script-based tooling for validation, checklist generation, coverage checks, reporting, and export
- A complete EAP-L1 worked example

**What this is not:**
- Not a fork of ATAL
- Not a runtime enforcement engine
- Not a replacement for upstream ATAL semantics

---

## Assurance levels

| Level | Name | Intended use |
|---|---|---|
| **EAP-L1** | Enterprise Baseline | Internal copilots, low-to-medium impact, audit-required |
| **EAP-L2** | Controlled Autonomy | Tool-using agents, persistent memory, production workflows |
| **EAP-L3** | High Assurance | Safety, security, financial, critical operations |

---

## v0.2.0 — Operational Assurance Core

v0.2.0 transforms this repository from a descriptive assurance profile into a **portable operational assurance pack**. New in this release:

- **Control catalog** — 20 controls across 8 families, seeded from existing normative and test-harness material (`catalogs/`)
- **Assurance-level overlays** — machine-readable applicability, strength tightening, and dependency rules per level (`catalogs/assurance-level-overlays/`)
- **JSON Schemas** — for control catalog, assurance profile, evidence bundle, assessment result, deployment context, and exception waiver (`schemas/`)
- **Evidence and assessment templates** — ready-to-use starting points for evidence collection and assessment (`evidence/templates/`, `assessments/templates/`)
- **EAP-L1 worked example** — complete end-to-end sample demonstrating deployment context, evidence bundle, assessment result, and compiled report (`evidence/samples/`, `assessments/samples/`, `examples/eap-l1-worked-example/`)
- **Script tooling** — 8 scripts for validation, checklist generation, coverage checking, report compilation, traceability generation, and export (`scripts/`)
- **Documentation refresh** — operational model, artifact model, catalog design guide, and CLI usage reference (`docs/`)

---

## Quickstart

Install dependencies:

```bash
pip install jsonschema pyyaml openpyxl
```

Run the complete EAP-L1 sample path:

```bash
# Validate the catalog
python scripts/validate_catalog.py catalogs/atal-eap-control-catalog.json

# Generate the L1 checklist
python scripts/generate_profile_checklist.py --level EAP-L1

# Validate the sample evidence bundle
python scripts/validate_evidence_bundle.py evidence/samples/eap-l1-sample-evidence-bundle.json

# Check all mandatory controls are covered
python scripts/check_required_controls.py \
  --level EAP-L1 \
  --bundle evidence/samples/eap-l1-sample-evidence-bundle.json

# Compile the assessment report
python scripts/compile_assessment_report.py \
  --level EAP-L1 \
  --bundle evidence/samples/eap-l1-sample-evidence-bundle.json \
  --result assessments/samples/eap-l1-sample-assessment.json

# Export the catalog to XLSX
python scripts/export_csv_xlsx.py --source catalog
```

All generated outputs land in `artifacts/`. See `docs/cli-usage.md` for the full command reference.

---

## Repository map

```
catalogs/                        Control catalog (JSON + YAML) and assurance-level overlays
docs/                            Operational model, artifact model, catalog design, CLI usage
evidence/
  templates/                     Evidence bundle, control evidence item, and waiver templates
  samples/                       EAP-L1 sample evidence bundle
assessments/
  templates/                     Assessment result template
  samples/                       EAP-L1 sample assessment result
schemas/                         JSON Schemas for all core artifacts
scripts/                         Validation, checklist, coverage, report, traceability, export scripts
examples/
  eap-l1-worked-example/         Complete EAP-L1 sample path (deployment context + artifacts)
  ordering-models/               Centralized and hybrid ordering model examples
  role-models/                   Enterprise role model examples
  sample-forensic-bundle/        Legacy sample forensic bundle (v0.1.0)
profiles/enterprise/             Human-readable EAP profile and level checklists (v0.1.0)
normative/                       Normative requirement documents by control family
mappings/                        ATAL to EAP traceability and control mapping (MD + CSV)
test-harness/                    Required test activity descriptions (bypass, reconstruction, kill-switch)
artifacts/                       Generated outputs (checklists, reports, traceability matrix, exports)
changelog/                       Version history
```

---

## How to run an assessment

1. **Select a level** — Pick EAP-L1, EAP-L2, or EAP-L3 based on your deployment context.
2. **Generate a checklist** — `python scripts/generate_profile_checklist.py --level <LEVEL>`
3. **Collect evidence** — Use templates in `evidence/templates/` to build your evidence bundle.
4. **Validate evidence** — `python scripts/validate_evidence_bundle.py <bundle>`
5. **Assess controls** — Populate an assessment result using `assessments/templates/assessment-result.template.json`.
6. **Compile report** — `python scripts/compile_assessment_report.py --level <LEVEL> --bundle <bundle> --result <result>`
7. **Record waivers** — For any `fail` or `waived` controls, create waiver records using `evidence/templates/waiver.template.json`.

See `docs/operational-model.md` for the full workflow description.

---

## Relationship to ATAL

This EAP is a conformance layer on top of ATAL, not a fork. Every control in the catalog traces back to at least one ATAL concept via `mapped_atal_references`. Upstream version pinning is recorded in [`UPSTREAM.md`](./UPSTREAM.md).

---

## Status

Draft. Intended for peer review and iteration against ATAL releases.

## License

See `LICENSE.md`.
