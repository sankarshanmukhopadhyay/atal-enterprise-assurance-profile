# ATAL ↔ EAP Control Map (Draft)

This mapping helps reviewers and implementers see how EAP **derives from** and **operationalizes** ATAL.

| EAP Requirement | EAP Level | ATAL Concept(s) (high-level) | Enterprise intent |
|---|---:|---|---|
| EAP-CRYPTO-1 Signed evidence chain | L2+ | Evidence integrity; forensic bundle verifiability | Comparable evidence across vendors |
| EAP-CRYPTO-2 Key custody & rotation | L1+ | Integrity requirements; audit readiness | Avoid weak key practices |
| EAP-CRYPTO-3 Verifier independence | L1+ | “Verifiable without proprietary systems” | Auditor portability |
| EAP-TIME-1 Event fields | L2+ | Reconstructability; timestamps | Causality and ordering |
| EAP-TIME-2 Ordering model | L2+ | Decision trail reconstruction | Distributed audit correctness |
| EAP-NB-1 Controlled invocation surface | L1+ | Non-bypassability; gateways | Enforceability beyond process |
| EAP-NB-2 Change control | L1+ | Governance / certification readiness | Prevent silent drift |
| EAP-PRIV-2 Auditor access governance | L1+ | Audit interfaces; forensic bundles | Prevent evidence exfiltration |
| EAP-TEST-1 Bypass test suite | L2+ | Forbidden behaviors | Demonstrable effectiveness |
| EAP-TEST-2 Reconstruction drills | L2+ | Auditability | Proof under stress |
| EAP-ROLE-1 Separation of duties | L2+ | Operator/approvals concepts | Reduce rubber-stamping |
