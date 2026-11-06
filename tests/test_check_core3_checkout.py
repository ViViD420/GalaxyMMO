from __future__ import annotations

import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from tools.check_core3_checkout import EXPECTED_CORE3_COMMIT, _is_accepted_origin, inspect_checkout


class Core3CheckoutTests(unittest.TestCase):
    def test_rejects_missing_checkout(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            missing = Path(directory) / "missing"
            self.assertTrue(any("does not exist" in e for e in inspect_checkout(missing)))

    def test_rejects_file_as_checkout(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "not-a-directory"
            path.write_text("x", encoding="utf-8")
            self.assertTrue(any("not a directory" in e for e in inspect_checkout(path)))

    def test_reports_non_git_directory(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            with patch("tools.check_core3_checkout.subprocess.run") as run:
                run.side_effect = subprocess.CalledProcessError(
                    128, ["git"], stderr="fatal: not a git repository"
                )
                self.assertTrue(
                    any("Could not inspect Git checkout" in e for e in inspect_checkout(Path(directory)))
                )
                self.assertEqual(run.call_count, 1)

    def test_accepts_https_ssh_and_gerrit_upstream_origins(self) -> None:
        for remote in (
            "https://github.com/swgemu/Core3.git",
            "git@github.com:swgemu/Core3.git",
            "ssh://git@github.com/swgemu/Core3.git",
            "https://review.swgemu.com/core3",
        ):
            with self.subTest(remote=remote):
                self.assertTrue(_is_accepted_origin(remote))

    def test_rejects_lookalike_or_fork_origins(self) -> None:
        for remote in (
            "https://github.com/swgemu/Core3.evil.git",
            "https://github.com/attacker/Core3.git",
            "https://github.com.evil/swgemu/Core3.git",
            "https://example.com/swgemu/Core3.git",
            "",
        ):
            with self.subTest(remote=remote):
                self.assertFalse(_is_accepted_origin(remote))

    def test_accepts_clean_pinned_checkout_including_worktree_layout(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            checkout = Path(directory)
            outputs = [
                "true",
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
                self.assertEqual(run.call_count, 4)

    def test_rejects_wrong_commit_remote_and_dirty_tree(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            checkout = Path(directory)
            outputs = [
                "true",
                "deadbeef",
                "https://example.com/fork/Core3.git",
                " M changed.cpp",
            ]
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
