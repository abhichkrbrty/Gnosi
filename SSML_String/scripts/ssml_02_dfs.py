from __future__ import annotations
from pathlib import Path
import sys
import xml.etree.ElementTree as ET

# add project root for imports
THIS_DIR = Path(__file__).resolve().parent
PROJ_ROOT = THIS_DIR.parent
sys.path.insert(0, str(PROJ_ROOT))

from src.ssml.simple_etree import parse_ssml

SAMPLE = """<speak>
  Hello <sub alias="NYC">New York City</sub> fans!
  <p>
    <s>Welcome to our quick SSML demo.</s>
    <s>We’ll slow down a bit using <prosody rate="slow">prosody</prosody>.</s>
  </p>
  <voice name="en-US-JennyNeural">This line is under a specific voice.</voice>
  Thanks for listening. <break time="500ms"/>
</speak>"""

def dfs_preorder(el: ET.Element, visit):
    """Pre-order DFS: visit node, then its children."""
    visit(el)
    for c in list(el):
        dfs_preorder(c, visit)

def dfs_flatten_reading_order(el: ET.Element, out):
    """
    Flatten visible text in natural reading order:
    - el.text
    - child subtree
    - child.tail (after each child)
    """
    if el.tag == "sub" and "alias" in el.attrib:
        # <sub alias="X">Y</sub> => use alias
        out.append(el.attrib["alias"])
        return

    if el.text:
        out.append(el.text)

    for c in list(el):
        dfs_flatten_reading_order(c, out)
        if c.tail:
            out.append(c.tail)

def dfs_collect_prosody_segments(el: ET.Element, cur_style, segments):
    """
    Example of style inheritance during DFS.
    cur_style = dict with 'rate', 'pitch', 'volume'.
    """
    style = dict(cur_style)
    if el.tag == "prosody":
        # override any provided attributes
        for k in ("rate", "pitch", "volume"):
            if k in el.attrib:
                style[k] = el.attrib[k]

    # record text at this node with the current style
    if el.text and el.text.strip():
        segments.append((el.text.strip(), style.copy()))

    for c in list(el):
        dfs_collect_prosody_segments(c, style, segments)
        if c.tail and c.tail.strip():
            segments.append((c.tail.strip(), style.copy()))

if __name__ == "__main__":
    root = parse_ssml(SAMPLE)

    print("=== DFS (pre-order) visiting tags ===")
    dfs_preorder(root, lambda e: print(f"<{e.tag}> attrs={dict(e.attrib)}"))

    print("\n=== DFS flatten to visible text ===")
    buf: list[str] = []
    dfs_flatten_reading_order(root, buf)
    # normalize spaces lightly for display
    text = " ".join(" ".join(buf).split())
    print(text)

    print("\n=== DFS with style inheritance (prosody) ===")
    segs = []
    dfs_collect_prosody_segments(root, {"rate": "medium", "pitch": "medium", "volume": "medium"}, segs)
    for t, st in segs:
        print(f"{t!r} -> {st}")