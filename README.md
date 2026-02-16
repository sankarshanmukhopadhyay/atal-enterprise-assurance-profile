# ATAL Enterprise Assurance Profile (EAP)

[![Upstream: ATAL Standard](https://img.shields.io/badge/upstream-ATAL%20Standard-2ea44f)](https://github.com/Elytra-Security/atal-standard)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](./LICENSE.md)
[![Docs](https://img.shields.io/badge/docs-markdown-informational.svg)](./README.md)

## Relationship to ATAL

This repository is an **Enterprise Assurance Profile (EAP)** that *profiles and extends* the upstream **ATAL Standard**.  
It is designed to give verifiers and implementers predictable, enterprise-friendly assurance requirements, mappings, and test guidance without forking the upstream standard’s intent.

**Upstream project:** https://github.com/Elytra-Security/atal-standard

### Upstream version pinning

This EAP is intended to track ATAL releases. When publishing, pin to an upstream tag/commit and record it in [`UPSTREAM.md`](./UPSTREAM.md).



This repository provides a **normative Enterprise Assurance Profile (EAP)** intended to be used **alongside** the ATAL specification.

**What this is**
- An **assurance addendum** that constrains and operationalizes ATAL for enterprise deployments (multi-team, multi-vendor, cloud-native, audit-driven).
- A set of **profiles (EAP-L1/L2/L3)**, **normative requirements**, **mappings** back to ATAL, and a **test harness** description.

**What this is not**
- Not a fork of ATAL.
- Not an implementation.
- Not a replacement standard.

## Quick links

- Enterprise profiles: [`profiles/enterprise/`](./profiles/enterprise/)
- Normative requirements: [`normative/`](./normative/)
- Mappings and traceability: [`mappings/`](./mappings/)
- Test harness: [`test-harness/`](./test-harness/)


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



## Upstream Reference

This Enterprise Assurance Profile (EAP) extends and profiles the ATAL Standard.
Upstream project reference:

ATAL Standard Repository:
https://github.com/Elytra-Security/atal-standard

This repository provides enterprise-oriented assurance overlays, mappings, and control refinements aligned to the upstream ATAL specification.
