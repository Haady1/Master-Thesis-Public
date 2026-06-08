"""Tekst-fingerprint voor de advies-matcher-evaluatie.

Wat dit doet
------------
Berekent een deterministische "vingerafdruk" van documenttekst zodat we kunnen
vaststellen of twee documenten (vrijwel) hetzelfde zijn. We gebruiken dit om een
website-adviesrapport te koppelen aan zijn kopie in de officiele bekendmakingen:
beide zijn hetzelfde document, dus hun tekst overlapt sterk.

Methode
-------
- Normaliseer tekst: lowercase, alleen alfanumeriek, splits op witruimte.
- Neem de eerste MAX_TOKENS woorden (begrenst geheugen en is symmetrisch).
- Bouw woord-shingles (k opeenvolgende woorden) en hash ze stabiel met crc32.
  Stabiele hash is belangrijk: Python's ingebouwde hash() is per proces gesalt
  en dus niet herhaalbaar tussen runs/scripts.
- Vergelijk twee fingerprints met de Jaccard-index |A snijpunt B| / |A vereniging B|.

Plaats in de pijplijn
---------------------
Hulpmodule voor matcher/advies/evaluatie/*. Read-only; raakt de database niet.

"""
from __future__ import annotations

import re
import zlib

MAX_TOKENS = 8000
SHINGLE_K = 4

_NON_ALNUM = re.compile(r"[^0-9a-z]+")

def normalize_tokens(text: str | None) -> list[str]:
    """Zet ruwe tekst om naar een lijst genormaliseerde woorden (begrensd)."""
    if not text:
        return []
    lowered = text.lower()
                                                                        
    cleaned = _NON_ALNUM.sub(" ", lowered)
    tokens = [tok for tok in cleaned.split() if len(tok) >= 2]
    return tokens[:MAX_TOKENS]

def fingerprint(text: str | None, *, k: int = SHINGLE_K) -> set[int]:
    """Geef de set crc32-gehashte woord-shingles van de tekst."""
    tokens = normalize_tokens(text)
    if len(tokens) < k:
                                                            
        return {zlib.crc32(tok.encode("utf-8")) for tok in tokens}
    shingles: set[int] = set()
    for i in range(len(tokens) - k + 1):
        shingle = " ".join(tokens[i : i + k])
        shingles.add(zlib.crc32(shingle.encode("utf-8")))
    return shingles

def jaccard(a: set[int], b: set[int]) -> float:
    """Jaccard-overeenkomst tussen twee shingle-sets (0.0 - 1.0)."""
    if not a or not b:
        return 0.0
    intersection = len(a & b)
    if intersection == 0:
        return 0.0
    union = len(a) + len(b) - intersection
    return intersection / union
