# EAP Control Checklist — EAP-L1

Generated from `catalogs/atal-eap-control-catalog.json` and `catalogs/assurance-level-overlays/EAP-L1-overlay.json`.

| Control ID | Title | Family | Applicable | Strength | Mandatory | Criticality | Status |
|---|---|---|:---:|:---:|:---:|:---:|:---:|
| EAP-CTRL-001 | Integrity-protected evidence chain | Evidence and Assurance | Yes | MUST | **Yes** | critical | — |
| EAP-CTRL-002 | Key custody and rotation | Evidence and Assurance | Yes | MUST | **Yes** | high | — |
| EAP-CTRL-003 | Verifier independence | Evidence and Assurance | Yes | MUST | **Yes** | high | — |
| EAP-CTRL-004 | Minimum event fields for evidence objects | Governance | Yes | SHOULD | No | high | — |
| EAP-CTRL-005 | Declared ordering model | Governance | No | N/A | No | high | — |
| EAP-CTRL-006 | Replay and duplication detection | Security | No | N/A | No | high | — |
| EAP-CTRL-007 | Controlled invocation surface | Enforcement | Yes | MUST | **Yes** | critical | — |
| EAP-CTRL-008 | Change control for enforcement layer | Enforcement | Yes | MUST | **Yes** | high | — |
| EAP-CTRL-009 | Threat model declaration | Governance | No | N/A | No | high | — |
| EAP-CTRL-010 | Field-level privacy protection | Security | Yes | SHOULD | No | high | — |
| EAP-CTRL-011 | Auditor access governance | Oversight | Yes | MUST | **Yes** | high | — |
| EAP-CTRL-012 | Retention-by-class policy | Governance | Yes | SHOULD | No | medium | — |
| EAP-CTRL-013 | Evidence store incident posture | Resilience | No | N/A | No | high | — |
| EAP-CTRL-014 | Bypass test suite | Forensics and Reconstruction | Yes | SHOULD | No | critical | — |
| EAP-CTRL-015 | Evidence reconstruction drill | Forensics and Reconstruction | Yes | SHOULD | No | high | — |
| EAP-CTRL-016 | Kill-switch test and dual-control enforcement | Resilience | No | N/A | No | critical | — |
| EAP-CTRL-017 | Operator-of-Record and Approver-of-Record role definitions | Oversight | Yes | MUST | **Yes** | high | — |
| EAP-CTRL-018 | Separation of duties | Oversight | Yes | SHOULD | No | high | — |
| EAP-CTRL-019 | Dual control for high-impact actions | Oversight | No | N/A | No | critical | — |
| EAP-CTRL-020 | Vendor and integration dependency documentation | Vendor and Integration | No | N/A | No | medium | — |

## Notes

- **EAP-CTRL-001**: Simplified chain acceptable at L1. Full append-only hash-chained log required at L2+.
- **EAP-CTRL-004**: SHOULD at L1; MUST at L2+.
- **EAP-CTRL-005**: Not applicable at L1.
- **EAP-CTRL-006**: Not applicable at L1.
- **EAP-CTRL-009**: Not applicable at L1.
- **EAP-CTRL-010**: SHOULD at L1; MUST at L2+.
- **EAP-CTRL-012**: SHOULD at L1; MUST at L2+.
- **EAP-CTRL-013**: Not applicable at L1.
- **EAP-CTRL-014**: SHOULD at L1; MUST at L2+.
- **EAP-CTRL-015**: Annually recommended at L1. At least twice yearly mandatory at L2+.
- **EAP-CTRL-016**: Not applicable at L1.
- **EAP-CTRL-018**: Basic SoD between Policy Owner and Evidence Custodian recommended at L1; MUST at L2+.
- **EAP-CTRL-019**: Not applicable at L1.
- **EAP-CTRL-020**: Not applicable at L1.
