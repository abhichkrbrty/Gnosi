
from __future__ import annotations
from pathlib import Path
import sys
import xml.etree.ElementTree as ET

THIS_DIR = Path(__file__).resolve().parent
PROJ_ROOT = THIS_DIR.parent
sys.path.insert(0, str(PROJ_ROOT))

from src.ssml.simple_etree import parse_ssml

SAMPLE = """<speak>
  First sentence. <break time="500ms"/>
  Second sentence. <break strength="weak"/>
  Third sentence. <break strength="x-strong"/>
  Fourth sentence. <break time="2s"/>
</speak>"""

STRENGTH_MAP = {
    "none": 0.0,
    "x-weak": 0.1,
    "weak": 0.25,
    "medium": 0.5,
    "strong": 0.75,
    "x-strong": 1.0,
}

def break_duration(el: ET.Element) -> float:
    """Convert <break> to seconds using either time or strength."""
    if "time" in el.attrib:
        t = el.attrib["time"]
        if t.endswith("ms"):
            return float(t[:-2]) / 1000.0
        elif t.endswith("s"):
            return float(t[:-1])
    if "strength" in el.attrib:
        return STRENGTH_MAP.get(el.attrib["strength"], 0.5)
    return 0.0

if __name__ == "__main__":
    root = parse_ssml(SAMPLE)
    print("=== Break Durations ===")
    for el in root.iter("break"):
        d = break_duration(el)
        print(f"<break {el.attrib}> => {d:.2f}s")