# EAP Traceability Matrix

Generated from `catalogs/atal-eap-control-catalog.json` (v0.2.0).

| Control ID | Title | Family | Levels | Strength | ATAL References | Repo Sources |
|---|---|---|:---:|:---:|---|---|
| EAP-CTRL-001 | Integrity-protected evidence chain | Evidence and Assurance | EAP-L1, EAP-L2, EAP-L3 | MUST | Evidence integrity; Forensic bundle verifiability | normative/evidence-integrity.md#EAP-CRYPTO-1; mappings/atal-eap-control-map.md |
| EAP-CTRL-002 | Key custody and rotation | Evidence and Assurance | EAP-L1, EAP-L2, EAP-L3 | MUST | Integrity requirements; Audit readiness | normative/evidence-integrity.md#EAP-CRYPTO-2; mappings/atal-eap-control-map.md |
| EAP-CTRL-003 | Verifier independence | Evidence and Assurance | EAP-L1, EAP-L2, EAP-L3 | MUST | Verifiable without proprietary systems; Auditor portability | normative/evidence-integrity.md#EAP-CRYPTO-3; mappings/atal-eap-control-map.md |
| EAP-CTRL-004 | Minimum event fields for evidence objects | Governance | EAP-L1, EAP-L2, EAP-L3 | MUST | Reconstructability; Timestamps | normative/time-and-ordering.md#EAP-TIME-1; mappings/atal-eap-control-map.md |
| EAP-CTRL-005 | Declared ordering model | Governance | EAP-L2, EAP-L3 | MUST | Decision trail reconstruction | normative/time-and-ordering.md#EAP-TIME-2; examples/ordering-models/ |
| EAP-CTRL-006 | Replay and duplication detection | Security | EAP-L2, EAP-L3 | MUST | Reconstructability | normative/time-and-ordering.md#EAP-TIME-3 |
| EAP-CTRL-007 | Controlled invocation surface | Enforcement | EAP-L1, EAP-L2, EAP-L3 | MUST | Non-bypassability; Gateways | normative/non-bypassability.md#EAP-NB-1; test-harness/bypass-tests.md |
| EAP-CTRL-008 | Change control for enforcement layer | Enforcement | EAP-L1, EAP-L2, EAP-L3 | MUST | Governance / certification readiness | normative/non-bypassability.md#EAP-NB-2; mappings/atal-eap-control-map.md |
| EAP-CTRL-009 | Threat model declaration | Governance | EAP-L3 | MUST | Non-bypassability | normative/non-bypassability.md#EAP-NB-3 |
| EAP-CTRL-010 | Field-level privacy protection | Security | EAP-L1, EAP-L2, EAP-L3 | MUST | Logging; Privacy | normative/privacy-and-retention.md#EAP-PRIV-1 |
| EAP-CTRL-011 | Auditor access governance | Oversight | EAP-L1, EAP-L2, EAP-L3 | MUST | Audit interfaces; Forensic bundles | normative/privacy-and-retention.md#EAP-PRIV-2; mappings/atal-eap-control-map.md |
| EAP-CTRL-012 | Retention-by-class policy | Governance | EAP-L1, EAP-L2, EAP-L3 | MUST | Audit readiness | normative/privacy-and-retention.md#EAP-PRIV-3 |
| EAP-CTRL-013 | Evidence store incident posture | Resilience | EAP-L3 | MUST | Audit readiness | normative/privacy-and-retention.md#EAP-PRIV-4 |
| EAP-CTRL-014 | Bypass test suite | Forensics and Reconstruction | EAP-L1, EAP-L2, EAP-L3 | MUST | Forbidden behaviors | test-harness/bypass-tests.md; normative/control-effectiveness.md#EAP-TEST-1 |
| EAP-CTRL-015 | Evidence reconstruction drill | Forensics and Reconstruction | EAP-L1, EAP-L2, EAP-L3 | MUST | Auditability | test-harness/reconstruction-drills.md; normative/control-effectiveness.md#EAP-TEST-2 |
| EAP-CTRL-016 | Kill-switch test and dual-control enforcement | Resilience | EAP-L2, EAP-L3 | MUST | Kill-switch | test-harness/kill-switch-tests.md; normative/control-effectiveness.md#EAP-TEST-3 |
| EAP-CTRL-017 | Operator-of-Record and Approver-of-Record role definitions | Oversight | EAP-L1, EAP-L2, EAP-L3 | MUST | Operator/approvals concepts | normative/roles-and-separation.md; examples/role-models/ |
| EAP-CTRL-018 | Separation of duties | Oversight | EAP-L2, EAP-L3 | MUST | Operator/approvals concepts | normative/roles-and-separation.md#EAP-ROLE-1; mappings/atal-eap-control-map.md |
| EAP-CTRL-019 | Dual control for high-impact actions | Oversight | EAP-L3 | MUST | Operator/approvals concepts | normative/roles-and-separation.md#EAP-ROLE-2 |
| EAP-CTRL-020 | Vendor and integration dependency documentation | Vendor and Integration | EAP-L2, EAP-L3 | MUST | Governance / certification readiness | UPSTREAM.md; COMPATIBILITY.md |

## Risk and Compensating Control Cross-Reference

| Control ID | Related Risks | Compensating Controls | Automation Candidate |
|---|---|---|:---:|
| EAP-CTRL-001 | Evidence tampering; Audit evidence repudiation; Chain replay | EAP-CTRL-002, EAP-CTRL-003 | True |
| EAP-CTRL-002 | Key compromise; Evidence repudiation; Audit trail invalidation |  | False |
| EAP-CTRL-003 | Auditor lock-in; Verification failure under vendor unavailability |  | False |
| EAP-CTRL-004 | Ordering ambiguity; Causal reconstruction failure; Audit gap | EAP-CTRL-005 | True |
| EAP-CTRL-005 | Distributed ordering failure; Partition-induced audit gaps |  | False |
| EAP-CTRL-006 | Evidence replay attack; Audit corruption | EAP-CTRL-001 | True |
| EAP-CTRL-007 | Direct endpoint bypass; Gateway circumvention; Policy evasion | EAP-CTRL-008 | True |
| EAP-CTRL-008 | Silent policy drift; Unauthorized gateway modification |  | True |
| EAP-CTRL-009 | Unmodeled threat vectors; Non-bypassability claim failure |  | False |
| EAP-CTRL-010 | Evidence store data breach; Sensitive data exposure to auditors | EAP-CTRL-011 | True |
| EAP-CTRL-011 | Evidence exfiltration; Auditor role abuse |  | False |
| EAP-CTRL-012 | Evidence prematurely deleted; Excessive sensitive data retention |  | False |
| EAP-CTRL-013 | Evidence store breach; Audit record destruction | EAP-CTRL-011 | False |
| EAP-CTRL-014 | Undetected bypass; Control degradation over time | EAP-CTRL-007, EAP-CTRL-008 | True |
| EAP-CTRL-015 | Evidence system failure discovered only in real incident | EAP-CTRL-001, EAP-CTRL-003 | False |
| EAP-CTRL-016 | Kill-switch failure during incident; Unauthorized kill-switch invocation | EAP-CTRL-018 | False |
| EAP-CTRL-017 | Accountability gap; Unowned high-impact action |  | False |
| EAP-CTRL-018 | Rubber-stamp approval; Insider policy manipulation |  | False |
| EAP-CTRL-019 | Unilateral kill-switch invocation; Unilateral policy change | EAP-CTRL-018 | True |
| EAP-CTRL-020 | Supply chain compromise; Undocumented integration bypass surface | EAP-CTRL-008 | False |
