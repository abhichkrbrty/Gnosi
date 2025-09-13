
from __future__ import annotations
from pathlib import Path
import sys
import xml.etree.ElementTree as ET

# add root for imports
THIS_DIR = Path(__file__).resolve().parent
PROJ_ROOT = THIS_DIR.parent
sys.path.insert(0, str(PROJ_ROOT))

from src.ssml.simple_etree import parse_ssml

SAMPLE = """<speak>
  Spell out: <say-as interpret-as="characters">HTML</say-as>.
  Digits: <say-as interpret-as="digits">1234</say-as>.
  Ordinal: <say-as interpret-as="ordinal">5</say-as>.
  Date: <say-as interpret-as="date" format="mdy">10/05/2025</say-as>.
  Telephone: <say-as interpret-as="telephone">8005551212</say-as>.
</speak>"""

def interpret_say_as(el: ET.Element) -> str:
    """Very simplified say-as interpreter (mocked for practice)."""
    txt = (el.text or "").strip()
    mode = el.attrib.get("interpret-as", "")
    if not txt:
        return ""
    if mode == "characters":
        return " ".join(list(txt))
    if mode == "digits":
        return " ".join(list(txt))
    if mode == "ordinal":
        # naive mock
        mapping = {"1": "first", "2": "second", "3": "third", "4": "fourth", "5": "fifth"}
        return mapping.get(txt, txt + "th")
    if mode == "date":
        # naive US mdy format
        parts = txt.split("/")
        if len(parts) == 3:
            m, d, y = parts
            return f"Month {m}, Day {d}, Year {y}"
    if mode == "telephone":
        return " ".join(list(txt))
    # default fallback
    return txt

def flatten_with_say_as(el: ET.Element, out):
    if el.tag == "say-as":
        out.append(interpret_say_as(el))
    else:
        if el.text:
            out.append(el.text)
        for c in list(el):
            flatten_with_say_as(c, out)
            if c.tail:
                out.append(c.tail)

if __name__ == "__main__":
    root = parse_ssml(SAMPLE)

    buf: list[str] = []
    flatten_with_say_as(root, buf)
    text = " ".join(" ".join(buf).split())

    print("=== Flattened Text with <say-as> handled ===")
    print(text)