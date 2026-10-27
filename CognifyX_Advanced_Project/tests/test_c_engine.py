"""Small standard-library regression checks for the CognifyX C engine."""
import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "c_engine" / "cognifyx_engine.c"


class CEngineTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        compiler = shutil.which("gcc") or shutil.which("clang")
        if not compiler:
            raise unittest.SkipTest("GCC/Clang not available; install a C compiler to run engine tests")
        cls.temp = tempfile.TemporaryDirectory(prefix="cognifyx_test_")
        cls.binary = Path(cls.temp.name) / ("engine.exe" if __import__("os").name == "nt" else "engine")
        subprocess.run([compiler, "-std=c11", "-O2", "-Wall", "-Wextra", str(SOURCE), "-o", str(cls.binary)], check=True)

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, "temp"):
            cls.temp.cleanup()

    def run_json(self, *args):
        result = subprocess.run([str(self.binary), *map(str, args)], text=True, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        return json.loads(result.stdout)

    def test_scoring(self):
        result = self.run_json("score", 7, 2, 1, 402, 10)
        self.assertEqual(result["score"], 26)
        self.assertEqual(result["max_score"], 40)
        self.assertAlmostEqual(result["accuracy"], 77.78, places=2)
        self.assertAlmostEqual(result["percentage"], 65.00, places=2)

    def test_adaptive_level_moves_up_after_correct_answer(self):
        result = self.run_json("adapt", 2, 1)
        self.assertEqual(result["next_level"], 3)
        self.assertEqual(result["difficulty"], "Hard")

    def test_adaptive_level_moves_down_after_wrong_answer(self):
        result = self.run_json("adapt", 2, 0)
        self.assertEqual(result["next_level"], 1)
        self.assertEqual(result["difficulty"], "Easy")

    def test_adaptation_is_bounded(self):
        self.assertEqual(self.run_json("adapt", 3, 1)["next_level"], 3)
        self.assertEqual(self.run_json("adapt", 1, 0)["next_level"], 1)

    def test_weakest_category_recommendation(self):
        result = self.run_json("recommend", 62, 82, 74, 78)
        self.assertEqual(result["weakest_category"], "Quantitative Aptitude")

    def test_invalid_counts_are_rejected(self):
        result = subprocess.run([str(self.binary), "score", "7", "2", "0", "10", "10"], text=True, capture_output=True)
        self.assertNotEqual(result.returncode, 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
