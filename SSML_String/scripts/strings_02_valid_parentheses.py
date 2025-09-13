

import sys
import unittest

def is_valid_brackets(s: str) -> bool:
    """
    Return True if all (), [], {} are balanced and properly nested.
    Non-bracket characters are ignored.
    """
    close_to_open = {')': '(', ']': '[', '}': '{'}
    opens = set(close_to_open.values())
    stack = []

    for ch in s:
        if ch in opens:
            stack.append(ch)
        elif ch in close_to_open:
            if not stack or stack[-1] != close_to_open[ch]:
                return False
            stack.pop()
        else:
            # ignore other characters
            continue

    return len(stack) == 0

# -------- sample runner --------

def _run_samples():
    samples = [
        "()",
        "()[]{}",
        "(]",
        "([)]",
        "{[]}",
        "",
        ")(",
        "a(b[c]{d}e)f",      # with non-brackets
        "((((((((",
        "))))))))",
    ]
    for s in samples:
        print(f"IN : {s!r}")
        print(f"OUT: {is_valid_brackets(s)}")
        print("-" * 40)

# -------- unit tests (built-in) --------

class TestValidBrackets(unittest.TestCase):
    def test_true_cases(self):
        self.assertTrue(is_valid_brackets("()"))
        self.assertTrue(is_valid_brackets("()[]{}"))
        self.assertTrue(is_valid_brackets("{[]}"))
        self.assertTrue(is_valid_brackets(""))
        self.assertTrue(is_valid_brackets("a(b[c]{d}e)f"))

    def test_false_cases(self):
        self.assertFalse(is_valid_brackets("(]"))
        self.assertFalse(is_valid_brackets("([)]"))
        self.assertFalse(is_valid_brackets(")("))
        self.assertFalse(is_valid_brackets("(((((((("))
        self.assertFalse(is_valid_brackets("))))))))"))

    def test_long_mixed(self):
        s = "{[()()[]{}]}()([]{})"
        self.assertTrue(is_valid_brackets(s))
        bad = "{[()()[]{}]}()([]{)"
        self.assertFalse(is_valid_brackets(bad))

if __name__ == "__main__":
    if "--tests" in sys.argv:
        unittest.main(argv=[sys.argv[0]])
    else:
        _run_samples()