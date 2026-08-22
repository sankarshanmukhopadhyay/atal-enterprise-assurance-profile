# Governed Release Publication

EAP releases are published from a versioned release ledger record in `releases/v<version>.md`. The ledger record is the human-readable release note source and the publication workflow treats the validated repository commit as the immutable release point.

## Automatic path

A future release is prepared in a normal pull request. The release PR MUST add exactly one new `releases/v<version>.md` file and update all version surfaces required by `scripts/release_governance.py`.

When that PR is merged to `main`, `.github/workflows/publish-release.yml` detects the newly added ledger record. It checks out the exact merge commit, validates release governance, executes the canonical assurance quality gate, creates an annotated `v<version>` tag at that exact commit, pushes the tag, and creates the GitHub Release using the ledger file as the release body.

Automatic discovery intentionally ignores modifications to existing release records. Editing historical notes therefore cannot create or move a tag.

## Version contract

At the commit being released, all of the following MUST agree:

- `PROJECT-STATUS.yaml` → `project.version`
- `README.md` version badge
- `changelog/CHANGELOG.md` release heading
- `upstream/atal-baseline.yaml` → `eap_version`
- `releases/v<version>.md` filename and first heading

The release ledger MUST contain `## Validation` and `## Release evidence` sections. The canonical quality gate also executes `scripts/release_governance.py validate-current`, so version drift is rejected during ordinary CI before publication.

## Tag immutability

The workflow never moves an existing tag. If `v<version>` already exists at a different commit, publication fails closed. If it already exists at the validated target commit, the tag is reused.

An existing GitHub Release is also left unchanged by default. A maintainer may explicitly use manual dispatch with `force_republish=true` to refresh only the release title/body. This does not move the tag.

## Manual/recovery path

The workflow supports `workflow_dispatch` with:

- `version` — required semantic version, with or without leading `v`
- `target_sha` — optional exact release commit; when omitted, the latest commit touching `releases/v<version>.md` is resolved
- `force_republish` — optional release-body refresh when the GitHub Release already exists

A manually supplied target MUST be an ancestor of `origin/main`, and all release-governance checks run against that exact detached commit before any tag or release is created.

## Required repository permission

The workflow declares `contents: write`, which is required for tag pushes and GitHub Release creation through the repository-scoped `GITHUB_TOKEN`. Repository/organization Actions policy must allow the workflow token to have write access to contents.

## Evidence produced

Each successful publication writes a GitHub Actions step summary containing the version, exact tag target SHA, notes source, governance-validation result, assurance-validation result, and tag-immutability policy. The Git tag and GitHub Release then provide durable publication evidence anchored to the validated commit.
