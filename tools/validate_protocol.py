#!/usr/bin/env python3
"""Validate the GalaxyMMO protocol manifest using only the Python standard library."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "Integration" / "Protocol" / "protocol-manifest.json"
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


def validate_manifest(path: Path = MANIFEST) -> list[str]:
    errors: list[str] = []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return [f"Manifest not found: {path}"]
    except json.JSONDecodeError as exc:
        return [f"Invalid JSON at line {exc.lineno}, column {exc.colno}: {exc.msg}"]
    except OSError as exc:
        return [f"Could not read manifest: {exc}"]

    if not isinstance(data, dict):
        return ["Manifest root must be a JSON object."]

    missing = sorted(REQUIRED_KEYS - data.keys())
    if missing:
        errors.append("Missing required keys: " + ", ".join(missing))

    if data.get("product") != "GalaxyMMO":
        errors.append("product must be 'GalaxyMMO'.")
    if not isinstance(data.get("protocol_name"), str) or not data["protocol_name"].strip():
        errors.append("protocol_name must be a non-empty string.")
    version = data.get("protocol_version")
    if not isinstance(version, str) or not SEMVER.fullmatch(version):
        errors.append("protocol_version must use MAJOR.MINOR.PATCH numeric format.")
    if data.get("status") not in {"design", "experimental", "stable", "deprecated"}:
        errors.append("status must be design, experimental, stable, or deprecated.")
    if not isinstance(data.get("transport"), str) or not data["transport"].strip():
        errors.append("transport must be a non-empty string (use 'undecided' while evaluating).")
    if not isinstance(data.get("serialization"), str) or not data["serialization"].strip():
        errors.append("serialization must be a non-empty string (use 'undecided' while evaluating).")
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
