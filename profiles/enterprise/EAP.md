# ATAL Enterprise Assurance Profile (EAP)

## 1. Scope and intent
The Enterprise Assurance Profile (EAP) defines **enterprise-grade assurance requirements** for deployments of ATAL in operational environments where:
- multiple teams and environments are involved,
- audit and incident response are mandatory,
- evidence must be portable across vendors and tools,
- non-bypassability must be enforceable beyond process controls.

EAP is designed to be **layered on top of ATAL**, not to replace it.

## 2. Assurance levels
EAP defines three assurance levels:

- **EAP-L1 (Enterprise Baseline)**  
  Suitable for internal copilots and low-to-medium impact workflows.

- **EAP-L2 (Controlled Autonomy)**  
  Suitable for tool-using agents, persistent memory, production workflows.

- **EAP-L3 (High Assurance)**  
  Suitable for high-impact autonomy (safety/security/financial), broad agentic orchestration, and environments requiring strong separation-of-duties and adversarial validation.

## 3. Normative language
- **MUST / SHALL**: mandatory requirements
- **SHOULD**: strongly recommended; deviations must be documented
- **MAY**: optional

## 4. Control families
EAP is organized into six control families:
1. Evidence Integrity
2. Time & Ordering
3. Non-bypassability & Enforcement Boundaries
4. Privacy, Minimization & Retention
5. Control Effectiveness Testing
6. Roles & Separation of Duties

Normative requirements live in `normative/` and are pulled into L1/L2/L3 checklists.

## 5. Conformance evidence
Conformance requires:
- meeting the applicable level checklist,
- producing required evidence artifacts,
- passing required test activities described in `test-harness/`.

## 6. Traceability
Traceability to ATAL is maintained in `mappings/`.
