import sys
import re
import xml.etree.ElementTree as ET

# ============================================================
# SSML Edge-Case Toolkit
# - Conservative validator for allowed tags/attrs
# - Break handling (time vs strength)
# - <sub> aliasing, <say-as> simple mock, <prosody>/<emphasis> style tracking
# - Whitespace normalization options
# - Collects ALL issues instead of failing fast
# ============================================================

ALLOWED_TAGS = {
    "speak", "p", "s", "voice", "prosody", "break", "say-as", "sub", "emphasis"
}

ALLOWED_ATTRS = {
    "voice": {"name", "language", "gender"},
    "prosody": {"rate", "pitch", "volume"},
    "break": {"time", "strength"},
    "say-as": {"interpret-as", "format", "detail"},
    "sub": {"alias"},
    "emphasis": {"level"},
    # generic container tags usually have no attrs; allow none by default
}

STRENGTH_MAP = {
    "none": 0.0,
    "x-weak": 0.1,
    "weak": 0.25,
    "medium": 0.5,
    "strong": 0.75,
    "x-strong": 1.0,
}

def parse_ssml_text(text: str):
    """
    Parse with ElementTree (requires well-formed XML).
    Return root or raise ET.ParseError for unbalanced/malformed XML.
    """
    return ET.fromstring(text)

def validate_tree(root: ET.Element):
    """
    Collect edge-case issues instead of raising immediately.
    - Root must be <speak>.
    - Only ALLOWED_TAGS.
    - Tag-specific attribute allow-list.
    - <break> must have either time or strength (not both), and time unit must be ms/s.
    - <sub> 'alias' should be non-empty.
    - Optional: depth limit to catch pathological nesting.
    Returns: list[str] of issues (empty => OK)
    """
    issues = []

    if root.tag != "speak":
        issues.append("Root must be <speak>.")

    MAX_DEPTH = 64
    def walk(el: ET.Element, depth: int):
        if depth > MAX_DEPTH:
            issues.append(f"Exceeded max depth {MAX_DEPTH} at <{el.tag}>.")
        if el.tag not in ALLOWED_TAGS:
            issues.append(f"Unknown/unsupported tag <{el.tag}>.")

        # attribute checks
        allowed = ALLOWED_ATTRS.get(el.tag, set())
        for k in el.attrib.keys():
            if k not in allowed and allowed:
                issues.append(f"Unsupported attribute '{k}' on <{el.tag}>.")
        # special tag rules
        if el.tag == "break":
            t = el.attrib.get("time")
            s = el.attrib.get("strength")
            if t and s:
                issues.append("<break> should not specify both 'time' and 'strength'.")
            if not t and not s:
                issues.append("<break> requires either 'time' or 'strength'.")
            if t:
                if not (t.endswith("ms") or t.endswith("s")):
                    issues.append("<break time> must end with 'ms' or 's'.")
                else:
                    # numeric sanity
                    try:
                        float(t[:-2]) if t.endswith("ms") else float(t[:-1])
                    except Exception:
                        issues.append("<break time> must be numeric.")
            if s and s not in STRENGTH_MAP:
                issues.append(f"Unknown break strength '{s}'.")
        if el.tag == "sub":
            alias = el.attrib.get("alias", "")
            if alias.strip() == "":
                issues.append("<sub> requires non-empty 'alias'.")
        if el.tag == "say-as":
            interp = el.attrib.get("interpret-as")
            if not interp:
                issues.append("<say-as> requires 'interpret-as'.")
        # recurse
        for c in list(el):
            walk(c, depth + 1)

    walk(root, 0)
    return issues

def break_duration_seconds(el: ET.Element) -> float:
    if "time" in el.attrib:
        t = el.attrib["time"]
        if t.endswith("ms"):
            return float(t[:-2]) / 1000.0
        if t.endswith("s"):
            return float(t[:-1])
        return 0.0
    if "strength" in el.attrib:
        return STRENGTH_MAP.get(el.attrib["strength"], 0.5)
    return 0.0

