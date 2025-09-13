from __future__ import annotations
from typing import Dict, List, Tuple, Optional
from .node import Node

# NOTE: This is an intentionally minimal, learning-oriented parser.
# It supports: <tag key="val"> ... </tag> and <selfclosing .../> with double-quoted attrs.
# It does NOT support comments, CDATA, namespaces, or entities.

def _parse_attrs(s: str) -> Dict[str, str]:
    attrs: Dict[str, str] = {}
    i = 0
    n = len(s)
    while i < n:
        while i < n and s[i].isspace():
            i += 1
        if i >= n:
            break
        # read key
        start = i
        while i < n and (s[i].isalnum() or s[i] in "_-:"):
            i += 1
        key = s[start:i]
        while i < n and s[i].isspace():
            i += 1
        if i >= n or s[i] != "=":
            # malformed; bail
            break
        i += 1
        while i < n and s[i].isspace():
            i += 1
        if i < n and s[i] == '"':
            i += 1
            start = i
            while i < n and s[i] != '"':
                i += 1
            val = s[start:i]
            if i < n and s[i] == '"':
                i += 1
            attrs[key] = val
        else:
            break
    return attrs

def parse_tiny(xml: str) -> Node:
    i = 0
    n = len(xml)
    stack: List[Node] = [Node("ROOT")]
    text_buf: List[str] = []

    def flush_text():
        if text_buf:
            txt = "".join(text_buf)
            if txt.strip():
                stack[-1].add(Node("#text", text=txt))
            text_buf.clear()

    while i < n:
        if xml[i] == "<":
            # tag start
            j = xml.find(">", i + 1)
            if j == -1:
                raise ValueError("Unclosed tag bracket")
            inside = xml[i+1:j].strip()
            if not inside:
                raise ValueError("Empty tag")
            if inside.startswith("?") or inside.startswith("!--"):
                # skip processing instructions/comments (very naive)
                i = j + 1
                continue
            is_end = inside.startswith("/")
            is_self = inside.endswith("/")

            if is_end:
                flush_text()
                tag = inside[1:].strip()
                if not stack or stack[-1].tag != tag:
                    raise ValueError(f"Mismatched closing tag: {tag}")
                stack.pop()
            else:
                # start or self-close
                # split tag name and attrs
                parts = inside[:-1].strip() if is_self else inside
                if " " in parts:
                    tag, rest = parts.split(" ", 1)
                    attrs = _parse_attrs(rest)
                else:
                    tag, attrs = parts, {}
                flush_text()
                node = Node(tag, attrs=attrs)
                stack[-1].add(node)
                if not is_self:
                    stack.append(node)
            i = j + 1
        else:
            text_buf.append(xml[i])
            i += 1
    flush_text()
    if len(stack) != 1:
        raise ValueError("Unclosed tags at end")
    return stack[0]
