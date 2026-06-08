from __future__ import annotations

import re
import zlib

MAX_TOKENS = 8000
SHINGLE_K = 4

_NON_ALNUM = re.compile(r"[^0-9a-z]+")

def normalize_tokens(text: str | None) -> list[str]:
    if not text:
        return []
    lowered = text.lower()

    cleaned = _NON_ALNUM.sub(" ", lowered)
    tokens = [tok for tok in cleaned.split() if len(tok) >= 2]
    return tokens[:MAX_TOKENS]

def fingerprint(text: str | None, *, k: int = SHINGLE_K) -> set[int]:
    tokens = normalize_tokens(text)
    if len(tokens) < k:

        return {zlib.crc32(tok.encode("utf-8")) for tok in tokens}
    shingles: set[int] = set()
    for i in range(len(tokens) - k + 1):
        shingle = " ".join(tokens[i : i + k])
        shingles.add(zlib.crc32(shingle.encode("utf-8")))
    return shingles

def jaccard(a: set[int], b: set[int]) -> float:
    if not a or not b:
        return 0.0
    intersection = len(a & b)
    if intersection == 0:
        return 0.0
    union = len(a) + len(b) - intersection
    return intersection / union
