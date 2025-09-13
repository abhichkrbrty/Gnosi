

import sys
import unittest
from collections import Counter

def min_window(s: str, t: str) -> str:
    """
    Return the smallest window in s containing all characters of t (with multiplicities).
    Sliding window with frequency maps and two pointers.
    """
    if not s or not t or len(t) > len(s):
        return ""

    need = Counter(t)
    have = Counter()
    required = len(need)
    formed = 0

    best_len = float("inf")
    best_range = (0, 0)

    L = 0
    for R, ch in enumerate(s):
        have[ch] += 1
        if ch in need and have[ch] == need[ch]:
            formed += 1

        # Try shrink while valid
        while formed == required:
            if (R - L + 1) < best_len:
                best_len = R - L + 1
                best_range = (L, R)

            left_ch = s[L]
            have[left_ch] -= 1
            if left_ch in need and have[left_ch] < need[left_ch]:
                formed -= 1
            L += 1

    if best_len == float("inf"):
        return ""
    a, b = best_range
    return s[a:b+1]

# -------- sample runner --------

def _run_samples():
    samples = [
        ("ADOBECODEBANC", "ABC"),
        ("a", "aa"),
        ("aaflslflsldkalskaaa", "aaa"),
        ("ab", "b"),
        ("ab", "A"),
        ("aa", "aa"),
        ("", "a"),
    ]
    for s, t in samples:
        print(f"s={s!r}, t={t!r}  ->  {min_window(s, t)!r}")
        print("-" * 40)

# -------- unit tests (built-in) --------

class TestMinWindow(unittest.TestCase):
    def test_examples(self):
        self.assertEqual(min_window("ADOBECODEBANC", "ABC"), "BANC")
        self.assertEqual(min_window("a", "aa"), "")
        self.assertEqual(min_window("aaflslflsldkalskaaa", "aaa"), "aaa")

    def test_basic(self):
        self.assertEqual(min_window("ab", "b"), "b")
        self.assertEqual(min_window("aa", "aa"), "aa")
        self.assertEqual(min_window("ab", "A"), "")  # case sensitive

    def test_empty(self):
        self.assertEqual(min_window("", "a"), "")
        self.assertEqual(min_window("a", ""), "")

    def test_more(self):
        self.assertEqual(min_window("bba", "ab"), "ba")
        self.assertEqual(min_window("cabefgecdaecf", "cae"), "aec")

if __name__ == "__main__":
    if "--tests" in sys.argv:
        unittest.main(argv=[sys.argv[0]])
    else:
        _run_samples()