# Maintainer Release Checklist

Use this checklist before merging a release PR. See `docs/release-automation.md` for the publication contract.

## Preconditions

- Choose one semantic version for the release.
- Update `PROJECT-STATUS.yaml` `project.version`.
- Update the README version badge.
- Add the matching heading to `changelog/CHANGELOG.md`.
- Update `upstream/atal-baseline.yaml` `eap_version` and confirm the pinned ATAL baseline remains correct.
- Add exactly one new `releases/v<version>.md` release ledger record.
- Ensure that release record contains `## Validation` and `## Release evidence` sections.
- Update catalog/overlay versions when their own artifact semantics require a version increment; do not change them merely to mirror the repository version.

## Quality gate

Run:

```bash
pip install -r requirements.txt
python scripts/run_quality_gate.py --mode all
```

The quality gate includes `scripts/release_governance.py validate-current`, so inconsistent release/version surfaces fail CI before publication.

A release is not ready unless this completes cleanly.

## Review points

- Catalog JSON and YAML remain semantically equivalent.
- Overlays reference only valid controls.
- Mandatory controls remain applicable at each level.
- Dependency rules remain valid for the target level.
- Sample evidence and assessment stay aligned to the current control set.
- Checked-in artifacts in `artifacts/` are regenerated from current sources.
- Release ledger title, version, validation instructions, and release-evidence statement are accurate.
- `PROJECT-STATUS.yaml`, README, changelog, upstream baseline, and release ledger agree on the repository release version.

## Publication

For normal releases, merge the release PR to `main`. Adding the new `releases/v<version>.md` file triggers `.github/workflows/publish-release.yml` automatically.

The workflow validates the exact merge commit, creates an immutable annotated `v<version>` tag at that commit, pushes it, and publishes the GitHub Release using the release ledger as the notes body.

For recovery or historical publication, use the workflow's manual dispatch path and provide the version plus an optional exact target SHA. The workflow refuses to move an existing tag.
