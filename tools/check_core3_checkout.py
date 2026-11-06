#!/usr/bin/env python3
"""Check that a Core3 working copy matches GalaxyMMO's audited source pin.

This is a read-only guardrail. It does not clone, build, modify, or run Core3.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import urlsplit

EXPECTED_CORE3_COMMIT = "403893d9b9f8e6fa712fbb3cb1fcd8f0fe45bb79"
EXPECTED_REMOTE_PATH = "swgemu/core3"
SSH_REMOTE = re.compile(r"^(?:[^@]+@)?([^:]+):(.+)$")


def _git(checkout: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(checkout), *args],
        check=True,
        capture_output=True,
        text=True,
        timeout=15,
    )
    return result.stdout.strip()


def _is_accepted_origin(remote: str) -> bool:
    """Accept only the canonical upstream host and repository path."""
    candidate = remote.strip()
    if not candidate:
        return False

    if "://" in candidate:
        parsed = urlsplit(candidate)
        host = (parsed.hostname or "").lower()
        path = parsed.path.strip("/").removesuffix(".git").lower()
    else:
        match = SSH_REMOTE.fullmatch(candidate)
        if not match:
            return False
        host = match.group(1).lower()
        path = match.group(2).strip("/").removesuffix(".git").lower()

    return (host, path) in {
        ("github.com", EXPECTED_REMOTE_PATH),
        ("review.swgemu.com", "core3"),
    }


def inspect_checkout(checkout: Path) -> list[str]:
    """Return validation errors; an empty list means the checkout matches the pin.

    Git itself determines whether the path is a working tree. This supports
    linked worktrees, where .git is a file rather than a directory.
    """
    if not checkout.exists():
        return [f"Core3 checkout does not exist: {checkout}"]
    if not checkout.is_dir():
        return [f"Core3 checkout path is not a directory: {checkout}"]

    try:
        inside_work_tree = _git(checkout, "rev-parse", "--is-inside-work-tree")
        if inside_work_tree != "true":
            return [f"Not a Git working copy: {checkout}"]
        commit = _git(checkout, "rev-parse", "HEAD")
        remote = _git(checkout, "remote", "get-url", "origin")
        dirty = _git(checkout, "status", "--porcelain")
    except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired) as exc:
        return [f"Could not inspect Git checkout: {exc}"]

    errors: list[str] = []
    if commit != EXPECTED_CORE3_COMMIT:
        errors.append(
            f"Unexpected Core3 commit: {commit or '(empty)'}; "
            f"expected {EXPECTED_CORE3_COMMIT}."
        )
    if not _is_accepted_origin(remote):
        errors.append(f"Unexpected Core3 origin remote: {remote or '(missing)'}.")
    if dirty:
        errors.append("Core3 working tree is dirty; use a clean checkout for baseline verification.")
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "checkout",
        type=Path,
        help="Path to the Core3 Git checkout (kept separate from GalaxyMMO).",
    )
    args = parser.parse_args(argv)

    errors = inspect_checkout(args.checkout.resolve())
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print(f"Core3 checkout matches audited pin: {EXPECTED_CORE3_COMMIT}")
    print("Working tree is clean. This does not verify build or runtime behavior.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
