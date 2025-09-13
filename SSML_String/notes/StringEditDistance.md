# ✏️ Edit Distance (Levenshtein)

## 📌 Problem
Given two strings `a` and `b`, compute the **minimum number of single-character edits** required to transform `a` into `b`.  
Allowed edits (each cost = 1):
- **Insert**
- **Delete**
- **Substitute** (replace one char with another)

> If substitutions are disallowed and only insert/delete are allowed, this becomes the **LCS**-derived distance; here we use standard Levenshtein (insert/delete/substitute).

---

## 🔍 Examples
a=“kitten”, b=“sitting”  → 3   (kitten → sitten [sub], sitten → sittin [sub], sittin → sitting [ins])
a=“intention”, b=“execution” → 5
a=””, b=“abc” → 3
a=“abc”, b=“abc” → 0

---

## 🧠 Idea (Dynamic Programming)

Let `dp[i][j]` = edit distance between `a[:i]` and `b[:j]`.  
Recurrence:
- Base:
  - `dp[0][j] = j`  (insert j chars)
  - `dp[i][0] = i`  (delete i chars)
- Step:
  - If `a[i-1] == b[j-1]`:  
    `dp[i][j] = dp[i-1][j-1]`
  - Else:  
    `dp[i][j] = 1 + min(dp[i-1][j],     # delete a[i-1]
                         dp[i][j-1],     # insert b[j-1]
                         dp[i-1][j-1])`  # substitute a[i-1]→b[j-1]

Answer is `dp[m][n]` where `m=len(a)`, `n=len(b)`.

---

## ⏱️ Complexity
- **Time:** `O(m·n)`
- **Space:** `O(m·n)` with full table (simplifiable to `O(min(m,n))` for distance only).
- We keep the full table to also reconstruct an **edit script**.

---

## 🧪 Edge Cases
- Empty strings.
- Identical strings.
- Unicode characters (Python strings handle them fine).
- Highly different lengths.

---

## ✅ Acceptance Criteria
- Correct distance for classic examples.
- Optional: recover a **deterministic edit script** (sequence of ops) with priorities:
  1. **Match** (no cost)
  2. **Substitute**
  3. **Insert**
  4. **Delete**

---

## 📂 File & Run
Create: `scripts/strings_07_edit_distance.py`

Run samples:
```bash
python3 scripts/strings_07_edit_distance.py