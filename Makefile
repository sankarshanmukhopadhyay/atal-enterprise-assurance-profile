PYTHON ?= python3

.PHONY: install validate build all clean

install:
	$(PYTHON) -m pip install -r requirements.txt

validate:
	$(PYTHON) scripts/run_quality_gate.py --mode validate

build:
	$(PYTHON) scripts/run_quality_gate.py --mode build

all:
	$(PYTHON) scripts/run_quality_gate.py --mode all

clean:
	rm -f artifacts/EAP-L1-checklist.json artifacts/EAP-L1-checklist.csv artifacts/EAP-L1-checklist.md
	rm -f artifacts/EAP-L2-checklist.json artifacts/EAP-L2-checklist.csv artifacts/EAP-L2-checklist.md
	rm -f artifacts/EAP-L3-checklist.json artifacts/EAP-L3-checklist.csv artifacts/EAP-L3-checklist.md
	rm -f artifacts/traceability-matrix.json artifacts/traceability-matrix.csv artifacts/traceability-matrix.md
	rm -f artifacts/eap-control-catalog-export.csv artifacts/eap-control-catalog-export.xlsx
	rm -f artifacts/assess-eap-l1-sample-001-export.csv artifacts/assess-eap-l1-sample-001-export.xlsx
	rm -f artifacts/EAP-L1-assessment-report.md
