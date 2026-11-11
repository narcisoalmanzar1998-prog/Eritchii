#!/usr/bin/env python3
"""Game-free checks for the optional OoT cheat menu installer."""

import io
from pathlib import Path
import tempfile
import unittest
import zipfile

from install import FILES, install, selected_files


class OotCheatInstallerTest(unittest.TestCase):
    def setUp(self):
        self.tempdir = tempfile.TemporaryDirectory()
        self.addCleanup(self.tempdir.cleanup)
        self.root = Path(self.tempdir.name)
        (self.root / "config").mkdir()
        self.content = {FILES[0]: b"module", FILES[1]: b"[No damage]\n"}

    def test_selected_files_ignore_unrelated_archive_members(self):
        output = io.BytesIO()
        with zipfile.ZipFile(output, "w") as bundle:
            for name, data in self.content.items():
                bundle.writestr(name, data)
            bundle.writestr("elsewhere.txt", "unrelated")
        self.assertEqual(selected_files(output.getvalue()), self.content)

    def test_install_is_idempotent(self):
        targets = install(self.root, self.content)
        self.assertEqual(install(self.root, self.content), targets)
        for target, data in zip(targets, self.content.values()):
            self.assertEqual(target.read_bytes(), data)

    def test_dry_run_does_not_write(self):
        targets = install(self.root, self.content, dry_run=True)
        self.assertTrue(all(not target.exists() for target in targets))

    def test_existing_cheats_are_not_overwritten(self):
        target = self.root / FILES[1]
        target.parent.mkdir(parents=True)
        target.write_bytes(b"my existing cheats")
        with self.assertRaises(FileExistsError):
            install(self.root, self.content)
        self.assertEqual(target.read_bytes(), b"my existing cheats")
        self.assertFalse((self.root / FILES[0]).exists())


if __name__ == "__main__":
    unittest.main()
