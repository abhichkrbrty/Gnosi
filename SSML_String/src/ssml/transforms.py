from __future__ import annotations
from typing import List
import xml.etree.ElementTree as ET

def flatten_text(root: ET.Element) -> str:
    """Flatten SSML to visible text. Applies <sub alias="..."> if present."""
    out: List[str] = []

    def walk(el: ET.Element):
        # apply <sub alias="..."> replacement
        if el.tag == "sub" and "alias" in el.attrib:
            out.append(el.attrib["alias"])
        else:
            # text at this node
            if el.text and el.text.strip():
                out.append(el.text.strip())
            # children
            for c in list(el):
                walk(c)
                if c.tail and c.tail.strip():
                    out.append(c.tail.strip())

    walk(root)
    return " ".join(" ".join(out).split())

def total_duration_seconds(root: ET.Element, wpm: int = 180) -> float:
    """Estimate speech duration + breaks. 180 wpm default; <break time="..."> adds pauses."""
    words = len(flatten_text(root).split())
    speech = words / (wpm / 60.0)
    br = 0.0

    def walk(el: ET.Element):
        nonlocal br
        if el.tag == "break":
            t = el.attrib.get("time")
            if t:
                if t.endswith("ms"):
                    br += float(t[:-2]) / 1000.0
                elif t.endswith("s"):
                    br += float(t[:-1])
        for c in list(el):
            walk(c)

    walk(root)
    return round(speech + br, 3)

def validate_ssml(root: ET.Element) -> None:
    """Very light validation: root must be <speak>, and tags must be well-formed (ElementTree ensures that).
    Extend with your own allowed tags/attrs rules if you like.
    """
    if root.tag != "speak":
        raise ValueError("Root must be <speak>")
    # Example: ensure <break> only has 'time' or 'strength'
    for el in root.iter():
        if el.tag == "break":
            for k in el.attrib.keys():
                if k not in {"time", "strength"}:
                    raise ValueError(f"Unsupported attribute on <break>: {k}")
