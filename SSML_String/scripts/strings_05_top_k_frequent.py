

import sys
import unittest
from collections import Counter
import heapq

def top_k_frequent_sort(words, k):
    """
    Counter + sort solution.
    Sort by (-freq, word) and return first k words.
    """
    cnt = Counter(words)
    ordered = sorted(cnt.items(), key=lambda x: (-x[1], x[0]))
    return [w for w, _ in ordered[:k]]

def top_k_frequent_heap(words, k):
    """
    Min-heap solution for large streams.
    Keep heap of size k with ordering by (freq asc, word desc),
    so the smallest-by-rules item is popped first.
    """
    cnt = Counter(words)
    heap = []
    for w, f in cnt.items():
        # Python's heap is min-heap; to prefer lexicographically smaller words
        # on ties of frequency, we push (-ord) by reversing word order via a trick:
        # We want to eject lexicographically larger words first at equal freq,
        # so we keep (f, -word) equivalently by using a tuple (f, reverse_flag, w).
        # Simpler: use (f, -ord) is messy; instead store (f, invert word ordering)
        # Use (f, WordNeg(w)) by pushing (f, tuple of negative code points) is overkill.
        # Easiest: push (f, ReverseLex(w)) simulated by using (f, -w) not possible.
        # Practical approach: push (f, -1*alphabetic rank) is not clean either.
        # Therefore a standard trick: store (f, WordWrap) where WordWrap compares inverted.
        # Python heapq doesn't allow custom comparators, so we'll invert by storing (f, Invert(w)).
        # We'll store (f, Inverter(w)) where Inverter has __lt__ reversed. Keep it simple:
        heapq.heappush(heap, (f, _Rev(w)))
        if len(heap) > k:
            heapq.heappop(heap)
    # extract and sort by our final required ordering (-freq, word)
    result = [item[1].s for item in heap]
    result.sort(key=lambda w: (-cnt[w], w))
    return result

class _Rev:
    """
    Helper wrapper to invert lexicographic ordering inside the heap for ties.
    We want the heap (which pops smallest) to treat lexicographically *larger* words as smaller,
    so they are popped first when heap exceeds size k.
    """
    __slots__ = ("s",)
    def __init__(self, s): self.s = s
    def __lt__(self, other):  # invert normal order
        return self.s > other.s

# -------- sample runner --------

def _run_samples():
    samples = [
        (["the","day","is","sunny","the","the","the","sunny","is","is"], 2),
        (["i","love","leetcode","i","love","coding"], 2),
        ([], 3),
        (["a","b","c"], 5),
        (["Z","z","z","Z","a","A","A","a"], 2),
    ]
    for words, k in samples:
        print(f"WORDS: {words} | k={k}")
        print(" sort:", top_k_frequent_sort(words, k))
        print(" heap:", top_k_frequent_heap(words, k))
        print("-" * 60)

# -------- unit tests (built-in) --------

class TestTopKFrequent(unittest.TestCase):
    def test_examples(self):
        words = ["the","day","is","sunny","the","the","the","sunny","is","is"]
        self.assertEqual(top_k_frequent_sort(words, 2), ["the","is"])
        self.assertEqual(top_k_frequent_heap(words, 2), ["the","is"])

    def test_basic(self):
        words = ["i","love","leetcode","i","love","coding"]
        self.assertEqual(top_k_frequent_sort(words, 2), ["i","love"])
        self.assertEqual(top_k_frequent_heap(words, 2), ["i","love"])

    def test_empty(self):
        self.assertEqual(top_k_frequent_sort([], 3), [])
        self.assertEqual(top_k_frequent_heap([], 3), [])

    def test_k_larger(self):
        self.assertEqual(top_k_frequent_sort(["a","b","c"], 5), ["a","b","c"])
        self.assertEqual(top_k_frequent_heap(["a","b","c"], 5), ["a","b","c"])

    def test_case_sensitive(self):
        words = ["Z","z","z","Z","a","A","A","a"]
        # counts: A=2, Z=2, a=2, z=2 -> tie by lexicographic
        # lexicographic ascending: 'A' < 'Z' < 'a' < 'z'
        self.assertEqual(top_k_frequent_sort(words, 2), ["A","Z"])
        self.assertEqual(top_k_frequent_heap(words, 2), ["A","Z"])

if __name__ == "__main__":
    if "--tests" in sys.argv:
        unittest.main(argv=[sys.argv[0]])
    else:
        _run_samples()