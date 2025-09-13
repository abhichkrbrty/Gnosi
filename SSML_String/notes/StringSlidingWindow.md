# 🚪 Sliding Window: Longest Substring Without Repeating Characters

## 📌 Problem
Given a string `s`, return the **length** of the longest substring that contains **no repeated characters**.

- Substring = contiguous block of characters.
- Characters can be letters, digits, symbols, or Unicode.

---

## 🧠 Why It’s Important
- Canonical sliding-window interview problem.
- Tests:
  - Two-pointer technique
  - Hash map usage for last-seen indices
  - Off-by-one traps and window maintenance

---

## 🔍 Examples

“abcabcbb”  → 3    (“abc”)
“bbbbb”     → 1    (“b”)
“pwwkew”    → 3    (“wke”)
“”          → 0
“dvdf”      → 3    (“vdf”)

---

## 🧩 Core Idea (Sliding Window)
Maintain a window `[left, right]` with all unique chars.

For each `right`:
- If `s[right]` was seen **inside** the current window, **move `left`** to `last_seen[s[right]] + 1` (never move left backward).
- Update `last_seen[s[right]] = right`.
- Update `best = max(best, right - left + 1)`.

This ensures the window always has **no duplicates**.

---

## ⏱️ Complexity
- **Time**: `O(n)` — each index enters/leaves the window at most once.  
- **Space**: `O(min(n, |Σ|))` — map of last positions (Σ: character set).

---

## ✅ Acceptance Criteria
- Works on empty string.
- Handles repeated blocks and interleaved duplicates.
- Handles Unicode (Python `dict` works fine).

---

## 🧪 Edge Cases
- All unique (answer = `len(s)`).
- All same (answer = `1`).
- Repeats right at window boundary (correctly shift `left`).