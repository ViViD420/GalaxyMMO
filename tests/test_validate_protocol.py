from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from tools.validate_protocol import validate_manifest


class ProtocolManifestTests(unittest.TestCase):
    def test_repository_manifest_is_valid(self) -> None:
        self.assertEqual(validate_manifest(), [])

    def test_rejects_unproven_core3_compatibility(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "manifest.json"
            data = {
                "product": "GalaxyMMO",
                "protocol_name": "galaxymmo-client-server",
                "protocol_version": "0.1.0",
                "status": "design",
                "transport": "undecided",
                "serialization": "undecided",
                "server_authoritative": True,
                "compatibility": {"core3_wire_compatible": True},
            }
            path.write_text(json.dumps(data), encoding="utf-8")
            self.assertTrue(any("core3_wire_compatible" in e for e in validate_manifest(path)))

    def test_rejects_invalid_version(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "manifest.json"
            data = {
                "product": "GalaxyMMO",
                "protocol_name": "galaxymmo-client-server",
                "protocol_version": "v1",
                "status": "design",
                "transport": "undecided",
                "serialization": "undecided",
                "server_authoritative": True,
                "compatibility": {"core3_wire_compatible": False},
            }
            path.write_text(json.dumps(data), encoding="utf-8")
            self.assertTrue(any("protocol_version" in e for e in validate_manifest(path)))


if __name__ == "__main__":
    unittest.main()
