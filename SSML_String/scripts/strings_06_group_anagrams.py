

import sys
import unittest
from collections import defaultdict, Counter

def group_anagrams_sort(words, case_sensitive=True):
    """
    Group anagrams using the sorted-string as the key.
    Returns a list of groups; each group is a list of words.
    """
    groups = defaultdict(list)
    for w in words:
        key_src = w if case_sensitive else w.lower()
        key = "".join(sorted(key_src))
        groups[key].append(w)
    # make output deterministic: sort each group, then sort groups by their first element
    result = [sorted(g) for g in groups.values()]
    result.sort(key=lambda g: (g[0], len(g), g))
    return result

def group_anagrams_count(words, case_sensitive=True):
    """
    Group anagrams using frequency counts as the key.
    Assumes ASCII letters when case_sensitive=True; for Unicode, use Counter-based key.
    """
    groups = defaultdict(list)
    for w in words:
        key_src = w if case_sensitive else w.lower()
        # Use Counter as key to support broader character sets
        # Convert to a tuple of sorted items for a hashable, deterministic key
        c = Counter(key_src)
        key = tuple(sorted(c.items()))
        groups[key].append(w)
    result = [sorted(g) for g in groups.values()]
    result.sort(key=lambda g: (g[0], len(g), g))
    return result

# -------- sample runner --------

def _run_samples():
    samples = [
        ["eat","tea","tan","ate","nat","bat"],
        [""],
        ["a"],
        ["Tea","Eat","ate","BAT","tab","tap"],  # mixed case
        ["résumé", "sérumé", "ésumér"],        # unicode accents
    ]
    for words in samples:
        print(f"WORDS: {words}")
        print(" sort (case-sensitive):", group_anagrams_sort(words, case_sensitive=True))
        print(" sort (case-insensitive):", group_anagrams_sort(words, case_sensitive=False))
        print(" count (case-sensitive):", group_anagrams_count(words, case_sensitive=True))
        print(" count (case-insensitive):", group_anagrams_count(words, case_sensitive=False))
        print("-" * 80)

# -------- unit tests (built-in) --------

def _normalize(groups):
    """Sort groups and items for comparison."""
    return sorted([tuple(sorted(g)) for g in groups])

class TestGroupAnagrams(unittest.TestCase):
    def test_basic(self):
        words = ["eat","tea","tan","ate","nat","bat"]
        expected = [["ate","eat","tea"], ["bat"], ["nat","tan"]]
        res = group_anagrams_sort(words)
        self.assertEqual(_normalize(res), _normalize(expected))
        res2 = group_anagrams_count(words)
        self.assertEqual(_normalize(res2), _normalize(expected))

    def test_empty_and_single(self):
        self.assertEqual(group_anagrams_sort([""]), [[""]])
        self.assertEqual(group_anagrams_sort(["a"]), [["a"]])

    def test_case_insensitive(self):
        words = ["Tea","Eat","ate","BAT","tab","tap"]
        # case-insensitive: "Tea","Eat","ate" together; "BAT","tab" together; "tap" alone
        res = group_anagrams_sort(words, case_sensitive=False)
        expected = [["Eat","Tea","ate"], ["BAT","tab"], ["tap"]]
        self.assertEqual(_normalize(res), _normalize(expected))

    def test_unicode(self):
        words = ["résumé", "sérumé", "ésumér"]
        # They are anagrams if we consider exact code points; Counter-based key handles that.
        res = group_anagrams_count(words)
        # All should be grouped together if truly anagrams at code-point level.
        self.assertEqual(len(res), 1)
        self.assertEqual(set(res[0]), set(words))

    def test_determinism(self):
        words = ["ab", "ba", "abc", "bca", "cab", "z"]
        r1 = group_anagrams_sort(words)
        r2 = group_anagrams_sort(words[::-1])
        self.assertEqual(r1, r2)  # stable deterministic ordering

if __name__ == "__main__":
    if "--tests" in sys.argv:
        unittest.main(argv=[sys.argv[0]])
    else:
        _run_samples()