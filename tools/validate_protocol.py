#!/usr/bin/env python3
"""Validate the GalaxyMMO protocol manifest using only the Python standard library."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "Integration" / "Protocol" / "protocol-manifest.json"
MAX_MANIFEST_BYTES = 64 * 1024
REQUIRED_KEYS = {
    "product",
    "protocol_name",
    "protocol_version",
    "status",
    "transport",
    "serialization",
    "server_authoritative",
    "compatibility",
}
SEMVER = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$")
VALID_STATUSES = {"design", "experimental", "stable", "deprecated"}


def _reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    """Reject ambiguous JSON objects instead of silently accepting the last key."""
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate object key: {key!r}")
        result[key] = value
    return result


def _reject_nonstandard_constant(value: str) -> None:
    """Python's JSON decoder otherwise accepts NaN and Infinity extensions."""
    raise ValueError(f"non-standard JSON constant: {value}")


def validate_manifest(path: Path = MANIFEST) -> list[str]:
    try:
        raw = path.read_bytes()
    except FileNotFoundError:
        return [f"Manifest not found: {path}"]
    except OSError as exc:
        return [f"Could not read manifest: {exc}"]

    if len(raw) > MAX_MANIFEST_BYTES:
        return [
            f"Manifest exceeds the {MAX_MANIFEST_BYTES}-byte safety limit: {len(raw)} bytes."
        ]

    try:
        data = json.loads(
            raw.decode("utf-8"),
            object_pairs_hook=_reject_duplicate_keys,
            parse_constant=_reject_nonstandard_constant,
        )
    except UnicodeDecodeError as exc:
        return [f"Manifest is not valid UTF-8 at byte {exc.start}."]
    except json.JSONDecodeError as exc:
        return [f"Invalid JSON at line {exc.lineno}, column {exc.colno}: {exc.msg}"]
    except ValueError as exc:
        return [f"Invalid JSON value: {exc}"]

    if not isinstance(data, dict):
        return ["Manifest root must be a JSON object."]

    errors: list[str] = []
    missing = sorted(REQUIRED_KEYS - data.keys())
    if missing:
        errors.append("Missing required keys: " + ", ".join(missing))

    if data.get("product") != "GalaxyMMO":
        errors.append("product must be 'GalaxyMMO'.")
    protocol_name = data.get("protocol_name")
    if not isinstance(protocol_name, str) or not protocol_name.strip():
        errors.append("protocol_name must be a non-empty string.")
    version = data.get("protocol_version")
    if not isinstance(version, str) or not SEMVER.fullmatch(version):
        errors.append("protocol_version must use MAJOR.MINOR.PATCH numeric format.")
    status = data.get("status")
    if not isinstance(status, str) or status not in VALID_STATUSES:
        errors.append("status must be design, experimental, stable, or deprecated.")
    for field in ("transport", "serialization"):
        value = data.get(field)
        if not isinstance(value, str) or not value.strip():
            errors.append(
                f"{field} must be a non-empty string (use 'undecided' while evaluating)."
            )
    if data.get("server_authoritative") is not True:
        errors.append("server_authoritative must be true.")

    compatibility = data.get("compatibility")
    if not isinstance(compatibility, dict):
        errors.append("compatibility must be a JSON object.")
    elif compatibility.get("core3_wire_compatible") is not False:
        errors.append("core3_wire_compatible must remain false until compatibility is proven.")

    return errors


def main() -> int:
    errors = validate_manifest()
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(f"Protocol manifest valid: {MANIFEST.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
