import sys
import unittest
from collections import Counter, defaultdict, deque

# ============================================================
# String Utilities: "All-in-One" reference implementations
# Each function has:
#   - Clear docstring with idea + complexity
#   - Minimal dependencies (stdlib only)
#   - Deterministic behavior for easy testing
# ============================================================

def reverse_words(s: str) -> str:
    """
    Reverse the order of words; collapse extra whitespace.
    Idea: split by whitespace, reverse list, join with single spaces.
    Time: O(n), Space: O(n)
    """
    return " ".join(reversed(s.split()))

def is_valid_brackets(s: str) -> bool:
    """
    Validate (), [], {} using a stack (LIFO).
    Ignore non-bracket characters.
    Time: O(n), Space: O(n)
    """
    close_to_open = {')': '(', ']': '[', '}': '{'}
    opens = set(close_to_open.values())
    st = []
    for ch in s:
        if ch in opens:
            st.append(ch)
        elif ch in close_to_open:
            if not st or st[-1] != close_to_open[ch]:
                return False
            st.pop()
    return not st

def length_of_longest_substring_no_repeat(s: str) -> int:
    """
    Sliding window with last-seen map; keep window unique.
    Time: O(n), Space: O(min(n, |Σ|))
    """
    last = {}
    left = 0
    best = 0
    for right, ch in enumerate(s):
        if ch in last and last[ch] >= left:
            left = last[ch] + 1
        last[ch] = right
        best = max(best, right - left + 1)
    return best

def min_window(s: str, t: str) -> str:
    """
    Minimum window in s containing all chars of t (with multiplicities).
    Sliding window + two hash maps.
    Time: O(|s| + |t|), Space: O(|Σ|)
    """
    if not s or not t or len(t) > len(s):
        return ""
    need = Counter(t)
    have = Counter()
    required = len(need)
    formed = 0
    best_len = float("inf")
    best = (0, 0)
    L = 0
    for R, ch in enumerate(s):
        have[ch] += 1
        if ch in need and have[ch] == need[ch]:
            formed += 1
        while formed == required:
            if R - L + 1 < best_len:
                best_len = R - L + 1
                best = (L, R)
            left_ch = s[L]
            have[left_ch] -= 1
            if left_ch in need and have[left_ch] < need[left_ch]:
                formed -= 1
            L += 1
    return "" if best_len == float("inf") else s[best[0]:best[1]+1]

def top_k_frequent_words(words, k):
    """
    Count words, return top-k by (-freq, word).
    Time: O(n log n) on distinct words, Space: O(n)
    """
    cnt = Counter(words)
    ordered = sorted(cnt.items(), key=lambda x: (-x[1], x[0]))
    return [w for w, _ in ordered[:k]]

def group_anagrams_sort(words, case_sensitive=True):
    """
    Group anagrams via sorted-string key.
    Time: O(n * L log L), Space: O(n * L)
    """
    groups = defaultdict(list)
    for w in words:
        key = "".join(sorted(w if case_sensitive else w.lower()))
        groups[key].append(w)
    out = [sorted(g) for g in groups.values()]
    out.sort(key=lambda g: (g[0], len(g), g))
    return out

def group_anagrams_count(words, case_sensitive=True):
    """
    Group anagrams via frequency-count key (supports Unicode via Counter).
    Time: O(n * (L + Σ)), Space: O(n * Σ)
    """
    groups = defaultdict(list)
    for w in words:
        base = w if case_sensitive else w.lower()
        key = tuple(sorted(Counter(base).items()))
        groups[key].append(w)
    out = [sorted(g) for g in groups.values()]
    out.sort(key=lambda g: (g[0], len(g), g))
    return out

def edit_distance(a: str, b: str) -> int:
    """
    Levenshtein (insert/delete/substitute = 1).
    DP table dp[i][j] = distance(a[:i], b[:j]).
    Time: O(mn), Space: O(mn)
    """
    m, n = len(a), len(b)
    dp = [[0]*(n+1) for _ in range(m+1)]
    for i in range(1, m+1): dp[i][0] = i
    for j in range(1, n+1): dp[0][j] = j
    for i in range(1, m+1):
        ai = a[i-1]
        for j in range(1, n+1):
            bj = b[j-1]
            if ai == bj:
                dp[i][j] = dp[i-1][j-1]
            else:
                dp[i][j] = 1 + min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])
    return dp[m][n]

# ---------- More “grab-bag” string questions (quick, commented) ----------

def is_anagram(a: str, b: str) -> bool:
    """
    Check if two strings are anagrams (case-sensitive).
    Time: O(n), Space: O(1) if alphabet fixed; else O(n)
    """
    return Counter(a) == Counter(b)

def first_unique_char(s: str) -> int:
    """
    Return index of first non-repeating character; -1 if none.
    Time: O(n), Space: O(n)
    """
    cnt = Counter(s)
    for i, ch in enumerate(s):
        if cnt[ch] == 1:
            return i
    return -1

def is_isomorphic(s: str, t: str) -> bool:
    """
    Two strings are isomorphic if a one-to-one mapping exists from s chars to t chars.
    Time: O(n), Space: O(Σ)
    """
    if len(s) != len(t): return False
    map_st, map_tst = {}, set()
    for a, b in zip(s, t):
        if a in map_st:
            if map_st[a] != b: return False
        else:
            if b in map_tst: return False
            map_st[a] = b
            map_tst.add(b)
    return True

