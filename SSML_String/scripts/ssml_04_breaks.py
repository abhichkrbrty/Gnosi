
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
  Welcome to Speechify.
  <break time="500ms"/>
  This part comes after half a second.
  <break strength="strong"/>
  And this part comes after a strong pause.
</speak>"""

def parse_break(el: ET.Element) -> float:
    """Return break duration in seconds (simple model)."""
    if el.tag != "break":
        return 0.0
    if "time" in el.attrib:
        t = el.attrib["time"]
        if t.endswith("ms"):
            return float(t[:-2]) / 1000.0
        elif t.endswith("s"):
            return float(t[:-1])
    elif "strength" in el.attrib:
        # map strengths to rough durations
        mapping = {
            "none": 0.0,
            "x-weak": 0.1,
            "weak": 0.25,
            "medium": 0.5,
            "strong": 0.75,
            "x-strong": 1.0,
        }
        return mapping.get(el.attrib["strength"], 0.5)
    return 0.0

def total_duration_with_breaks(root: ET.Element, wpm: int = 180) -> float:
    """Count words + break durations."""
    text = []
    total_break = 0.0

    def dfs(el: ET.Element):
        nonlocal total_break
        if el.tag == "break":
            total_break += parse_break(el)
        if el.text:
            text.append(el.text)
        for c in list(el):
            dfs(c)
            if c.tail:
                text.append(c.tail)

    dfs(root)
    words = len(" ".join(text).split())
    speech = words / (wpm / 60.0)
    return round(speech + total_break, 3)

if __name__ == "__main__":
    root = parse_ssml(SAMPLE)

    # collect all breaks
    print("=== Break Elements ===")
    for el in root.iter("break"):
        dur = parse_break(el)
        print(f"<break {el.attrib}> => {dur:.2f}s")

    # compute total duration
    dur = total_duration_with_breaks(root, wpm=180)
    print("\n=== Total Duration (s) with breaks ===")
    print(dur)