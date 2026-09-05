# Public repository baseline

This record captures controls reviewed under issue #26. It is repository assurance evidence, not external certification.

| Control | State | Evidence | Residual risk |
|---|---|---|---|
| Purpose/maturity/adoption/upstream boundary | PASS | `README.md`, `PROJECT-STATUS.yaml`, `GOVERNANCE.md`, `UPSTREAM.md`, `COMPATIBILITY.md` | None identified. |
| Licensing | PASS | `LICENSE.md` | None identified. |
| Security reporting/supported versions | PASS | `SECURITY.md` | Hosted private-reporting enablement remains platform evidence. |
| Contribution/community/support | PASS | `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `SUPPORT.md`, issue/PR templates | None identified. |
| Dependency updates | PASS | `.github/dependabot.yml` | Hosted Dependabot enablement remains platform evidence. |
| Default-branch protection | EVIDENCE REQUIRED | rulesets API returned no active ruleset on 2026-09-05 | Tracked separately as a repository-setting control. |
| Assurance/evidence/compatibility | PASS / bounded | assessments, assurance, artifacts, catalogs, workflows and compatibility surfaces | Workflow green is not an external certification conclusion. |
| Authority boundary | PASS | governance/upstream docs | Profile authority does not supersede upstream frameworks or deployment authorities. |

## Completion boundary

Repository-owned baseline gaps are closed by the remediation PR. Default-branch protection remains a GitHub-hosted residual tracked separately.
