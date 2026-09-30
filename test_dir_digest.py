import json
import tempfile
import unittest
from pathlib import Path

import dir_digest


class DirDigestTests(unittest.TestCase):
    def test_human_size(self) -> None:
        self.assertEqual(dir_digest.human_size(512), "512 B")
        self.assertEqual(dir_digest.human_size(2048), "2.0 KB")

    def test_walk_counts_files(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            (root / "a.txt").write_text("hi", encoding="utf-8")
            (root / "nested").mkdir()
            (root / "nested" / "b.txt").write_text("there", encoding="utf-8")
            files, dirs, total_bytes = dir_digest.walk_directory(root)
            self.assertEqual(files, 2)
            self.assertEqual(dirs, 1)
            self.assertGreater(total_bytes, 0)


if __name__ == "__main__":
    unittest.main()
