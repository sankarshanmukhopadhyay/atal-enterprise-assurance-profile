# Normative: Time & Ordering

## EAP-TIME-1 — Minimum event fields
**MUST L2+; SHOULD L1.**

Evidence objects MUST include:
- `event_time` (wall clock),
- `monotonic_time` (node monotonic where available),
- `sequence_number` (per producer), and
- producer identity (workload identity / node identity / component identity).

## EAP-TIME-2 — Declared ordering model (MUST L2+)
Deployments MUST declare an ordering model:
- **Centralized ordering**, or
- **Hybrid ordering** (per-producer ordering with reconciliation rules).

Reconciliation rules MUST be documented and auditable (tie-break rules, clock tolerance, partition behavior).

## EAP-TIME-3 — Replay and duplication handling
**MUST L3; SHOULD L2.**
- Duplicate `record_id` or replayed evidence objects MUST be detectable.
- The system MUST define how replays are flagged and how investigations proceed.
