#!/usr/bin/env python3

import sys
import unittest

def length_of_longest_substring_no_repeat(s: str) -> int:
    """
    Return length of the longest substring without repeating characters.
    Sliding window with last-seen index map.
    """
    last_seen = {}
    left = 0
    best = 0
    for right, ch in enumerate(s):
        if ch in last_seen and last_seen[ch] >= left:
            left = last_seen[ch] + 1
        last_seen[ch] = right
        best = max(best, right - left + 1)
    return best

# -------- sample runner --------

def _run_samples():
    samples = [
        "abcabcbb",
        "bbbbb",
        "pwwkew",
        "",
        "dvdf",
        "anviaj",
        "tmmzuxt",
        "🙂🙃🙂🙃",  # unicode emojis
    ]
    for s in samples:
        print(f"IN : {s!r}")
        print(f"OUT: {length_of_longest_substring_no_repeat(s)}")
        print("-" * 40)

# -------- unit tests (built-in) --------

class TestLongestNoRepeat(unittest.TestCase):
    def test_examples(self):
        self.assertEqual(length_of_longest_substring_no_repeat("abcabcbb"), 3)
        self.assertEqual(length_of_longest_substring_no_repeat("bbbbb"), 1)
        self.assertEqual(length_of_longest_substring_no_repeat("pwwkew"), 3)
        self.assertEqual(length_of_longest_substring_no_repeat(""), 0)
        self.assertEqual(length_of_longest_substring_no_repeat("dvdf"), 3)  # "vdf"

    def test_unicode(self):
        self.assertEqual(length_of_longest_substring_no_repeat("🙂🙃🙂🙃"), 2)

    def test_edges(self):
        self.assertEqual(length_of_longest_substring_no_repeat("a"), 1)
        self.assertEqual(length_of_longest_substring_no_repeat("abca"), 3)
        self.assertEqual(length_of_longest_substring_no_repeat("tmmzuxt"), 5)  # "mzuxt"

    def test_long(self):
        s = "".join(chr(32 + (i % 90)) for i in range(5000))
        self.assertGreaterEqual(length_of_longest_substring_no_repeat(s), 90)

if __name__ == "__main__":
    if "--tests" in sys.argv:
        unittest.main(argv=[sys.argv[0]])
    else:
        _run_samples()