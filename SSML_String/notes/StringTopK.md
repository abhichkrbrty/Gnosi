# 🔢 Top-K Frequent Words

## 📌 Problem
Given a list of words (strings) and an integer `k`, return the **k most frequent words**.

- If two words have the same frequency, return them in **lexicographic order** (ascending).
- Assume case-sensitive tokens unless you normalize.

---

## 🔍 Examples
words = [“the”,“day”,“is”,“sunny”,“the”,“the”,“the”,“sunny”,“is”,“is”], k=2
→ [“the”,“is”]

words = [“i”,“love”,“leetcode”,“i”,“love”,“coding”], k=2
→ [“i”,“love”]

---

## 🧠 Ideas & Variants
1) **Counter + sort** (simple & clear)
   - Count with a hash map.
   - Sort by `(-freq, word)`.
   - Return first `k`.
2) **Min-heap of size k** (good for streaming/very large inputs)
   - Push pairs with custom order (freq ascending, word descending for tiebreak).
   - Pop when size > k.
   - Extract and reverse at the end.

**Trade-off**
- Sort: `O(n log n)` on distinct words `n`.
- Heap: `O(n log k)`; better when `k << n`.

---

## 🧪 Edge Cases
- `k` ≥ number of distinct words → return all.
- Mixed case: `"The"` vs `"the"` (decide normalization).
- Punctuation: decide tokenization strategy (out of scope here).
- Empty input → `[]`.

---

## ✅ Acceptance Criteria
- Correct frequency counting.
- Tie-break by word lexicographically (ascending).
- Deterministic, stable for equal frequencies.

---

## 📂 File & Run
Create: `scripts/strings_05_top_k_frequent.py`

Run samples:
```bash
python3 scripts/strings_05_top_k_frequent.py