def interpret_say_as(el: ET.Element) -> str:
    """
    Very light mock to expand <say-as> text.
    Extend as needed for more modes.
    """
    txt = (el.text or "").strip()
    mode = el.attrib.get("interpret-as", "")
    if not txt:
        return ""
    if mode in ("characters", "digits", "telephone"):
        return " ".join(list(txt))
    if mode == "ordinal":
        map_ord = {"1": "first", "2": "second", "3": "third", "4": "fourth", "5": "fifth"}
        return map_ord.get(txt, txt + "th")
    if mode == "date":
        parts = txt.split("/")
        if len(parts) == 3:
            m, d, y = parts
            return f"Month {m}, Day {d}, Year {y}"
    return txt

def flatten_with_styles(root: ET.Element, wpm: int = 180, normalize_spaces: bool = True):
    """
    Flatten to visible text while:
      - applying <sub alias>
      - expanding <say-as> (simple mock)
      - accounting for <break> duration
      - tracking style context from <prosody> and <emphasis>
    Returns: dict(text=..., duration=..., segments=[(text, style_dict), ...])
    """
    total_break = 0.0
    out_text_chunks = []
    segments = []

    def dfs(el: ET.Element, style):
        nonlocal total_break
        # style inheritance
        st = dict(style)
        if el.tag == "prosody":
            for k in ("rate", "pitch", "volume"):
                if k in el.attrib:
                    st[k] = el.attrib[k]
        if el.tag == "emphasis":
            st["emphasis"] = el.attrib.get("level", "moderate")

        # emit text for this node based on tag semantics
        if el.tag == "break":
            total_break += break_duration_seconds(el)
        elif el.tag == "sub":
            alias = el.attrib.get("alias")
            if alias:
                segments.append((alias.strip(), dict(st)))
                out_text_chunks.append(alias)
            # else: validator will flag empty alias
        elif el.tag == "say-as":
            exp = interpret_say_as(el)
            if exp:
                segments.append((exp, dict(st)))
                out_text_chunks.append(exp)
        else:
            # generic text handling
            if el.text and el.text.strip():
                txt = el.text.strip()
                segments.append((txt, dict(st)))
                out_text_chunks.append(txt)

        # children
        for c in list(el):
            dfs(c, st)
            if c.tail and c.tail.strip():
                segments.append((c.tail.strip(), dict(st)))
                out_text_chunks.append(c.tail.strip())

    dfs(root, {"rate": "medium", "pitch": "medium", "volume": "medium", "emphasis": "none"})
    text = " ".join(" ".join(out_text_chunks).split()) if normalize_spaces else "".join(out_text_chunks)
    # crude speech time based on WPM
    words = len(text.split())
    speech = words / (wpm / 60.0) if wpm > 0 else 0.0
    return {
        "text": text,
        "duration_seconds": round(speech + total_break, 3),
        "segments": segments,
        "break_seconds": round(total_break, 3),
    }

# ---------- Demo SSML payloads to exercise edge cases ----------

SAMPLES = {
    "ok_mixed": """<speak>
      Hello <sub alias="New York City">NYC</sub>!
      <p>We pause <break time="500ms"/> and continue.</p>
      <say-as interpret-as="characters">HTML</say-as>
      <prosody rate="slow"><emphasis level="strong">Important</emphasis> message.</prosody>
    </speak>""",
    "bad_break_units": """<speak>Oops <break time="5sec"/></speak>""",
    "both_break_attrs": """<speak><break time="500ms" strength="strong"/></speak>""",
    "empty_sub_alias": """<speak><sub alias="">USA</sub></speak>""",
    "missing_say_as_mode": """<speak><say-as>123</say-as></speak>""",
    "unknown_tag": """<speak><foo>bar</foo></speak>""",
    "deep_nesting": "<speak>" + "<p>"*70 + "text" + "</p>"*70 + "</speak>",
}

def _run_samples():
    for name, ssml in SAMPLES.items():
        print("=" * 72)
        print(f"Sample: {name}")
        try:
            root = parse_ssml_text(ssml)
        except ET.ParseError as e:
            print("XML ParseError:", e)
            continue
        issues = validate_tree(root)
        if issues:
            print("Issues:")
            for i in issues:
                print(" -", i)
        else:
            print("Issues: none")

        result = flatten_with_styles(root, wpm=180, normalize_spaces=True)
        print("Flattened text:", result["text"])
        print("Break seconds:", result["break_seconds"])
        print("Total duration (s):", result["duration_seconds"])
        print("Segments (text -> style) [first 5]:")
        for t, st in result["segments"][:5]:
            print("  ", repr(t), "->", st)

if __name__ == "__main__":
    _run_samples()