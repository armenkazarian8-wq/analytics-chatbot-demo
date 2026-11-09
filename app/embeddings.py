"""Deterministic local embeddings (no external API required).

Produces a fixed-dimension unit vector from text via hashing. Good enough
for demo retrieval; swap for OpenAI/pgvector when USE_PGVECTOR + API key.
"""

from __future__ import annotations

import hashlib
import math
import re
from typing import Iterable

import numpy as np

from app.config import EMBEDDING_DIM


def _tokenize(text: str) -> list[str]:
    return re.findall(r"[a-z0-9]+", text.lower())


def embed_text(text: str, dim: int = EMBEDDING_DIM) -> list[float]:
    vec = np.zeros(dim, dtype=np.float64)
    tokens = _tokenize(text)
    if not tokens:
        return vec.tolist()
    for token in tokens:
        digest = hashlib.sha256(token.encode("utf-8")).digest()
        # Use multiple bytes to spread signal across dimensions.
        for i in range(0, min(len(digest), dim * 2), 2):
            idx = digest[i] % dim
            sign = 1.0 if digest[i + 1] % 2 == 0 else -1.0
            weight = 1.0 + (digest[i] / 255.0)
            vec[idx] += sign * weight
    norm = math.sqrt(float(np.dot(vec, vec)))
    if norm > 0:
        vec = vec / norm
    return vec.tolist()


def cosine_similarity(a: Iterable[float], b: Iterable[float]) -> float:
    va = np.asarray(list(a), dtype=np.float64)
    vb = np.asarray(list(b), dtype=np.float64)
    denom = float(np.linalg.norm(va) * np.linalg.norm(vb))
    if denom == 0:
        return 0.0
    return float(np.dot(va, vb) / denom)
