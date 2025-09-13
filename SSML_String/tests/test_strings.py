import unittest
from src.strings.reverse_words import reverse_words
from src.strings.is_valid_tags import is_well_formed_markup
from src.strings.sliding_window_substring import length_of_longest_substring_no_repeat
from src.strings.top_k_freq import top_k_frequent_words

class TestStrings(unittest.TestCase):
    def test_reverse_words(self):
        self.assertEqual(reverse_words("  hello   world "), "world hello")

    def test_valid_markup(self):
        self.assertTrue(is_well_formed_markup("<a><b></b><c/></a>"))
        self.assertFalse(is_well_formed_markup("<a><b></a></b>"))
        self.assertFalse(is_well_formed_markup("<a>"))

    def test_longest_substring(self):
        self.assertEqual(length_of_longest_substring_no_repeat("abcabcbb"), 3)
        self.assertEqual(length_of_longest_substring_no_repeat("bbbbb"), 1)
        self.assertEqual(length_of_longest_substring_no_repeat("pwwkew"), 3)

    def test_top_k_freq(self):
        words = "the day is sunny the the the sunny is is".split()
        self.assertEqual(top_k_frequent_words(words, 2), ["the", "is"])

if __name__ == "__main__":
    unittest.main()
