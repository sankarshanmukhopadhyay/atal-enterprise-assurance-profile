# Maintainer Release Checklist

Use this checklist before cutting a release.

## Preconditions

- Update version references in the catalog, overlays, README, and changelog
- Confirm sample artifacts still represent the intended profile behavior
- Confirm upstream pinning in `UPSTREAM.md` if upstream dependencies changed

## Quality gate

Run:

```bash
pip install -r requirements.txt
python scripts/run_quality_gate.py --mode all
```

A release is not ready unless this completes cleanly.

## Review points

- Catalog JSON and YAML remain semantically equivalent
- Overlays reference only valid controls
- Mandatory controls remain applicable at each level
- Dependency rules remain valid for the target level
- Sample evidence and assessment stay aligned to the current catalog version and control set
- Checked-in artifacts in `artifacts/` are regenerated from current sources

## Packaging

- Review `artifacts/` diffs for accidental drift
- Review `README.md` and `docs/cli-usage.md` for command accuracy
- Add a changelog entry with the release theme and major additions
- Package the repository only after the quality gate passes
