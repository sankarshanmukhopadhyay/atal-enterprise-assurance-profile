#!/usr/bin/env python3
"""Governed release discovery, validation, and metadata extraction.

The release ledger is `releases/v<semver>.md`. Automatic publication is allowed only
when exactly one new ledger record is added to `main` and repository version surfaces
agree at the commit being tagged.
"""

from __future__ import annotations

import argparse
import json
import pathlib
import re
import subprocess
import sys

import yaml

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
SEMVER_RE = re.compile(r"^(?:v)?(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-([0-9A-Za-z.-]+))?$" )
RELEASE_PATH_RE = re.compile(r"^releases/v((?:0|[1-9]\d*)\.(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)(?:-[0-9A-Za-z.-]+)?)\.md$")


def run(*args: str) -> str:
    completed = subprocess.run(
        args,
        cwd=REPO_ROOT,
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return completed.stdout.strip()


def normalize_version(raw: str) -> str:
    raw = raw.strip()
    match = SEMVER_RE.fullmatch(raw)
    if not match:
        raise ValueError(f"invalid semantic version: {raw!r}")
    return raw[1:] if raw.startswith("v") else raw


def release_path(version: str) -> pathlib.Path:
    return REPO_ROOT / "releases" / f"v{version}.md"


def write_output(path: str, key: str, value: str) -> None:
    with open(path, "a", encoding="utf-8") as handle:
        handle.write(f"{key}={value}\n")


def discover(before: str, after: str) -> list[str]:
    zero = "0" * 40
    if not before or before == zero:
        parent = run("git", "rev-parse", f"{after}^")
        before = parent

    changed = run(
        "git",
        "diff",
        "--diff-filter=A",
        "--name-only",
        before,
        after,
        "--",
        "releases/v*.md",
    )
    paths = [line.strip() for line in changed.splitlines() if line.strip()]
    versions: list[str] = []
    for path in paths:
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


def read_text(path: pathlib.Path) -> str:
    if not path.exists():
        raise ValueError(f"required file is missing: {path.relative_to(REPO_ROOT)}")
    return path.read_text(encoding="utf-8")


def release_title(version: str) -> str:
    text = read_text(release_path(version))
    first = next((line.strip() for line in text.splitlines() if line.strip()), "")
    match = re.fullmatch(rf"#\s+v{re.escape(version)}\s+[—-]\s+(.+)", first)
    if not match:
        raise ValueError(
            f"releases/v{version}.md must start with '# v{version} — <release title>'"
        )
    return f"v{version} — {match.group(1).strip()}"


def validate(version: str, target_sha: str) -> None:
    version = normalize_version(version)
    expected_head = run("git", "rev-parse", "HEAD")
    resolved_target = run("git", "rev-parse", f"{target_sha}^{{commit}}")
    if resolved_target != expected_head:
        raise ValueError(
            f"release validation must run at the tag target: HEAD={expected_head}, target={resolved_target}"
        )

    notes = read_text(release_path(version))
    title = release_title(version)
    if "## Validation" not in notes:
        raise ValueError(f"releases/v{version}.md must contain a '## Validation' section")
    if "## Release evidence" not in notes:
        raise ValueError(f"releases/v{version}.md must contain a '## Release evidence' section")

    status = yaml.safe_load(read_text(REPO_ROOT / "PROJECT-STATUS.yaml"))
    project_version = str(status.get("project", {}).get("version", "")).lstrip("v")
    if project_version != version:
        raise ValueError(
            f"PROJECT-STATUS.yaml project.version={project_version!r}; expected {version!r}"
        )

    readme = read_text(REPO_ROOT / "README.md")
    if not re.search(rf"version-{re.escape(version)}-blue\.svg", readme):
        raise ValueError(f"README version badge does not declare {version}")

    changelog = read_text(REPO_ROOT / "changelog" / "CHANGELOG.md")
    if not re.search(rf"^##\s+{re.escape(version)}(?:\s|$)", changelog, re.MULTILINE):
        raise ValueError(f"changelog does not contain a {version} release heading")

    upstream = yaml.safe_load(read_text(REPO_ROOT / "upstream" / "atal-baseline.yaml"))
    eap_version = str(upstream.get("eap_version", "")).lstrip("v")
    if eap_version and eap_version != version:
        raise ValueError(
            f"upstream/atal-baseline.yaml eap_version={eap_version!r}; expected {version!r}"
        )

    print(f"✓ Release governance validation passed for {title}")
    print(f"  Target commit: {resolved_target}")
    print(f"  Release ledger: releases/v{version}.md")
    print(f"  Project status: {project_version}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    p_norm = sub.add_parser("normalize-version")
    p_norm.add_argument("version")

    p_discover = sub.add_parser("discover")
    p_discover.add_argument("--before", required=True)
    p_discover.add_argument("--after", required=True)
    p_discover.add_argument("--github-output", required=True)

    p_validate = sub.add_parser("validate")
    p_validate.add_argument("--version", required=True)
    p_validate.add_argument("--target-sha", required=True)

    p_metadata = sub.add_parser("metadata")
    p_metadata.add_argument("--version", required=True)
    p_metadata.add_argument("--github-output", required=True)

    args = parser.parse_args()
    try:
        if args.command == "normalize-version":
            print(normalize_version(args.version))
        elif args.command == "discover":
            versions = discover(args.before, args.after)
            write_output(args.github_output, "versions", json.dumps(versions, separators=(",", ":")))
            print(f"Discovered release records: {versions}")
        elif args.command == "validate":
            validate(args.version, args.target_sha)
        elif args.command == "metadata":
            version = normalize_version(args.version)
            write_output(args.github_output, "title", release_title(version))
        return 0
    except (ValueError, subprocess.CalledProcessError, yaml.YAMLError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
