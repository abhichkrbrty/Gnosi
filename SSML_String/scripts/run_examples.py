from __future__ import annotations
from pathlib import Path
import os, sys
import xml.etree.ElementTree as ET

# make project root importable when running this script directly
THIS_DIR = Path(__file__).resolve().parent
PROJ_ROOT = THIS_DIR.parent
sys.path.insert(0, str(PROJ_ROOT))

from src.ssml.simple_etree import parse_ssml
from src.ssml.transforms import flatten_text, total_duration_seconds, validate_ssml

if __name__ == "__main__":
    ssml_path = PROJ_ROOT / "src" / "ssml" / "examples" / "sample1.xml"
    txt = ssml_path.read_text(encoding="utf-8")
    root = parse_ssml(txt)
    validate_ssml(root)
    plain = flatten_text(root)
    dur = total_duration_seconds(root, wpm=180)
    print("Flattened:", plain)
    print("Duration (s):", dur)
    print("OK")