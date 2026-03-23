# EAP Assessment Report — EAP-L1

**Assurance level:** EAP-L1  
**Assessment ID:** assess-eap-l1-sample-001  
**Assessment date:** 2026-03-18  
**Assessor:** Jordan Lee, Evidence Custodian  
**Report compiled:** 2026-03-23  

---

## System

| Field | Value |
|---|---|
| System name | Enterprise Copilot — Internal HR Workflow Assistant |
| Version | 2.1.4 |
| Environment | production |
| Assessment period | 2026-01-01 to 2026-03-15 |
| Attested by | Jordan Lee (Evidence Custodian) |

---

## Decision

**Outcome: CONFORMANT**

All mandatory EAP-L1 controls pass. All non-applicable controls are correctly marked per the EAP-L1-overlay. No findings, no waivers, no residual risks. The system is assessed as conformant with EAP-L1 (Enterprise Baseline).

**Valid until:** 2027-03-18

---

## Control Results

| Control ID | Title | Family | Mandatory | Result | Finding |
|---|---|---|:---:|:---:|---|
| EAP-CTRL-001 | Integrity-protected evidence chain | Evidence and Assurance | **Yes** | ✅ pass |  |
| EAP-CTRL-002 | Key custody and rotation | Evidence and Assurance | **Yes** | ✅ pass |  |
| EAP-CTRL-003 | Verifier independence | Evidence and Assurance | **Yes** | ✅ pass |  |
| EAP-CTRL-004 | Minimum event fields for evidence objects | Governance | No | ✅ pass |  |
| EAP-CTRL-005 | Declared ordering model | Governance | No | — not_applicable |  |
| EAP-CTRL-006 | Replay and duplication detection | Security | No | — not_applicable |  |
| EAP-CTRL-007 | Controlled invocation surface | Enforcement | **Yes** | ✅ pass |  |
| EAP-CTRL-008 | Change control for enforcement layer | Enforcement | **Yes** | ✅ pass |  |
| EAP-CTRL-009 | Threat model declaration | Governance | No | — not_applicable |  |
| EAP-CTRL-010 | Field-level privacy protection | Security | No | ✅ pass |  |
| EAP-CTRL-011 | Auditor access governance | Oversight | **Yes** | ✅ pass |  |
| EAP-CTRL-012 | Retention-by-class policy | Governance | No | ✅ pass |  |
| EAP-CTRL-013 | Evidence store incident posture | Resilience | No | — not_applicable |  |
| EAP-CTRL-014 | Bypass test suite | Forensics and Reconstruction | No | ✅ pass |  |
| EAP-CTRL-015 | Evidence reconstruction drill | Forensics and Reconstruction | No | ✅ pass |  |
| EAP-CTRL-016 | Kill-switch test and dual-control enforcement | Resilience | No | — not_applicable |  |
| EAP-CTRL-017 | Operator-of-Record and Approver-of-Record role definitions | Oversight | **Yes** | ✅ pass |  |
| EAP-CTRL-018 | Separation of duties | Oversight | No | ✅ pass |  |
| EAP-CTRL-019 | Dual control for high-impact actions | Oversight | No | — not_applicable |  |
| EAP-CTRL-020 | Vendor and integration dependency documentation | Vendor and Integration | No | — not_applicable |  |

**Summary:**

| Status | Count |
|---|:---:|
| pass | 13 |
| fail | 0 |
| partial | 0 |
| not_applicable | 7 |
| waived | 0 |

---

## Evidence References

### EAP-CTRL-001 — Integrity-protected evidence chain

- **ART-001-001**: Forensic bundle manifest with hashes for Q1 2026 evidence objects  
  `examples/eap-l1-worked-example/artifacts/q1-2026-bundle-manifest.json`
- **ART-001-002**: Tamper simulation test result — verification failure confirmed on modified artifact  
  `examples/eap-l1-worked-example/artifacts/tamper-sim-result.txt`

### EAP-CTRL-002 — Key custody and rotation

- **ART-002-001**: KMS configuration documentation excerpt showing key management policy  
  `examples/eap-l1-worked-example/artifacts/kms-config-summary.md`
- **ART-002-002**: Key rotation schedule and last rotation confirmation  
  `examples/eap-l1-worked-example/artifacts/key-rotation-log.txt`

### EAP-CTRL-003 — Verifier independence

- **ART-003-001**: Verification guide — docs/artifact-model.md section on independent verification  
  `docs/artifact-model.md`
- **ART-003-002**: Independent verification exercise completion record — 2026-02-20  
  `examples/eap-l1-worked-example/artifacts/independent-verify-record.md`

### EAP-CTRL-004 — Minimum event fields for evidence objects

- **ART-004-001**: Sample evidence object showing all four required fields  
  `examples/eap-l1-worked-example/artifacts/sample-evidence-object.json`

### EAP-CTRL-007 — Controlled invocation surface

- **ART-007-001**: Network policy configuration summary (sanitized for external review)  
  `examples/eap-l1-worked-example/artifacts/network-policy-summary.md`
- **ART-007-002**: Identity policy configuration documentation  
  `examples/eap-l1-worked-example/artifacts/identity-policy-summary.md`

### EAP-CTRL-008 — Change control for enforcement layer

- **ART-008-001**: Change log extract for enforcement layer Q1 2026 — 3 changes with review records  
  `examples/eap-l1-worked-example/artifacts/change-log-q1-2026.md`

### EAP-CTRL-010 — Field-level privacy protection

- **ART-010-001**: Sample evidence object showing redacted PII fields with integrity references  
  `examples/eap-l1-worked-example/artifacts/sample-evidence-object.json`

### EAP-CTRL-011 — Auditor access governance

- **ART-011-001**: Evidence access role definitions and access control policy  
  `examples/eap-l1-worked-example/artifacts/evidence-access-policy.md`
- **ART-011-002**: Sample access log showing time-bounded auditor session  
  `examples/eap-l1-worked-example/artifacts/access-log-sample.txt`

### EAP-CTRL-012 — Retention-by-class policy

- **ART-012-001**: Data retention policy document covering risk class, classification, and jurisdiction  
  `examples/eap-l1-worked-example/artifacts/retention-policy.md`

### EAP-CTRL-014 — Bypass test suite

- **ART-014-001**: Q1 2026 bypass test suite results — all scenarios pass  
  `examples/eap-l1-worked-example/artifacts/bypass-test-q1-2026.md`

### EAP-CTRL-015 — Evidence reconstruction drill

- **ART-015-001**: Reconstruction drill completion record — 2026-02-28  
  `examples/eap-l1-worked-example/artifacts/reconstruction-drill-record.md`

### EAP-CTRL-017 — Operator-of-Record and Approver-of-Record role definitions

- **ART-017-001**: Role definitions and current role assignment table  
  `examples/eap-l1-worked-example/artifacts/role-assignments.md`

### EAP-CTRL-018 — Separation of duties

- **ART-018-001**: SoD confirmation — role assignment review showing distinct identities  
  `examples/eap-l1-worked-example/artifacts/role-assignments.md`

---

*Report generated by `scripts/compile_assessment_report.py`. Review all referenced evidence artifacts before relying on this report for conformance decisions.*
