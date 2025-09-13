from collections import Counter

def top_k_frequent_words(words: list[str], k: int) -> list[str]:
    cnt = Counter(words)
    # sort by (-freq, word) for deterministic order
    return [w for w, _ in sorted(cnt.items(), key=lambda x: (-x[1], x[0]))[:k]]
