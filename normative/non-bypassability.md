# Normative: Non-bypassability & Enforcement Boundaries

## EAP-NB-1 — Controlled invocation surface (MUST L1+)
Tool/API/memory/routing endpoints MUST be reachable only through the ATAL enforcement layer.
Any direct access path MUST be blocked using network and identity controls (not only application logic).

## EAP-NB-2 — Change control for enforcement layer (MUST L1+)
Changes to gateway policies, tool registries, envelope evaluators, routing rules, and safety kernel configurations MUST be:
- versioned,
- peer-reviewed, and
- recorded as governance events.

## EAP-NB-3 — Threat model declaration
**MUST L3; SHOULD L2.**

Deployments MUST declare:
- attacker classes considered (external, insider, compromised host, supply chain),
- assumptions and out-of-scope boundaries,
- mitigations required to sustain “non-bypassable” claims.
