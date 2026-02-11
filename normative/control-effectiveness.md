# Normative: Control Effectiveness Testing

## EAP-TEST-1 — Bypass test suite
**MUST L2+; SHOULD L1.**

A test suite MUST include attempts for:
- direct tool/API invocation bypass,
- undeclared memory persistence / side-channel state storage,
- unauthorized delegation / routing,
- tool registry tampering,
- evidence tampering and replay attempts.

## EAP-TEST-2 — Reconstruction drill
**MUST L2+; SHOULD L1.**

At least twice per year (L2+), an audit team MUST reconstruct a selected incident path using only recorded evidence.
One drill SHOULD assume “vendor tooling unavailable” (MUST for L3).

## EAP-TEST-3 — Kill-switch tabletop/live-fire (MUST L2+)
Kill-switch procedures MUST be tested periodically and evidence retained.
L3 MUST enforce dual-control and include at least one live-fire test in controlled conditions.
