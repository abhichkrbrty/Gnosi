def reverse_words(s: str) -> str:
    """Reverse words; normalize whitespace to single spaces."""
    parts = s.split()
    return " ".join(reversed(parts))
