from pathlib import Path
import sys, xml.etree.ElementTree as ET

THIS_DIR = Path(__file__).resolve().parent
PROJ_ROOT = THIS_DIR.parent
sys.path.insert(0, str(PROJ_ROOT))

from src.ssml.simple_etree import parse_ssml

SAMPLE = """<speak>
  This is <emphasis level="strong">very important</emphasis>.
  This is <emphasis level="reduced">less important</emphasis>.
  This is <emphasis>moderately emphasized</emphasis>.
</speak>"""

def dfs_with_emphasis(el: ET.Element, cur_style, segments):
    style = dict(cur_style)
    if el.tag == "emphasis":
        style["emphasis"] = el.attrib.get("level", "moderate")
    if el.text and el.text.strip():
        segments.append((el.text.strip(), style.copy()))
    for c in list(el):
        dfs_with_emphasis(c, style, segments)
        if c.tail and c.tail.strip():
            segments.append((c.tail.strip(), style.copy()))

if __name__ == "__main__":
    root = parse_ssml(SAMPLE)
    segments = []
    dfs_with_emphasis(root, {"emphasis": "none"}, segments)
    print("=== Segments with Emphasis Styles ===")
    for txt, st in segments:
        print(f"{txt!r} -> {st}")