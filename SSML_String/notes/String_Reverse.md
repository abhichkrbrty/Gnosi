# 🔄 Reverse Words in a String

## ✅ Problem
Given a string `s`, return a new string with the **order of words reversed**.

- A *word* is a maximal sequence of non-space characters.
- Ignore extra spaces (leading, trailing, multiple between words).
- Output uses **single spaces** between words.

---

## 🧪 Examples
- `s = "  hello   world  "` → `"world hello"`
- `s = "a good   example"` → `"example good a"`
- `s = "single"` → `"single"`
- `s = ""` → `""`
- `s = "  a  b\tc\n"` → `"c b a"`  (tabs/newlines are whitespace)

---

## 🧠 Key Points & Pitfalls
- `.split()` without arguments splits on **any** whitespace and collapses multiples.
- Don’t forget to **normalize** spaces in output via `" ".join(...)`.
- Preserve punctuation **inside words** (we are not re-punctuating):  
  `"hello, world!"` → `"world! hello,"`
- Unicode & whitespace: Python’s `.split()` handles `\t`, `\n`, non-breaking spaces, etc.

---

## 🚀 Approaches
1) **Pythonic (recommended)**  
   ```py
   " ".join(reversed(s.split()))