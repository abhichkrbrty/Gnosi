

import sys
import unittest

def reverse_words(s: str) -> str:
    """
    Reverse the order of words in a string.
    - Words are sequences of non-space characters.
    - Extra whitespace is ignored.
    - Output uses single spaces.
    """
    return " ".join(reversed(s.split()))

# -------- sample runner --------

def _run_samples():
    samples = [
        "  hello   world  ",
        "a good   example",
        "single",
        "",
        "  a  b\tc\n",
        "hello,   world!",
        "  multiple     \t   spaces   here  "
    ]
    for s in samples:
        print(f"IN : {s!r}")
        print(f"OUT: {reverse_words(s)!r}")
        print("-" * 40)

# -------- unit tests (built-in) --------

class TestReverseWords(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(reverse_words("  hello   world  "), "world hello")
        self.assertEqual(reverse_words("a good   example"), "example good a")
        self.assertEqual(reverse_words("single"), "single")
        self.assertEqual(reverse_words(""), "")

    def test_whitespace_variants(self):
        self.assertEqual(reverse_words("  a  b\tc\n"), "c b a")
        self.assertEqual(reverse_words("   \t  \n "), "")  # only whitespace

    def test_punctuation(self):
        self.assertEqual(reverse_words("hello,   world!"), "world! hello,")
        self.assertEqual(reverse_words("wow...  yes!"), "yes! wow...")

    def test_long(self):
        s = " ".join(str(i) for i in range(1000))
        expected = " ".join(str(i) for i in reversed(range(1000)))
        self.assertEqual(reverse_words(s), expected)

if __name__ == "__main__":
    if "--tests" in sys.argv:
        # run unit tests
        unittest.main(argv=[sys.argv[0]])
    else:
        # run samples
        _run_samples()