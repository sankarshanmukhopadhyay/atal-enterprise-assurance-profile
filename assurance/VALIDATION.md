# v0.9.0 Validation Checkpoint

This file records the candidate validation contract used to exercise the complete repository through GitHub Actions after the v0.4.0–v0.9.0 assurance sequence was landed.

The authoritative validation entrypoint is:

```bash
python scripts/run_quality_gate.py --mode all
```

A successful run demonstrates repository-level integrity, upstream provenance resolution, executable test-catalog validity, external mapping integrity, evidence-bundle grading, assessment consistency, generated artifact reproducibility, and the v0.9 cross-artifact assurance invariants.

This checkpoint is evidence of repository self-consistency only. It is not implementation certification, regulatory approval, or third-party assurance.
