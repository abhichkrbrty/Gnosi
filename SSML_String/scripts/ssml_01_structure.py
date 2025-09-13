from __future__ import annotations
from pathlib import Path
import sys

# make project root importable
THIS_DIR = Path(__file__).resolve().parent
PROJ_ROOT = THIS_DIR.parent
sys.path.insert(0, str(PROJ_ROOT))

import xml.etree.ElementTree as ET
from src.ssml.simple_etree import parse_ssml
from src.ssml.transforms import flatten_text, total_duration_seconds, validate_ssml

SAMPLE = """<speak>
  Hello <sub alias="NYC">New York City</sub> fans!
  <p>
    <s>Welcome to our quick SSML demo.</s>
    <s>We’ll slow down a bit using <prosody rate="slow">prosody</prosody>.</s>
  </p>
  <voice name="en-US-JennyNeural">
    This line is under a specific voice.
  </voice>
  Thanks for listening.
</speak>
"""

def pretty_tree(el: ET.Element, depth: int = 0):
    """Print tag, attrs, text, and tail with indentation to visualize structure."""
    pad = "  " * depth
    text = (el.text or "").strip()
    attrs = " " + " ".join(f'{k}="{v}"' for k, v in el.attrib.items()) if el.attrib else ""
    print(f"{pad}<{el.tag}{attrs}>")
    if text:
        print(f"{pad}  text: {text!r}")
    for c in list(el):
        pretty_tree(c, depth + 1)
        tail = (c.tail or "").strip()
        if tail:
            print(f"{pad}  tail-after-{c.tag}: {tail!r}")
    print(f"{pad}</{el.tag}>")

if __name__ == "__main__":
    # 1) parse
    root = parse_ssml(SAMPLE)

    # 2) minimal validation
    validate_ssml(root)  # will raise if not <speak> root or invalid <break> attrs, etc.

    # 3) inspect structure
    print("=== TREE STRUCTURE ===")
    pretty_tree(root)

    # 4) flatten to human-visible text
    flat = flatten_text(root)
    print("\n=== FLATTENED TEXT ===")
    print(flat)

    # 5) rough duration (just WPM; no breaks in this sample)
    dur = total_duration_seconds(root, wpm=180)
    print("\n=== ESTIMATED DURATION (s) ===")
    print(dur)