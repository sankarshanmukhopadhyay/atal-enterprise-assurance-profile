# EAP Control Checklist — EAP-L2

Generated from `catalogs/atal-eap-control-catalog.json` and `catalogs/assurance-level-overlays/EAP-L2-overlay.json`.

| Control ID | Title | Family | Applicable | Strength | Mandatory | Criticality | Status |
|---|---|---|:---:|:---:|:---:|:---:|:---:|
| EAP-CTRL-001 | Integrity-protected evidence chain | Evidence and Assurance | Yes | MUST | **Yes** | critical | — |
| EAP-CTRL-002 | Key custody and rotation | Evidence and Assurance | Yes | MUST | **Yes** | high | — |
| EAP-CTRL-003 | Verifier independence | Evidence and Assurance | Yes | MUST | **Yes** | high | — |
| EAP-CTRL-004 | Minimum event fields for evidence objects | Governance | Yes | MUST | **Yes** | high | — |
| EAP-CTRL-005 | Declared ordering model | Governance | Yes | MUST | **Yes** | high | — |
| EAP-CTRL-006 | Replay and duplication detection | Security | Yes | SHOULD | No | high | — |
| EAP-CTRL-007 | Controlled invocation surface | Enforcement | Yes | MUST | **Yes** | critical | — |
| EAP-CTRL-008 | Change control for enforcement layer | Enforcement | Yes | MUST | **Yes** | high | — |
| EAP-CTRL-009 | Threat model declaration | Governance | No | N/A | No | high | — |
| EAP-CTRL-010 | Field-level privacy protection | Security | Yes | MUST | **Yes** | high | — |
| EAP-CTRL-011 | Auditor access governance | Oversight | Yes | MUST | **Yes** | high | — |
| EAP-CTRL-012 | Retention-by-class policy | Governance | Yes | MUST | **Yes** | medium | — |
| EAP-CTRL-013 | Evidence store incident posture | Resilience | No | N/A | No | high | — |
| EAP-CTRL-014 | Bypass test suite | Forensics and Reconstruction | Yes | MUST | **Yes** | critical | — |
| EAP-CTRL-015 | Evidence reconstruction drill | Forensics and Reconstruction | Yes | MUST | **Yes** | high | — |
| EAP-CTRL-016 | Kill-switch test and dual-control enforcement | Resilience | Yes | MUST | **Yes** | critical | — |
| EAP-CTRL-017 | Operator-of-Record and Approver-of-Record role definitions | Oversight | Yes | MUST | **Yes** | high | — |
| EAP-CTRL-018 | Separation of duties | Oversight | Yes | MUST | **Yes** | high | — |
| EAP-CTRL-019 | Dual control for high-impact actions | Oversight | No | N/A | No | critical | — |
| EAP-CTRL-020 | Vendor and integration dependency documentation | Vendor and Integration | Yes | MUST | **Yes** | medium | — |

## Notes

- **EAP-CTRL-001**: Full append-only hash-chained log with signed bundle manifests required at L2.
- **EAP-CTRL-002**: KMS/HSM custody + documented rotation and compromise procedure required.
- **EAP-CTRL-003**: Vendor-independent verification steps must be documented.
- **EAP-CTRL-004**: All four required event fields must be present.
- **EAP-CTRL-006**: SHOULD at L2; MUST at L3.
- **EAP-CTRL-007**: Network-level and identity-level controls both required.
- **EAP-CTRL-008**: Change control on gateways, registries, evaluators, and safety kernel configs.
- **EAP-CTRL-009**: Not applicable at L2.
- **EAP-CTRL-010**: Field-level encryption or structured redaction required.
- **EAP-CTRL-011**: Time-boxed auditor sessions and controlled export required.
- **EAP-CTRL-012**: Retention-by-risk-class policy required.
- **EAP-CTRL-013**: Not applicable at L2.
- **EAP-CTRL-014**: Quarterly bypass test suite required.
- **EAP-CTRL-015**: Reconstruction drill every 6 months required.
- **EAP-CTRL-016**: Kill-switch tabletop plus controlled exercise annually.
- **EAP-CTRL-017**: Approver-of-Record and Evidence Custodian role definitions required.
- **EAP-CTRL-018**: OOR and AOR must be distinct identities for higher-risk actions.
- **EAP-CTRL-019**: Not applicable at L2.
