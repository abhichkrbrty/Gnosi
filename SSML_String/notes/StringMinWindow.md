# 🎯 Minimum Window Substring

## 📌 Problem
Given two strings `s` and `t`, return the **minimum window** in `s` which contains **all the characters** of `t` (including multiplicities).  
If no such window exists, return `""`.

- Characters are case-sensitive.
- Multiplicity matters (if `t = "AABC"`, window must have two `A`s, one `B`, one `C`).

---

## 🔍 Examples

s = “ADOBECODEBANC”, t = “ABC”  → “BANC”
s = “a”, t = “aa”               → “”
s = “aaflslflsldkalskaaa”, t=“aaa” → “aaa”

---

## 🧠 Idea (Sliding Window + Frequency Maps)
We keep a window `[L..R]` over `s` and maintain:
- `need`: frequency map of chars required by `t`
- `have`: frequency map inside current window
- `formed`: number of distinct chars whose `have[c] >= need[c]`
- `required = len(need)`

Algorithm:
1. Expand `R` rightwards, include `s[R]` → update `have`, maybe increase `formed`.
2. When `formed == required`, try **shrink from left** (advance `L`) to minimize window while still valid.
3. Track the best window length and start index.

---

## ⏱️ Complexity
- **Time**: `O(|s| + |t|)` — each pointer moves at most `|s|` steps; dict ops are amortized `O(1)`.
- **Space**: `O(|Σ|)` — character maps (bounded by alphabet size).

---

## 🧪 Edge Cases
- `t` longer than `s` → `""`
- `t` contains chars not in `s` → `""`
- Repeated characters in `t`
- Multiple optimal windows — any min one is fine.

---

## ✅ Acceptance Criteria
- Returns exact minimal window (shortest length).
- Preserves order from `s`.
- Works with any ASCII/Unicode characters.

---

## 📂 File & Run
Create: `scripts/strings_04_min_window_substring.py`

Run samples:
```bash
python3 scripts/strings_04_min_window_substring.py