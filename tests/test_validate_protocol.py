from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from tools.validate_protocol import MAX_MANIFEST_BYTES, validate_manifest


def valid_manifest() -> dict[str, object]:
    return {
        "product": "GalaxyMMO",
        "protocol_name": "galaxymmo-client-server",
        "protocol_version": "0.1.0",
        "status": "design",
        "transport": "undecided",
        "serialization": "undecided",
        "server_authoritative": True,
        "compatibility": {"core3_wire_compatible": False},
    }


class ProtocolManifestTests(unittest.TestCase):
    def write_manifest(self, directory: str, content: str | bytes) -> Path:
        path = Path(directory) / "manifest.json"
        path.write_bytes(content.encode("utf-8") if isinstance(content, str) else content)
        return path

    def test_repository_manifest_is_valid(self) -> None:
        self.assertEqual(validate_manifest(), [])

    def test_rejects_unproven_core3_compatibility(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            data = valid_manifest()
            data["compatibility"] = {"core3_wire_compatible": True}
            path = self.write_manifest(directory, json.dumps(data))
            self.assertTrue(any("core3_wire_compatible" in e for e in validate_manifest(path)))

    def test_rejects_invalid_version(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            data = valid_manifest()
            data["protocol_version"] = "v1"
            path = self.write_manifest(directory, json.dumps(data))
            self.assertTrue(any("protocol_version" in e for e in validate_manifest(path)))

    def test_rejects_unhashable_status_without_crashing(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            data = valid_manifest()
            data["status"] = ["design"]
            path = self.write_manifest(directory, json.dumps(data))
            self.assertTrue(any("status must be" in e for e in validate_manifest(path)))

    def test_rejects_duplicate_json_keys(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = self.write_manifest(directory, '{"product":"GalaxyMMO","product":"Other"}')
            self.assertTrue(any("duplicate object key" in e for e in validate_manifest(path)))

    def test_rejects_non_object_root(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = self.write_manifest(directory, "[]")
            self.assertTrue(any("root must be a JSON object" in e for e in validate_manifest(path)))

    def test_rejects_nonstandard_nan_constant(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = self.write_manifest(directory, '{"unexpected": NaN}')
            self.assertTrue(any("non-standard JSON constant" in e for e in validate_manifest(path)))

    def test_rejects_invalid_utf8(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = self.write_manifest(directory, b'{"name":"\xff"}')
            self.assertTrue(any("not valid UTF-8" in e for e in validate_manifest(path)))

    def test_rejects_oversized_manifest_before_parsing(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = self.write_manifest(directory, b" " * (MAX_MANIFEST_BYTES + 1))
            self.assertTrue(any("safety limit" in e for e in validate_manifest(path)))


if __name__ == "__main__":
    unittest.main()
