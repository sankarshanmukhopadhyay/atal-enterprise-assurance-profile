# ATAL Enterprise Assurance Profile (EAP)

[![Upstream: ATAL Standard](https://img.shields.io/badge/upstream-ATAL%20Standard-2ea44f)](https://github.com/Elytra-Security/atal-standard)
[![Version](https://img.shields.io/badge/version-0.3.0-blue.svg)](./changelog/CHANGELOG.md)
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

## v0.3.0 — Operational Integrity and Quality Gates

v0.3.0 hardens this repository as a **self-checking, release-ready assurance toolkit**. New in this release:

- **Repository quality gate** — canonical validation and artifact regeneration entrypoint via `scripts/run_quality_gate.py` and `make validate|build|all`
- **Semantic integrity validation** — cross-artifact checks for catalog, overlays, dependency rules, mandatory control applicability, sample coverage, and JSON/YAML equivalence via `scripts/validate_repo_integrity.py`
- **CI automation** — GitHub Actions workflow in `.github/workflows/validate.yml` that installs dependencies and runs the full quality gate on pushes and pull requests
- **Dependency pinning** — `requirements.txt` for reproducible local and CI execution
- **Maintainer guidance** — refreshed README and CLI usage, plus a release checklist for maintainers in `docs/maintainer-release-checklist.md`
- **Regenerated artifacts** — checklists, traceability outputs, assessment report, and exports refreshed under `artifacts/` against the v0.3.0 catalog and overlays

---

## Quickstart

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the full repository quality gate:

```bash
python scripts/run_quality_gate.py --mode all
```

Or use the Make targets:

```bash
make validate
make build
make all
```

This validates the catalog in JSON and YAML form, runs semantic repository integrity checks, verifies the sample evidence bundle and assessment result, checks mandatory controls, and regenerates all checked-in outputs in `artifacts/`. See `docs/cli-usage.md` for the full command reference.

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

Draft. Intended for peer review and iteration against ATAL releases. v0.3.0 adds repository integrity checks, CI quality gates, and a reproducible maintainer workflow.

## License

See `LICENSE.md`.
