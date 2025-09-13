# Speechify Platform Prep – Python (SSML + Strings/DSA)

A lightweight practice repo to prepare for Speechify’s 90‑minute manual assessment.
It focuses on **SSML parsing** (no external libs beyond Python stdlib) and **string/DSA fundamentals** you can build on.

> ⚠️ Use this only for **practice before** the real assessment. Do **not** open during the live test.

## ✅ What’s inside

- `src/ssml/` – Minimal SSML utilities
  - `simple_etree.py` – SSML parsing using `xml.etree.ElementTree` (stdlib only)
  - `node.py` – Tiny `Node` class (if you want to build a custom parser)
  - `tiny_parser.py` – Barebones tokenizer + stack-based XML-ish parser (learning only)
  - `transforms.py` – `flatten_text`, `total_duration_seconds`, `validate_ssml`
  - `examples/sample1.xml` – Small SSML
- `src/strings/` – Classic string & parsing problems
  - `reverse_words.py`, `is_valid_tags.py`, `sliding_window_substring.py`, `top_k_freq.py`
- `tests/` – `unittest` test suite
- `scripts/run_examples.py` – Quick demo runner

## ▶️ Quick start

```bash
python -V        # 3.10+ recommended
python -m unittest -v
python scripts/run_examples.py
```

## 🧩 SSML exercises

1. **Flatten**: Convert SSML → human-readable text (apply `<sub alias>`; ignore tags).
2. **Duration**: Estimate speech time (e.g., 180 wpm) + add `<break time="...">` pauses.
3. **Validate**: Basic checks: well-formed, unknown attributes, illegal nesting (extend as you like).

## 🧠 Strings/DSA included

- Balanced/valid tags with a **stack**
- Longest substring without repeating characters (**sliding window**)
- Reverse words (normalize whitespace)
- Top‑k frequent words (dict + sort)

## 🔧 No external deps

This repo uses only Python standard library. Tests use `unittest`.

## 📦 Suggested practice flow

- Study `src/ssml/simple_etree.py` + `src/ssml/transforms.py`
- Implement/extend `tiny_parser.py` to simulate a “no-stdlib-XML” environment
- Do `tests/` until all pass; add your own edge cases

## 📝 License

MIT – for your personal practice.
