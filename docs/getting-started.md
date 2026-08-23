# Getting Started — Run the Complete EAP Learning Path

This is the canonical first-use guide for the ATAL Enterprise Assurance Profile (EAP).

If this is your first time in the repository, **do not start with the schemas, control catalog, release history, or governance files**. Start with the complete EAP-L2 worked example and follow one deployment from declaration to assurance claim.

## 1. Clone and install

```bash
git clone https://github.com/sankarshanmukhopadhyay/atal-enterprise-assurance-profile.git
cd atal-enterprise-assurance-profile
python -m pip install -r requirements.txt
```

Run the repository gate once to establish a clean baseline:

```bash
python scripts/run_quality_gate.py --mode validate
```

## 2. Start with this file

Open:

```text
examples/eap-l2-worked-example/deployment-profile.json
```

This is the **first file to read**. It describes the system and deployment being assessed: its identity, autonomy, impact, environment, and the authorities responsible for the system, assessment, and risk acceptance.

EAP deliberately does not use one monolithic assessment file. Deployment facts, evidence, executable observations, assessment decisions, authorities, and assurance claims remain separate so each can be independently tested and audited.

## 3. Derive the minimum assurance level

Run:

```bash
python scripts/derive_assurance_level.py \
  examples/eap-l2-worked-example/deployment-profile.json
```

You should receive `EAP-L2` because the sample deployment declares characteristics such as tool use, persistent memory, external side effects, financial/regulated-data impact, and production operation.

**What this teaches:** assurance level is derived from deployment characteristics rather than selected only as a label.

## 4. See what EAP-L2 requires

Generate the L2 checklist:

```bash
python scripts/generate_profile_checklist.py --level EAP-L2 --format all
```

Inspect:

```text
artifacts/EAP-L2-checklist.md
catalogs/assurance-level-overlays/EAP-L2-overlay.json
```

Then verify that the worked example covers every mandatory L2 control:

```bash
python scripts/check_required_controls.py \
  --level EAP-L2 \
  --bundle examples/eap-l2-worked-example/evidence-bundle.json
```

**What this teaches:** the overlay determines which controls are mandatory and how evidence expectations tighten at the selected level.

## 5. Inspect the evidence bundle

Open:

```text
examples/eap-l2-worked-example/evidence-bundle.json
```

This is the primary evidence container. Follow several control entries and note the evidence grade, status, artifact references, and relationship to the control catalog.

Validate it indirectly through the complete worked-example validator:

```bash
python scripts/validate_l2_worked_example.py
```

**What this teaches:** evidence is structured input to an assessment; evidence is not itself the assessment decision.

## 6. Inspect executable observations

Open:

```text
examples/eap-l2-worked-example/test-results/EAP-TEST-NB-001.json
examples/eap-l2-worked-example/test-results/EAP-TEST-KS-001.json
```

These are machine-readable observations for non-bypassability and kill-switch behavior. Compare them with their portable test definitions under `tests/catalog/`.

**What this teaches:** EAP can require evidence produced by execution, not only policies or screenshots.

## 7. Inspect the assessment result

Open:

```text
examples/eap-l2-worked-example/assessment-result.json
```

Then run:

```bash
python scripts/check_required_controls.py \
  --level EAP-L2 \
  --result examples/eap-l2-worked-example/assessment-result.json
```

**What this teaches:** the assessment is a distinct judgment over evidence and control criteria. It is not enterprise risk acceptance and is not certification.

## 8. Build the human-readable report

Run:

```bash
python scripts/compile_assessment_report.py \
  --level EAP-L2 \
  --bundle examples/eap-l2-worked-example/evidence-bundle.json \
  --result examples/eap-l2-worked-example/assessment-result.json
```

Inspect:

```text
artifacts/EAP-L2-assessment-report.md
```

**What this teaches:** machine-readable evidence and assessment can produce an operator/auditor-readable output without becoming the source of truth themselves.

## 9. Build the bounded assurance claim

Run:

```bash
python scripts/build_l2_assurance_claim.py
```

Inspect:

```text
artifacts/eap-l2-assurance-claim.json
```

Notice that the claim is deployment-scoped, authority-scoped, versioned, time-bounded, and digest-bound to evidence and assessment artifacts.

**What this teaches:** the output is a bounded assurance claim, not a generic statement that a product or organization is “compliant”.

## 10. Break it deliberately

Make a temporary copy of the L2 evidence bundle:

```bash
cp examples/eap-l2-worked-example/evidence-bundle.json /tmp/eap-l2-evidence.json
```

In the repository copy, temporarily remove one mandatory control entry or change a mandatory control from `pass` to `fail`. Then run:

```bash
python scripts/validate_l2_worked_example.py
```

The validator should fail closed. Restore the original file:

```bash
cp /tmp/eap-l2-evidence.json examples/eap-l2-worked-example/evidence-bundle.json
```

Run the validator again and confirm it passes.

**What this teaches:** the examples are executable conformance evidence, not static documentation samples.

## 11. Move to the full high-assurance example

After completing L2, continue with:

```text
examples/eap-l3-worked-example/README.md
```

The L3 example adds:

- all 20 mandatory controls;
- stronger E4/E5 evidence expectations for designated critical controls;
- seven executable positive test results;
- adversarial negative fixtures;
- digest-addressed independent-assessor handoff;
- tamper rejection;
- compatibility/conformance and readiness evidence.

The learning progression is therefore:

```text
L2 = learn the tooling
L3 = understand the complete high-assurance/adversarial system
```

## 12. Run everything

When the individual steps make sense, run:

```bash
python scripts/run_quality_gate.py --mode all
```

That executes the repository's canonical assurance checks and regenerates derived artifacts.

## Artifact flow to remember

```text
deployment-profile.json
        ↓
derived assurance level
        ↓
profile overlay + mandatory controls
        ↓
evidence-bundle.json
        ↓
executable test-results/
        ↓
assessment-result.json
        ↓
assessment report
        ↓
assurance claim
        ↓
L3: independent assessor handoff + verification
```

## Authority boundary

EAP keeps these acts logically separate:

- **System Authority** declares responsibility for the deployed system.
- **Assessment Authority** evaluates evidence against EAP requirements.
- **Risk Acceptance Authority** decides whether residual enterprise risk is accepted.
- **Profile Authority** governs EAP semantics.
- **Independent Verifier** can verify a bounded handoff but does not inherit assessment or risk-acceptance authority.

Evidence is not assessment. Assessment is not risk acceptance. Risk acceptance is not EAP conformance. EAP conformance is not regulatory approval. Independent verification is not certification.
