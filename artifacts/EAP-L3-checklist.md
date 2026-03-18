# EAP Control Checklist — EAP-L3

Generated from `catalogs/atal-eap-control-catalog.json` and `catalogs/assurance-level-overlays/EAP-L3-overlay.json`.

| Control ID | Title | Family | Applicable | Strength | Mandatory | Criticality | Status |
|---|---|---|:---:|:---:|:---:|:---:|:---:|
| EAP-CTRL-001 | Integrity-protected evidence chain | Evidence and Assurance | Yes | MUST | **Yes** | critical | — |
| EAP-CTRL-002 | Key custody and rotation | Evidence and Assurance | Yes | MUST | **Yes** | high | — |
| EAP-CTRL-003 | Verifier independence | Evidence and Assurance | Yes | MUST | **Yes** | high | — |
| EAP-CTRL-004 | Minimum event fields for evidence objects | Governance | Yes | MUST | **Yes** | high | — |
| EAP-CTRL-005 | Declared ordering model | Governance | Yes | MUST | **Yes** | high | — |
| EAP-CTRL-006 | Replay and duplication detection | Security | Yes | MUST | **Yes** | high | — |
| EAP-CTRL-007 | Controlled invocation surface | Enforcement | Yes | MUST | **Yes** | critical | — |
| EAP-CTRL-008 | Change control for enforcement layer | Enforcement | Yes | MUST | **Yes** | high | — |
| EAP-CTRL-009 | Threat model declaration | Governance | Yes | MUST | **Yes** | high | — |
| EAP-CTRL-010 | Field-level privacy protection | Security | Yes | MUST | **Yes** | high | — |
| EAP-CTRL-011 | Auditor access governance | Oversight | Yes | MUST | **Yes** | high | — |
| EAP-CTRL-012 | Retention-by-class policy | Governance | Yes | MUST | **Yes** | medium | — |
| EAP-CTRL-013 | Evidence store incident posture | Resilience | Yes | MUST | **Yes** | high | — |
| EAP-CTRL-014 | Bypass test suite | Forensics and Reconstruction | Yes | MUST | **Yes** | critical | — |
| EAP-CTRL-015 | Evidence reconstruction drill | Forensics and Reconstruction | Yes | MUST | **Yes** | high | — |
| EAP-CTRL-016 | Kill-switch test and dual-control enforcement | Resilience | Yes | MUST | **Yes** | critical | — |
| EAP-CTRL-017 | Operator-of-Record and Approver-of-Record role definitions | Oversight | Yes | MUST | **Yes** | high | — |
| EAP-CTRL-018 | Separation of duties | Oversight | Yes | MUST | **Yes** | high | — |
| EAP-CTRL-019 | Dual control for high-impact actions | Oversight | Yes | MUST | **Yes** | critical | — |
| EAP-CTRL-020 | Vendor and integration dependency documentation | Vendor and Integration | Yes | MUST | **Yes** | medium | — |

## Notes

- **EAP-CTRL-001**: External witnessing or anchoring for evidence chain heads strongly recommended.
- **EAP-CTRL-002**: Strict rotation schedule and documented compromise playbook required.
- **EAP-CTRL-003**: Independent verification tooling or documented process required.
- **EAP-CTRL-004**: Monotonic sequencing and cross-node ordering strategy required.
- **EAP-CTRL-005**: Declared cross-node ordering strategy required.
- **EAP-CTRL-006**: Replay detection must be demonstrated, not only documented.
- **EAP-CTRL-007**: Strict network policy; enforcement layer must be the only invocation path.
- **EAP-CTRL-009**: All four attacker class categories must be addressed.
- **EAP-CTRL-010**: Field-level encryption plus redaction-by-class required.
- **EAP-CTRL-011**: Audited evidence access with export controls required.
- **EAP-CTRL-012**: Retention policy must align to jurisdiction and criticality.
- **EAP-CTRL-014**: Quarterly adversarial bypass tests plus registry tampering simulations required.
- **EAP-CTRL-015**: Semi-annual drills; at least one must assume vendor tooling unavailable.
- **EAP-CTRL-016**: Dual-control enforced; live-fire exercise in controlled environment required.
- **EAP-CTRL-017**: Three-way role separation required.
- **EAP-CTRL-018**: Full three-way SoD required.
