# CLI Usage

All scripts are in `scripts/`. They require Python 3.10+ and the following packages:

```bash
pip install jsonschema pyyaml openpyxl
```

No other dependencies are required for core validation and report generation.

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

## End-to-end EAP-L1 sample run

The following sequence exercises the complete EAP-L1 sample path:

```bash
# 1. Validate the catalog
python scripts/validate_catalog.py catalogs/atal-eap-control-catalog.json

# 2. Generate the L1 checklist
python scripts/generate_profile_checklist.py --level EAP-L1

# 3. Validate the sample evidence bundle
python scripts/validate_evidence_bundle.py evidence/samples/eap-l1-sample-evidence-bundle.json

# 4. Check required controls
python scripts/check_required_controls.py \
  --level EAP-L1 \
  --bundle evidence/samples/eap-l1-sample-evidence-bundle.json

# 5. Validate the sample assessment result
python scripts/validate_assessment_result.py assessments/samples/eap-l1-sample-assessment.json

# 6. Compile the assessment report
python scripts/compile_assessment_report.py \
  --level EAP-L1 \
  --bundle evidence/samples/eap-l1-sample-evidence-bundle.json \
  --result assessments/samples/eap-l1-sample-assessment.json

# 7. Build the traceability matrix
python scripts/build_traceability_matrix.py

# 8. Export catalog to XLSX
python scripts/export_csv_xlsx.py --source catalog
```

All outputs are written to `artifacts/`.
