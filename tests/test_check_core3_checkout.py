from __future__ import annotations

import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from tools.check_core3_checkout import EXPECTED_CORE3_COMMIT, inspect_checkout


class Core3CheckoutTests(unittest.TestCase):
    def test_rejects_missing_checkout(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            missing = Path(directory) / "missing"
            self.assertTrue(any("does not exist" in e for e in inspect_checkout(missing)))

    def test_rejects_directory_without_git_metadata(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            self.assertTrue(any("Not a Git working copy" in e for e in inspect_checkout(Path(directory))))

    def test_accepts_clean_pinned_checkout(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            checkout = Path(directory)
            (checkout / ".git").mkdir()
            outputs = [
                EXPECTED_CORE3_COMMIT,
                "https://github.com/swgemu/Core3.git",
                "",
            ]
            with patch("tools.check_core3_checkout.subprocess.run") as run:
                run.side_effect = [
                    subprocess.CompletedProcess([], 0, value + "\n", "")
                    for value in outputs
                ]
                self.assertEqual(inspect_checkout(checkout), [])
                self.assertEqual(run.call_count, 3)

    def test_rejects_wrong_commit_remote_and_dirty_tree(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            checkout = Path(directory)
            (checkout / ".git").mkdir()
            outputs = ["deadbeef", "https://example.com/fork/Core3.git", " M changed.cpp"]
            with patch("tools.check_core3_checkout.subprocess.run") as run:
                run.side_effect = [
                    subprocess.CompletedProcess([], 0, value + "\n", "")
                    for value in outputs
                ]
                errors = inspect_checkout(checkout)
            self.assertEqual(len(errors), 3)
            self.assertTrue(any("Unexpected Core3 commit" in e for e in errors))
            self.assertTrue(any("Unexpected Core3 origin" in e for e in errors))
            self.assertTrue(any("dirty" in e for e in errors))


if __name__ == "__main__":
    unittest.main()
