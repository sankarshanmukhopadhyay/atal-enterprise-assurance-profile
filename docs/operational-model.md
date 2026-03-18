# Operational Model

This document describes the end-to-end EAP assurance workflow introduced in v0.2.0.

## Overview

The EAP operational model is a portable, self-contained assurance workflow. It does not require a platform product, a SaaS tool, or vendor-specific infrastructure. It runs from the repository itself using lightweight Python scripts and machine-readable artifacts.

The workflow has seven steps.

---

## Step 1 — Select a profile

Choose an assurance level appropriate for the deployment:

| Level | Intended use |
|---|---|
| **EAP-L1** | Internal copilots, low-to-medium impact workflows, audit-required environments |
| **EAP-L2** | Tool-using agents, persistent memory, production autonomous workflows |
| **EAP-L3** | High-impact autonomy: safety, security, financial, critical operations |

The assurance level determines which controls are mandatory. See `catalogs/assurance-level-overlays/` for the machine-readable overlay per level.

---

## Step 2 — Generate a checklist

Use `scripts/generate_profile_checklist.py` to produce a control checklist for the selected level:

```bash
python scripts/generate_profile_checklist.py --level EAP-L1 --format all
```

This writes JSON, CSV, and Markdown checklists to `artifacts/`. The Markdown checklist is the working document for the assessment team.

---

## Step 3 — Collect evidence

For each applicable control in the checklist, gather evidence as specified in the `evidence_requirements` field of the catalog. Use the templates in `evidence/templates/` as a starting point:

- `evidence-bundle.template.json` — the container for all control evidence items
- `control-evidence-item.template.json` — a single control's evidence entry
- `waiver.template.json` — for controls that cannot be met

Populate one `control_evidence_item` entry per applicable control and assemble them into an evidence bundle.

Store evidence artifacts (logs, documents, test results, configurations) alongside or externally to the bundle and reference them by path or URL.

---

## Step 4 — Validate evidence

Validate the completed evidence bundle against its schema:

```bash
python scripts/validate_evidence_bundle.py evidence/<your-bundle>.json
```

Fix any schema validation errors before proceeding.

---

## Step 5 — Assess controls

Using the evidence bundle as input, evaluate each mandatory control against the pass criteria defined in the overlay. Populate an assessment result file using `assessments/templates/assessment-result.template.json`.

Valid status values are: `pass`, `fail`, `partial`, `not_applicable`, `waived`.

Check that all mandatory controls are passing:

```bash
python scripts/check_required_controls.py --level EAP-L1 --result <your-result>.json
```

---

## Step 6 — Compile report

Merge the profile overlay, evidence bundle, and assessment result into a human-readable Markdown report:

```bash
python scripts/compile_assessment_report.py \
  --level EAP-L1 \
  --bundle evidence/<your-bundle>.json \
  --result assessments/<your-result>.json
```

The report is written to `artifacts/`. Review it before sharing externally.

---

## Step 7 — Record waivers and remediation

For any controls that are `fail`, `partial`, or `waived`:

- Document the finding in the assessment result's `findings` array.
- If waived, create a waiver record using `evidence/templates/waiver.template.json` and reference it in the evidence bundle.
- Document residual risks in the `residual_risks` array of the assessment result.
- Record a remediation target date for each finding.

Waivers must be approved by an authorized role (Policy Owner or equivalent) and carry an expiry date to ensure they are reviewed periodically.

---

## Artifact relationships

See `docs/artifact-model.md` for a detailed description of how all artifacts relate to each other.
