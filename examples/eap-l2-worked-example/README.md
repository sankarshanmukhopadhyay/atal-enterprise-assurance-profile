# Start Here — Complete EAP-L2 Worked Example

This directory is the **canonical learning path** for first-time EAP users.

Start with:

```text
deployment-profile.json
```

Do not begin with `evidence-bundle.json` or `assessment-result.json`. The deployment profile establishes what the system is, what it can do, what impact it can have, where it operates, and who holds system/assessment/risk authority.

## Scenario

The sample models a synthetic production purchasing agent with tool use, persistent memory, external side effects, financial impact, regulated-data handling, and a production environment. Those characteristics cause the minimum assurance level to derive as **EAP-L2 — Controlled Autonomy**.

The sample is reference evidence for the EAP method. It is not a claim about a live deployment and does not constitute certification.

## Read the files in this order

| Order | File | Question it answers |
|---|---|---|
| 1 | `deployment-profile.json` | What system/deployment are we assessing and who has authority? |
| 2 | `evidence-bundle.json` | What evidence supports the applicable controls? |
| 3 | `test-results/EAP-TEST-NB-001.json` | Did the non-bypassability behavior produce executable evidence? |
| 4 | `test-results/EAP-TEST-KS-001.json` | Did kill-switch behavior produce executable evidence? |
| 5 | `assessment-result.json` | What did the assessor conclude from the evidence? |
| 6 | `../../artifacts/eap-l2-assurance-claim.json` | What bounded assurance claim can be generated? |

## Run the example

From the repository root:

```bash
python scripts/derive_assurance_level.py \
  examples/eap-l2-worked-example/deployment-profile.json
```

Expected result: `EAP-L2` plus the deployment characteristics that caused the derivation.

Generate the L2 checklist:

```bash
python scripts/generate_profile_checklist.py --level EAP-L2 --format all
```

Check mandatory evidence coverage:

```bash
python scripts/check_required_controls.py \
  --level EAP-L2 \
  --bundle examples/eap-l2-worked-example/evidence-bundle.json
```

Validate the complete cross-artifact case:

```bash
python scripts/validate_l2_worked_example.py
```

Check the assessment:

```bash
python scripts/check_required_controls.py \
  --level EAP-L2 \
  --result examples/eap-l2-worked-example/assessment-result.json
```

Build the operator-readable report:

```bash
python scripts/compile_assessment_report.py \
  --level EAP-L2 \
  --bundle examples/eap-l2-worked-example/evidence-bundle.json \
  --result examples/eap-l2-worked-example/assessment-result.json
```

Build the assurance claim:

```bash
python scripts/build_l2_assurance_claim.py
```

Inspect:

```text
artifacts/EAP-L2-assessment-report.md
artifacts/eap-l2-assurance-claim.json
```

## What each transition means

```text
deployment declaration
       ↓ derives
minimum EAP level
       ↓ selects
mandatory controls
       ↓ require
structured + executable evidence
       ↓ evaluated by
assessment authority
       ↓ supports
bounded assurance claim
```

No transition silently grants the authority of the next one. Evidence does not decide assessment; assessment does not accept risk; a generated EAP claim does not grant regulatory approval.

## Break/fix exercise

To prove that the example is executable rather than illustrative only:

1. Save a copy of `evidence-bundle.json`.
2. Temporarily remove one mandatory control or change a mandatory control status from `pass` to `fail`.
3. Run `python scripts/validate_l2_worked_example.py`.
4. Confirm the validator rejects the modified case.
5. Restore the original file and confirm the validator passes again.

## Next step

After you understand this example, continue to:

```text
../eap-l3-worked-example/README.md
```

L3 adds stronger evidence floors, a broader executable test corpus, adversarial negative fixtures, independent-assessor handoffs, and tamper rejection.

For the full guided tutorial, see [`../../docs/getting-started.md`](../../docs/getting-started.md).
