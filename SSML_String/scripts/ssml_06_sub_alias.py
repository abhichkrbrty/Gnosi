
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
  Welcome to <sub alias="New York City">NYC</sub>!
  This project uses <sub alias="C-sharp">C#</sub>.
  Abbreviation <sub>USA</sub> without alias.
</speak>"""

def flatten_with_subs(el: ET.Element, out):
    """DFS flatten with <sub> substitution handling."""
    if el.tag == "sub":
        if "alias" in el.attrib:
            out.append(el.attrib["alias"])
        else:
            if el.text:
                out.append(el.text)
    else:
        if el.text:
            out.append(el.text)
        for c in list(el):
            flatten_with_subs(c, out)
            if c.tail:
                out.append(c.tail)

if __name__ == "__main__":
    root = parse_ssml(SAMPLE)

    buf: list[str] = []
    flatten_with_subs(root, buf)
    text = " ".join(" ".join(buf).split())

    print("=== Flattened Text with <sub> handled ===")
    print(text)