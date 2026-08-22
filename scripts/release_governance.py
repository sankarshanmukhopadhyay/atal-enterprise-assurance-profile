#!/usr/bin/env python3
"""Governed release discovery, validation, and metadata extraction.

Future releases use a strict contract at the exact tag target. Historical releases
created before release automation use an explicit immutable target manifest and a
legacy validation mode that preserves history without weakening future governance.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import re
import subprocess
import sys

import yaml

DEFAULT_REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
SEMVER_RE = re.compile(r"^(?:v)?(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-([0-9A-Za-z.-]+))?$")
RELEASE_PATH_RE = re.compile(r"^releases/v((?:0|[1-9]\d*)\.(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)(?:-[0-9A-Za-z.-]+)?)\.md$")


def run(repo_root: pathlib.Path, *args: str) -> str:
    completed = subprocess.run(
        args, cwd=repo_root, check=True, text=True,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    )
    return completed.stdout.strip()


def normalize_version(raw: str) -> str:
    raw = raw.strip()
    if not SEMVER_RE.fullmatch(raw):
        raise ValueError(f"invalid semantic version: {raw!r}")
    return raw[1:] if raw.startswith("v") else raw


def release_path(repo_root: pathlib.Path, version: str) -> pathlib.Path:
    return repo_root / "releases" / f"v{version}.md"


def write_output(path: str, key: str, value: str) -> None:
    with open(path, "a", encoding="utf-8") as handle:
        handle.write(f"{key}={value}\n")


def read_text(repo_root: pathlib.Path, relative: str) -> str:
    path = repo_root / relative
    if not path.exists():
        raise ValueError(f"required file is missing: {relative}")
    return path.read_text(encoding="utf-8")


def discover(repo_root: pathlib.Path, before: str, after: str) -> list[str]:
    zero = "0" * 40
    if not before or before == zero:
        before = run(repo_root, "git", "rev-parse", f"{after}^")
    changed = run(repo_root, "git", "diff", "--diff-filter=A", "--name-only", before, after, "--", "releases/v*.md")
    versions: list[str] = []
    for path in [line.strip() for line in changed.splitlines() if line.strip()]:
        match = RELEASE_PATH_RE.fullmatch(path)
        if not match:
            raise ValueError(f"release ledger path is not canonical: {path}")
        versions.append(normalize_version(match.group(1)))
    if len(versions) > 1:
        raise ValueError(
            "automatic publication requires exactly one new release ledger record per merge; "
            f"found {len(versions)}: {', '.join(versions)}"
        )
    return versions


def current_project_version(repo_root: pathlib.Path) -> str:
    status = yaml.safe_load(read_text(repo_root, "PROJECT-STATUS.yaml"))
    raw = str(status.get("project", {}).get("version", ""))
    if not raw:
        raise ValueError("PROJECT-STATUS.yaml project.version is missing")
    return normalize_version(raw)


def release_title(repo_root: pathlib.Path, version: str) -> str:
    text = read_text(repo_root, f"releases/v{version}.md")
    first = next((line.strip() for line in text.splitlines() if line.strip()), "")
    match = re.fullmatch(rf"#\s+v{re.escape(version)}\s+[—-]\s+(.+)", first)
    if not match:
        raise ValueError(f"releases/v{version}.md must start with '# v{version} — <release title>'")
    return f"v{version} — {match.group(1).strip()}"


def load_legacy_manifest(engine_root: pathlib.Path) -> dict:
    path = engine_root / "releases" / "release-manifest.yaml"
    if not path.exists():
        return {}
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return data.get("legacy_releases", {}) or {}


def resolve_legacy_target(engine_root: pathlib.Path, version: str) -> str | None:
    entry = load_legacy_manifest(engine_root).get(version)
    if not entry:
        return None
    sha = str(entry.get("target_sha", ""))
    if not re.fullmatch(r"[0-9a-f]{40}", sha):
        raise ValueError(f"legacy target for {version} is not a full 40-character SHA")
    return sha


def validate_common(repo_root: pathlib.Path, version: str, target_sha: str) -> tuple[str, str]:
    version = normalize_version(version)
    expected_head = run(repo_root, "git", "rev-parse", "HEAD")
    resolved_target = run(repo_root, "git", "rev-parse", f"{target_sha}^{{commit}}")
    if resolved_target != expected_head:
        raise ValueError(f"release validation must run at the tag target: HEAD={expected_head}, target={resolved_target}")
    notes = read_text(repo_root, f"releases/v{version}.md")
    title = release_title(repo_root, version)
    if "## Validation" not in notes:
        raise ValueError(f"releases/v{version}.md must contain a '## Validation' section")
    return resolved_target, title


def validate_strict(repo_root: pathlib.Path, version: str, target_sha: str) -> None:
    resolved_target, title = validate_common(repo_root, version, target_sha)
    notes = read_text(repo_root, f"releases/v{version}.md")
    if "## Release evidence" not in notes:
        raise ValueError(f"releases/v{version}.md must contain a '## Release evidence' section")
    project_version = current_project_version(repo_root)
    if project_version != version:
        raise ValueError(f"PROJECT-STATUS.yaml project.version={project_version!r}; expected {version!r}")
    readme = read_text(repo_root, "README.md")
    if not re.search(rf"version-{re.escape(version)}-blue\.svg", readme):
        raise ValueError(f"README version badge does not declare {version}")
    changelog = read_text(repo_root, "changelog/CHANGELOG.md")
    if not re.search(rf"^##\s+{re.escape(version)}(?:\s|$)", changelog, re.MULTILINE):
        raise ValueError(f"changelog does not contain a {version} release heading")
    upstream = yaml.safe_load(read_text(repo_root, "upstream/atal-baseline.yaml"))
    eap_version = normalize_version(str(upstream.get("eap_version", "")))
    if eap_version != version:
        raise ValueError(f"upstream/atal-baseline.yaml eap_version={eap_version!r}; expected {version!r}")
    print(f"✓ Strict release governance validation passed for {title}")
    print(f"  Target commit: {resolved_target}")


def validate_legacy(engine_root: pathlib.Path, repo_root: pathlib.Path, version: str, target_sha: str) -> None:
    resolved_target, title = validate_common(repo_root, version, target_sha)
    declared = resolve_legacy_target(engine_root, version)
    if declared is None:
        raise ValueError(f"{version} is not declared in releases/release-manifest.yaml as a legacy release")
    if declared != resolved_target:
        raise ValueError(f"legacy manifest declares {declared} for {version}, not {resolved_target}")
    # Historical checkpoints predate the strict cross-file version contract. Do not
    # rewrite history or pretend those surfaces were synchronized when they were not.
    print(f"✓ Legacy release checkpoint validated for {title}")
    print(f"  Manifest target: {resolved_target}")
    print("  Contract: historical checkpoint (strict future version-surface rules not retroactive)")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", default=str(DEFAULT_REPO_ROOT), help="Repository tree to inspect")
    sub = parser.add_subparsers(dest="command", required=True)

    p_norm = sub.add_parser("normalize-version"); p_norm.add_argument("version")
    p_discover = sub.add_parser("discover")
    p_discover.add_argument("--before", required=True); p_discover.add_argument("--after", required=True); p_discover.add_argument("--github-output", required=True)
    p_validate = sub.add_parser("validate")
    p_validate.add_argument("--version", required=True); p_validate.add_argument("--target-sha", required=True)
    p_validate.add_argument("--mode", choices=["strict", "legacy"], default="strict")
    sub.add_parser("validate-current")
    p_metadata = sub.add_parser("metadata"); p_metadata.add_argument("--version", required=True); p_metadata.add_argument("--github-output", required=True)
    p_legacy = sub.add_parser("legacy-target"); p_legacy.add_argument("--version", required=True)

    args = parser.parse_args()
    repo_root = pathlib.Path(args.repo_root).resolve()
    engine_root = DEFAULT_REPO_ROOT
    try:
        if args.command == "normalize-version":
            print(normalize_version(args.version))
        elif args.command == "discover":
            versions = discover(repo_root, args.before, args.after)
            write_output(args.github_output, "versions", json.dumps(versions, separators=(",", ":")))
            print(f"Discovered release records: {versions}")
        elif args.command == "validate":
            if args.mode == "legacy": validate_legacy(engine_root, repo_root, normalize_version(args.version), args.target_sha)
            else: validate_strict(repo_root, normalize_version(args.version), args.target_sha)
        elif args.command == "validate-current":
            validate_strict(repo_root, current_project_version(repo_root), run(repo_root, "git", "rev-parse", "HEAD"))
        elif args.command == "metadata":
            version = normalize_version(args.version); write_output(args.github_output, "title", release_title(repo_root, version))
        elif args.command == "legacy-target":
            target = resolve_legacy_target(engine_root, normalize_version(args.version))
            if not target: raise ValueError(f"no legacy target declared for {args.version}")
            print(target)
        return 0
    except (ValueError, subprocess.CalledProcessError, yaml.YAMLError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(main())
