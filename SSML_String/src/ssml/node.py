from __future__ import annotations
from typing import Dict, List, Optional

class Node:
    """Minimal tree node for custom parsing experiments."""
    __slots__ = ("tag", "attrs", "text", "children")
    def __init__(self, tag: str, attrs: Optional[Dict[str, str]] = None, text: str = ""):
        self.tag = tag
        self.attrs = attrs or {}
        self.text = text
        self.children: List["Node"] = []

    def add(self, child: "Node") -> None:
        self.children.append(child)

    def __repr__(self) -> str:
        return f"Node(tag={self.tag!r}, attrs={self.attrs!r}, text={self.text!r}, children={len(self.children)})"
