# Next — Complete EAP-L3 High-Assurance / Adversarial Example

Use this example **after** completing the EAP-L2 learning path.

L2 teaches the tooling. L3 demonstrates the complete high-assurance/adversarial assurance system.

## Scenario

This synthetic critical-operations agent has safety and critical-operations impact. Those deployment characteristics deterministically require **EAP-L3 — High Assurance**.

Start with:

```text
deployment-profile.json
```

Then follow the same artifact separation used in L2, but with stronger evidence and adversarial expectations.

## Read the files in this order

| Order | File/directory | What it adds beyond L2 |
|---|---|---|
| 1 | `deployment-profile.json` | L3-triggering safety/critical impact |
| 2 | `evidence-bundle.json` | evidence for all 20 mandatory L3 controls |
| 3 | `test-results/` | seven positive executable observations |
| 4 | `negative-fixtures/` | deliberate unsafe outcomes that must remain failures |
| 5 | `reference/` | machine-readable supporting evidence referenced by the bundle |
| 6 | `assessment-result.json` | complete L3 assessment |
| 7 | `../../artifacts/eap-l3-assurance-claim.json` | digest-bound L3 claim |
| 8 | `../../artifacts/eap-l3-assessor-handoff.json` | bounded independent-assessor handoff |
| 9 | `../../artifacts/eap-l3-handoff-verification.json` | successful independent verification evidence |
| 10 | `../../artifacts/eap-l3-handoff-tamper-verification.json` | expected rejection of tampered handoff |

## Run the L3 path

```bash
python scripts/derive_assurance_level.py \
  examples/eap-l3-worked-example/deployment-profile.json

python scripts/validate_l3_worked_example.py

python scripts/check_required_controls.py \
  --level EAP-L3 \
  --bundle examples/eap-l3-worked-example/evidence-bundle.json

python scripts/check_required_controls.py \
  --level EAP-L3 \
  --result examples/eap-l3-worked-example/assessment-result.json
```

The L3 validator also enforces E4-or-stronger executable evidence for designated critical controls.

## Study the executable test corpus

Compare the portable test definitions in `tests/catalog/` with the positive results under this example:

- evidence-chain tamper detection;
- replay rejection;
- independent reconstruction;
- dual-control enforcement;
- delegation-boundary enforcement;
- non-bypassability;
- kill-switch effectiveness.

The distinction to understand is:

```text
portable test definition
       ↓ executed against a system
machine-readable test result
       ↓ cited as evidence
control assessment
```

## Study negative evidence

Open `negative-fixtures/`.

These files are intentionally valid result artifacts that describe **unsafe behavior**. They should remain `fail` outcomes. This is different from a malformed artifact:

```text
schema-invalid artifact
       ≠
valid artifact recording a failed safety/control test
```

That distinction is central to adversarial assurance.

## Build the claim and independent handoff

```bash
python scripts/build_l3_assurance_claim.py
python scripts/build_assessor_handoff.py
python scripts/verify_assessor_handoff.py --tamper-self-test
```

Inspect:

```text
artifacts/eap-l3-assurance-claim.json
artifacts/eap-l3-assessor-handoff.json
artifacts/eap-l3-handoff-verification.json
artifacts/eap-l3-handoff-tamper-verification.json
```

The handoff digest-binds the declared source set so a separate verifier can detect missing or altered evidence without relying on undocumented repository state.

## What independent verification does — and does not do

The verifier can check integrity, completeness, profile/version, subject, authorities, expiry, revocation, and declared source digests.

It does **not**:

- certify the deployment;
- establish that every underlying evidence statement is true;
- inherit Assessment Authority;
- accept enterprise risk;
- grant regulatory status.

## Complete repository run

```bash
python scripts/run_quality_gate.py --mode all
```

For the first-use walkthrough and L2 progression, see [`../../docs/getting-started.md`](../../docs/getting-started.md).
