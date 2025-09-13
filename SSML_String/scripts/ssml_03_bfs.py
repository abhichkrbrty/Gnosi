from __future__ import annotations
from pathlib import Path
import sys, collections
import xml.etree.ElementTree as ET

# add project root
THIS_DIR = Path(__file__).resolve().parent
PROJ_ROOT = THIS_DIR.parent
sys.path.insert(0, str(PROJ_ROOT))

from src.ssml.simple_etree import parse_ssml

SAMPLE = """<speak>
  <p id="intro">Hello <sub alias="NYC">New York City</sub> fans!</p>
  <p id="body">
    <s>Welcome to our quick SSML demo.</s>
    <s>We’ll slow down with <prosody rate="slow">prosody</prosody>.</s>
  </p>
  <voice name="en-US-JennyNeural">This line is under a specific voice.</voice>
  <break time="750ms"/>
</speak>"""

def bfs_levels(root: ET.Element):
    """Print nodes level-by-level and also build a structure summary."""
    q = collections.deque([(root, 0)])
    levels: dict[int, list[str]] = {}

    while q:
        el, d = q.popleft()
        levels.setdefault(d, []).append(el.tag)
        for c in list(el):
            q.append((c, d + 1))

    # pretty print
    print("=== BFS Levels ===")
    for depth in sorted(levels):
        print(f"depth {depth}: {levels[depth]}")

def bfs_collect_tags_and_attrs(root: ET.Element):
    """Collect tag frequencies and distinct attributes by tag."""
    q = collections.deque([root])
    tag_freq: dict[str, int] = {}
    attrs_by_tag: dict[str, set[str]] = {}

    while q:
        el = q.popleft()
        tag_freq[el.tag] = tag_freq.get(el.tag, 0) + 1
        if el.attrib:
            attrs_by_tag.setdefault(el.tag, set()).update(el.attrib.keys())
        for c in list(el):
            q.append(c)

    print("\n=== Tag Frequencies ===")
    for t, n in sorted(tag_freq.items(), key=lambda x: (-x[1], x[0])):
        print(f"{t}: {n}")

    print("\n=== Attributes Seen by Tag ===")
    for t in sorted(attrs_by_tag):
        print(f"{t}: {sorted(attrs_by_tag[t])}")

if __name__ == "__main__":
    root = parse_ssml(SAMPLE)
    bfs_levels(root)
    bfs_collect_tags_and_attrs(root)