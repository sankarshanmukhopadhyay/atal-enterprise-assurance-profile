# ATAL Enterprise Assurance Profile (EAP)

This repository provides a **normative Enterprise Assurance Profile (EAP)** intended to be used **alongside** the ATAL specification.

**What this is**
- An **assurance addendum** that constrains and operationalizes ATAL for enterprise deployments (multi-team, multi-vendor, cloud-native, audit-driven).
- A set of **profiles (EAP-L1/L2/L3)**, **normative requirements**, **mappings** back to ATAL, and a **test harness** description.

**What this is not**
- Not a fork of ATAL.
- Not an implementation.
- Not a replacement standard.

## How to use
1. Pick a target assurance level:
   - **EAP-L1**: Enterprise Baseline
   - **EAP-L2**: Controlled Autonomy
   - **EAP-L3**: High Assurance
2. Apply the normative requirements in `normative/`.
3. Use the control mapping in `mappings/` to trace requirements back to ATAL.
4. Run the test activities described in `test-harness/` and retain evidence artifacts.

## Repository map
- `profiles/enterprise/` — The EAP addendum and level-specific checklists
- `normative/` — Normative requirements by control family
- `mappings/` — ATAL ↔ EAP traceability and control mapping (MD + CSV)
- `test-harness/` — Required test activities (bypass attempts, reconstruction drills, kill-switch exercises)
- `examples/` — Example artifacts (sample forensic bundle, ordering models, role models)
- `changelog/` — Version history

## Status
Draft. Intended for peer review and iteration against ATAL releases.

## License
See `LICENSE.md`.
