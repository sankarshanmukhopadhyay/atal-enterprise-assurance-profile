# Independent Assessor Handoff

## Purpose

v0.9.3 makes an EAP assurance claim independently reproducible from a bounded, digest-addressed handoff rather than undocumented repository context.

The handoff is an evidence transport contract. It does not delegate enterprise risk acceptance, regulatory authority, or upstream ATAL governance to the verifier.

## Authority boundaries

- **Profile Authority** defines EAP schemas, controls, evidence contracts, and claim semantics.
- **System Authority** remains accountable for the assessed deployment and the truthfulness of deployment declarations.
- **Assessment Authority** evaluates evidence and produces the assessment result.
- **Risk Acceptance Authority** owns acceptance of residual risk and waivers.
- **Independent Verifier** checks integrity, completeness, version consistency, claim lifecycle, and reconstructability. Verification does not itself grant risk acceptance or certification.

## Bounded source set

`assurance/handoff-source-set.yaml` declares the source artifacts that must be present. `scripts/build_assessor_handoff.py` hashes each source and produces `artifacts/eap-l3-assessor-handoff.json`.

The manifest binds:

1. deployment profile;
2. evidence bundle;
3. assessment result;
4. executable test results;
5. upstream baseline;
6. release record;
7. generated assurance claim;
8. waivers, when applicable.

## Verification

```bash
python scripts/build_l3_assurance_claim.py
python scripts/build_assessor_handoff.py
python scripts/verify_assessor_handoff.py --tamper-self-test
```

The verifier fails closed when a required source is missing, a digest differs, the claim and manifest disagree on subject/authority/profile/lifecycle, the claim is revoked, or the validity window has elapsed without the state becoming `EXPIRED` or `REVOKED`.

A machine-readable result is written to `artifacts/eap-l3-handoff-verification.json`. The deliberate tamper test writes `artifacts/eap-l3-handoff-tamper-verification.json` and must report rejection for `digest-mismatch`.

## Assurance interpretation

A successful verification means that the bounded handoff is internally reproducible and integrity-consistent. It does **not** establish that the underlying evidence is true, sufficient for a regulator, or independently certified beyond the checks performed by the verifier.
