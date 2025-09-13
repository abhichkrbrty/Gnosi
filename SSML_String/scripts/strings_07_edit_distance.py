

import sys
import unittest

def edit_distance(a: str, b: str) -> int:
    """
    Levenshtein distance with unit costs for insert/delete/substitute.
    Returns the minimal number of edits to transform a -> b.
    """
    m, n = len(a), len(b)
    dp = [[0]*(n+1) for _ in range(m+1)]
    for i in range(1, m+1):
        dp[i][0] = i
    for j in range(1, n+1):
        dp[0][j] = j
    for i in range(1, m+1):
        ai = a[i-1]
        for j in range(1, n+1):
            bj = b[j-1]
            if ai == bj:
                dp[i][j] = dp[i-1][j-1]
            else:
                dp[i][j] = 1 + min(
                    dp[i-1][j],     # delete ai
                    dp[i][j-1],     # insert bj
                    dp[i-1][j-1],   # substitute ai->bj
                )
    return dp[m][n]

def edit_script(a: str, b: str):
    """
    Return (distance, ops) where ops is a list of (op, src_char, dst_char, i, j)
    describing a deterministic sequence from a -> b.
    op in {"match","sub","ins","del"}.
    (i,j) are 1-based positions in DP table after applying the operation.
    """
    m, n = len(a), len(b)
    dp = [[0]*(n+1) for _ in range(m+1)]
    for i in range(1, m+1):
        dp[i][0] = i
    for j in range(1, n+1):
        dp[0][j] = j
    for i in range(1, m+1):
        ai = a[i-1]
        for j in range(1, n+1):
            bj = b[j-1]
            if ai == bj:
                dp[i][j] = dp[i-1][j-1]
            else:
                dp[i][j] = 1 + min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])

    # backtrack with deterministic tie-breaking:
    # prefer match > sub > ins > del
    ops = []
    i, j = m, n
    while i > 0 or j > 0:
        if i > 0 and j > 0 and a[i-1] == b[j-1] and dp[i][j] == dp[i-1][j-1]:
            ops.append(("match", a[i-1], b[j-1], i, j))
            i, j = i-1, j-1
        else:
            # compute candidate costs (guard edges)
            del_cost = dp[i-1][j] if i > 0 else float("inf")
            ins_cost = dp[i][j-1] if j > 0 else float("inf")
            sub_cost = dp[i-1][j-1] if i > 0 and j > 0 else float("inf")
            best_prev = min(del_cost, ins_cost, sub_cost)
            # choose by priority: sub > ins > del (all +1 to reach dp[i][j])
            if j > 0 and i > 0 and sub_cost == best_prev and dp[i][j] == sub_cost + 1:
                ops.append(("sub", a[i-1], b[j-1], i, j))
                i, j = i-1, j-1
            elif j > 0 and ins_cost == best_prev and dp[i][j] == ins_cost + 1:
                ops.append(("ins", "", b[j-1], i, j))
                j = j-1
            elif i > 0 and del_cost == best_prev and dp[i][j] == del_cost + 1:
                ops.append(("del", a[i-1], "", i, j))
                i = i-1
            else:
                # fallback (shouldn't happen)
                if i > 0:
                    ops.append(("del", a[i-1], "", i, j))
                    i -= 1
                elif j > 0:
                    ops.append(("ins", "", b[j-1], i, j))
                    j -= 1
    ops.reverse()
    return dp[m][n], ops

# -------- sample runner --------

def _run_samples():
    pairs = [
        ("kitten", "sitting"),
        ("intention", "execution"),
        ("", "abc"),
        ("abc", "abc"),
        ("flaw", "lawn"),
    ]
    for a, b in pairs:
        print(f"a={a!r}, b={b!r} -> dist={edit_distance(a,b)}")
    print("-"*50)

def _run_ops_demo():
    pairs = [
        ("kitten", "sitting"),
        ("flaw", "lawn"),
    ]
    for a, b in pairs:
        d, ops = edit_script(a, b)
        print(f"a={a!r}, b={b!r} -> dist={d}")
        for op, src, dst, i, j in ops:
            print(f"  {op:5s}  {src!r:>3} -> {dst!r:<3}  @ dp[{i},{j}]")
        print("-"*50)

# -------- unit tests (built-in) --------

class TestEditDistance(unittest.TestCase):
    def test_classics(self):
        self.assertEqual(edit_distance("kitten", "sitting"), 3)
        self.assertEqual(edit_distance("intention", "execution"), 5)
        self.assertEqual(edit_distance("", "abc"), 3)
        self.assertEqual(edit_distance("abc", "abc"), 0)
        self.assertEqual(edit_distance("flaw", "lawn"), 2)

    def test_unicode(self):
        self.assertEqual(edit_distance("résumé", "resume"), 2)  # two substitutions (é->e twice)

    def test_ops_consistency(self):
        for a, b in [("kitten","sitting"), ("flaw","lawn"), ("","abc"), ("abc","")]:
            d = edit_distance(a, b)
            d2, ops = edit_script(a, b)
            self.assertEqual(d, d2)
            # applying ops length equals distance when counting non-"match"
            steps = sum(1 for op, *_ in ops if op != "match")
            self.assertEqual(steps, d)

if __name__ == "__main__":
    if "--tests" in sys.argv:
        unittest.main(argv=[sys.argv[0]])
    elif "--ops" in sys.argv:
        _run_ops_demo()
    else:
        _run_samples()