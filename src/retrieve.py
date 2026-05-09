# src/retrieve.py (vectorless version)
from typing import List, Tuple, Dict
import json
import os
from pathlib import Path

from rank_bm25 import BM25Okapi


# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
CHUNKS_PATH = BASE_DIR / "data" / "chunks.jsonl"


# In-memory index
_bm25 = None
_chunks: List[Dict] = []  # each: {"text": ..., "doc_name": ..., "section_path": ...}


def _load_chunks() -> List[Dict]:
    chunks = []
    if not CHUNKS_PATH.exists():
        raise FileNotFoundError(f"Chunks file not found at {CHUNKS_PATH}. "
                                f"Make sure you generated data/chunks.jsonl.")
    with open(CHUNKS_PATH, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            obj = json.loads(line)
            # Expect keys: text, doc_name, section_path
            chunks.append(obj)
    return chunks


def _tokenize(text: str) -> List[str]:
    # Simple whitespace tokenizer; you can improve this
    return text.lower().split()


def _get_bm25():
    global _bm25, _chunks
    if _bm25 is None:
        _chunks = _load_chunks()
        if not _chunks:
            raise ValueError(f"No chunks loaded from {CHUNKS_PATH}. "
                             "Make sure chunks.jsonl is populated.")
        corpus_tokens = [_tokenize(ch["text"]) for ch in _chunks]
        if not corpus_tokens:
            raise ValueError("No tokens in corpus. Check chunks.jsonl content.")
        _bm25 = BM25Okapi(corpus_tokens)
    return _bm25, _chunks


def search(query: str, k: int = 5) -> List[Tuple[str, Dict]]:
    """
    Vectorless retrieval: use BM25 over text chunks.
    Returns list of (text, meta_dict) just like the vector-based version.
    """
    if not query.strip():
        return []

    bm25, chunks = _get_bm25()
    query_tokens = _tokenize(query)
    scores = bm25.get_scores(query_tokens)

    # Get top-k indices sorted by score
    top_indices = sorted(
        range(len(scores)),
        key=lambda i: scores[i],
        reverse=True
    )[:k]

    results: List[Tuple[str, Dict]] = []
    for idx in top_indices:
        ch = chunks[idx]
        text = ch["text"]
        meta = {
            "doc_name": ch.get("doc_name", "unknown_doc"),
            "section_path": ch.get("section_path", "unknown_section"),
        }
        results.append((text, meta))

    return results


def demo():
    print("Vectorless Finance RAG – Retrieval demo (BM25)")
    while True:
        q = input("\nQuery (empty to quit): ").strip()
        if not q:
            print("Goodbye!")
            break
        hits = search(q, k=5)
        if not hits:
            print("\nNo results found")
            continue

        print("\nTop matches:")
        for i, (text, meta) in enumerate(hits, 1):
            print(f"\n[{i}] {meta['doc_name']} | {meta['section_path']}")
            snippet = text[:400].replace("\n", " ")
            print(snippet, "..." if len(text) > 400 else "")


if __name__ == "__main__":
    demo()