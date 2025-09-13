# ✅ Valid Parentheses (Bracket Matching with a Stack)

## 📌 Problem
Given a string `s` consisting of bracket characters `()[]{}`, determine if it is **valid**:
- Every **opening** bracket must be closed by the same type.
- Brackets must be closed in the **correct order**.
- Any other (non-bracket) characters can be ignored (optional behavior; see variants).

---

## 🧠 Why It’s Important
- Classic stack problem used to check understanding of **LIFO** structures.
- Forms the base for **parser** tasks (e.g., SSML/XML/HTML tag matching after tokenization).
- Teaches careful handling of **edge cases** and **mapping** logic.

---

## 🔍 Examples

“()”         -> True
“()[]{}”     -> True
“(]”         -> False
“([)]”       -> False
“{[]}”       -> True
“”           -> True
“)(”         -> False

---

## 🧩 Core Idea (Stack)
- Use a **stack** to hold opening brackets.
- For each character `c`:
  - If `c` is an **opening** bracket, push it.
  - If `c` is a **closing** bracket, check that the **top** of stack is its matching opener; if so, pop; otherwise invalid.
- At the end, the stack must be **empty**.

**Mapping**

close_to_open = { ‘)’:’(’, ‘]’:’[’, ‘}’:’{’ }

---

## ⏱️ Complexity
- **Time:** `O(n)` — single pass.
- **Space:** `O(n)` worst case (all openings before closings).

---

## 🧪 Variants
1) **Ignore non-bracket characters**: filter them out before processing.
2) **Custom bracket sets**: extend mapping for other delimiters.
3) **Tag matching** (SSML/XML/HTML): same stack idea, but you must **tokenize tags**, not just characters.

---

## ✅ Acceptance Criteria
- Reject when a close bracket appears with an empty stack.
- Reject when types don’t match (e.g., `(` with `]`).
- Valid only if the stack is empty at the end.

---

## 📂 File & Run
Create: `scripts/strings_02_valid_parentheses.py`

Run samples:
```bash
python3 scripts/strings_02_valid_parentheses.py