def valid_palindrome_alnum(s: str) -> bool:
    """
    Check palindrome ignoring non-alphanumeric and case.
    Two pointers from both ends.
    Time: O(n), Space: O(1)
    """
    i, j = 0, len(s)-1
    while i < j:
        while i < j and not s[i].isalnum(): i += 1
        while i < j and not s[j].isalnum(): j -= 1
        if s[i].lower() != s[j].lower(): return False
        i += 1; j -= 1
    return True

def longest_common_prefix(strs) -> str:
    """
    LCP across strings by vertical scanning.
    Time: O(sum of lengths), Space: O(1)
    """
    if not strs: return ""
    shortest = min(strs, key=len)
    for i, ch in enumerate(shortest):
        for s in strs:
            if s[i] != ch:
                return shortest[:i]
    return shortest

def str_str(haystack: str, needle: str) -> int:
    """
    Substring search (KMP for O(n+m)). Here: simple linear scan for clarity.
    Time: O(n*m) worst-case; OK for interview scaffolding.
    """
    if needle == "": return 0
    n, m = len(haystack), len(needle)
    for i in range(n - m + 1):
        if haystack[i:i+m] == needle:
            return i
    return -1

def roman_to_int(s: str) -> int:
    """
    Convert Roman numeral to integer.
    Handles subtraction pairs (IV, IX, XL, XC, CD, CM).
    Time: O(n)
    """
    val = {'I':1,'V':5,'X':10,'L':50,'C':100,'D':200//2,'M':1000}  # D=500 (kept simple)
    val['D'] = 500
    total = 0
    i = 0
    while i < len(s):
        if i+1 < len(s) and val[s[i]] < val[s[i+1]]:
            total += val[s[i+1]] - val[s[i]]
            i += 2
        else:
            total += val[s[i]]
            i += 1
    return total

def add_binary(a: str, b: str) -> str:
    """
    Add two binary strings.
    Time: O(max(n, m)), Space: O(1) excluding output
    """
    i, j, carry, out = len(a)-1, len(b)-1, 0, []
    while i >= 0 or j >= 0 or carry:
        s = carry
        if i >= 0: s += ord(a[i]) - 48; i -= 1
        if j >= 0: s += ord(b[j]) - 48; j -= 1
        out.append(str(s & 1))
        carry = 1 if s > 1 else 0
    return "".join(reversed(out))

def rotate_string(s: str, goal: str) -> bool:
    """
    Check if goal is a rotation of s (e.g., 'abcde' -> 'cdeab').
    Trick: goal in (s+s)
    Time: O(n), Space: O(n)
    """
    return len(s) == len(goal) and goal in (s + s)

# ============================================================
# Samples + test harness
# ============================================================

def _run_samples():
    print("reverse_words:", reverse_words("  hello   world  "))
    print("is_valid_brackets:", is_valid_brackets("a(b[c]{d}e)f"))
    print("length_of_longest_substring_no_repeat:", length_of_longest_substring_no_repeat("pwwkew"))
    print("min_window:", min_window("ADOBECODEBANC", "ABC"))
    print("top_k_frequent_words:", top_k_frequent_words("the day is sunny the the the sunny is is".split(), 2))
    print("group_anagrams_sort:", group_anagrams_sort(["eat","tea","tan","ate","nat","bat"]))
    print("edit_distance('kitten','sitting'):", edit_distance("kitten","sitting"))
    print("is_anagram:", is_anagram("listen", "silent"))
    print("first_unique_char:", first_unique_char("leetcode"))
    print("is_isomorphic:", is_isomorphic("egg","add"))
    print("valid_palindrome_alnum:", valid_palindrome_alnum("A man, a plan, a canal: Panama"))
    print("longest_common_prefix:", longest_common_prefix(["flower","flow","flight"]))
    print("str_str:", str_str("hello", "ll"))
    print("roman_to_int:", roman_to_int("MCMXCIV"))  # 1994
    print("add_binary:", add_binary("1010","1011"))
    print("rotate_string:", rotate_string("abcde", "cdeab"))

class TestAllInOne(unittest.TestCase):
    def test_core(self):
        self.assertEqual(reverse_words("  hello   world  "), "world hello")
        self.assertTrue(is_valid_brackets("{[()]}"))
        self.assertEqual(length_of_longest_substring_no_repeat("abcabcbb"), 3)
        self.assertEqual(min_window("ADOBECODEBANC", "ABC"), "BANC")
        self.assertEqual(top_k_frequent_words(["i","love","leetcode","i","love","coding"], 2), ["i","love"])
        self.assertEqual(edit_distance("flaw","lawn"), 2)
    def test_misc(self):
        self.assertTrue(is_anagram("anagram","nagaram"))
        self.assertEqual(first_unique_char("leetcode"), 0)
        self.assertTrue(is_isomorphic("paper","title"))
        self.assertTrue(valid_palindrome_alnum("A man, a plan, a canal: Panama"))
        self.assertEqual(longest_common_prefix(["cir","car"]), "c")
        self.assertEqual(str_str("aaaaa","bba"), -1)
        self.assertEqual(roman_to_int("LVIII"), 58)
        self.assertEqual(add_binary("11","1"), "100")
        self.assertTrue(rotate_string("abcde","cdeab"))

if __name__ == "__main__":
    if "--tests" in sys.argv:
        unittest.main(argv=[sys.argv[0]])
    else:
        _run_samples()