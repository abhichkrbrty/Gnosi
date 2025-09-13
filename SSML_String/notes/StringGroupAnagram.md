# 🔗 Group Anagrams

## 📌 Problem
Given a list of strings, group together the **anagrams**.  
Two words are anagrams if they contain the **same letters with the same multiplicities**, possibly in a different order.

---

## 🔍 Examples
[“eat”,“tea”,“tan”,“ate”,“nat”,“bat”]
→ [[“eat”,“tea”,“ate”], [“tan”,“nat”], [“bat”]]

[””] → [[””]]
[“a”] → [[“a”]]

---

## 🧠 Approaches

### 1) Sort-as-Key (simple & fast in practice)
- Key idea: sort the characters of each word — anagrams share the same sorted form.
- Key: `"aet"` for `"eat"`, `"tea"`, `"ate"`.
- Time: O(n * L log L) where n = number of words, L = max word length.

```py
key = "".join(sorted(word))
groups[key].append(word)

2) Frequency-Count Key (better when L is large)
	•	Key idea: use a 26-length tuple of character counts (assuming lowercase a–z) or a full Counter for Unicode.
	•	Time: O(n * (L + Σ)) where Σ is alphabet size (26 for lowercase).
	•	Avoids the per-word sort when strings are long.


freq = [0]*26
for ch in word: freq[ord(ch)-97] += 1
key = tuple(freq)
groups[key].append(word)

⚙️ Normalization Choices
	•	Case sensitivity: Decide whether "Eat" and "tea" are the same group.
	•	If you want case-insensitive grouping, convert to lowercase first.
	•	Whitespace/punctuation: Typically preserved; anagrams consider every character.
	•	Deterministic output:
	•	Sort each group alphabetically.
	•	Sort groups by their first element (or by length then lexicographic) for stable displays/tests.

⸻

⏱️ Complexity
	•	Sort-as-Key: O(n * L log L)
	•	Count-as-Key: O(n * (L + Σ)) (Σ=26 for lowercase) — faster for very long strings.

⸻

✅ Acceptance Criteria
	•	All anagrams are grouped together.
	•	No word is dropped/duplicated.
	•	Output order deterministic (for tests), or verify via set-of-frozensets.