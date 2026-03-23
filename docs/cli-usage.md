# CLI Usage

All scripts are in `scripts/`. They require Python 3.10+ and the dependencies in `requirements.txt`:

```bash
pip install -r requirements.txt
```

## Canonical quality gate

Use the quality gate as the default maintainer path:

```bash
python scripts/run_quality_gate.py --mode validate
python scripts/run_quality_gate.py --mode build
python scripts/run_quality_gate.py --mode all
```

Equivalent Make targets:

```bash
make validate
make build
make all
```

- `validate` runs schema validation, semantic integrity checks, and mandatory control coverage checks
- `build` regenerates all checked-in generated artifacts under `artifacts/`
- `all` runs validation first and then regenerates artifacts

## Validate repository integrity

```bash
python scripts/validate_repo_integrity.py
```

This performs cross-artifact checks that schema validation alone cannot catch, including catalog JSON/YAML equivalence, duplicate IDs, overlay integrity, dependency rule validity, mandatory control applicability, and sample coverage alignment.

---

## Validate the control catalog

```bash
python scripts/validate_catalog.py catalogs/atal-eap-control-catalog.json
python scripts/validate_catalog.py catalogs/atal-eap-control-catalog.yaml
```

Exits 0 on success, 1 on validation failure, 2 on missing file or dependency.

---

## Generate a profile checklist

```bash
# All formats (JSON, CSV, Markdown) — default
python scripts/generate_profile_checklist.py --level EAP-L1

# Single format
python scripts/generate_profile_checklist.py --level EAP-L2 --format csv
python scripts/generate_profile_checklist.py --level EAP-L3 --format md
```

Output is written to `artifacts/`. The Markdown checklist is intended as the working document for the assessment team.

---

## Validate an evidence bundle

```bash
python scripts/validate_evidence_bundle.py evidence/samples/eap-l1-sample-evidence-bundle.json
python scripts/validate_evidence_bundle.py evidence/<your-bundle>.json
```

Exits 0 on success. Prints status counts per control on success.

---

## Validate an assessment result

```bash
python scripts/validate_assessment_result.py assessments/samples/eap-l1-sample-assessment.json
python scripts/validate_assessment_result.py assessments/<your-result>.json
```

Exits 0 on success. Prints control count, decision outcome, and finding count on success.

---

## Check required controls

```bash
# Check against an evidence bundle
python scripts/check_required_controls.py \
  --level EAP-L1 \
  --bundle evidence/samples/eap-l1-sample-evidence-bundle.json

# Check against an assessment result
python scripts/check_required_controls.py \
  --level EAP-L1 \
  --result assessments/samples/eap-l1-sample-assessment.json
```

Exits 0 if all mandatory controls are passing. Exits 1 if any mandatory controls are missing or failing.

---

## Compile an assessment report

```bash
python scripts/compile_assessment_report.py \
  --level EAP-L1 \
  --bundle evidence/samples/eap-l1-sample-evidence-bundle.json \
  --result assessments/samples/eap-l1-sample-assessment.json

# Optional: specify output path
python scripts/compile_assessment_report.py \
  --level EAP-L1 \
  --bundle evidence/samples/eap-l1-sample-evidence-bundle.json \
  --result assessments/samples/eap-l1-sample-assessment.json \
  --output artifacts/my-org-eap-l1-report.md
```

Default output: `artifacts/<level>-assessment-report.md`.

---

## Build the traceability matrix

```bash
# All formats (JSON, CSV, Markdown) — default
python scripts/build_traceability_matrix.py

# Single format
python scripts/build_traceability_matrix.py --format csv
python scripts/build_traceability_matrix.py --format md
```

Output is written to `artifacts/traceability-matrix.{json,csv,md}`.

---

## Export catalog or assessment to CSV/XLSX

```bash
# Export the full control catalog
python scripts/export_csv_xlsx.py --source catalog
python scripts/export_csv_xlsx.py --source catalog --format xlsx

# Export an assessment result summary
python scripts/export_csv_xlsx.py \
  --source assessment \
  --result assessments/samples/eap-l1-sample-assessment.json

python scripts/export_csv_xlsx.py \
  --source assessment \
  --result assessments/samples/eap-l1-sample-assessment.json \
  --format xlsx
```

Output is written to `artifacts/`.

---

## End-to-end repository run

The following command exercises the canonical validation and regeneration path:

```bash
python scripts/run_quality_gate.py --mode all
```

All outputs are written to `artifacts/`. For release hygiene, run this command before packaging a release or merging substantive catalog changes.
