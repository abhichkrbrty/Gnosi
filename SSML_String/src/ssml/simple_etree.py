from __future__ import annotations
import xml.etree.ElementTree as ET
from typing import Any

def parse_ssml(text: str) -> ET.Element:
    """Parse SSML using Python stdlib ElementTree (no external libs)."""
    # ElementTree will raise for unclosed/ill-formed XML
    root = ET.fromstring(text)
    return root
