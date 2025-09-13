import unittest
from pathlib import Path
from src.ssml.simple_etree import parse_ssml
from src.ssml.transforms import flatten_text, total_duration_seconds, validate_ssml

class TestSSML(unittest.TestCase):
    def setUp(self):
        self.txt = Path("src/ssml/examples/sample1.xml").read_text(encoding="utf-8")
        self.root = parse_ssml(self.txt)

    def test_validate(self):
        validate_ssml(self.root)  # should not raise

    def test_flatten(self):
        flat = flatten_text(self.root)
        self.assertIn("Hello NYC fans!", flat)
        self.assertIn("This is a quick demo.", flat)

    def test_duration(self):
        dur = total_duration_seconds(self.root, wpm=180)
        self.assertGreater(dur, 0.5)  # includes break(0.5s)
        self.assertLess(dur, 10.0)

if __name__ == "__main__":
    unittest.main()
