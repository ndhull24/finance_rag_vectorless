# scripts/build_chunks_jsonl.py
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

CHUNKS_PATH = DATA_DIR / "chunks.jsonl"

# TODO: Replace this with your real chunking logic.
# For now, here's an example list to show the format:
chunks = [
    {
        "text": "Capitalization thresholds for fixed assets are defined as ...",
        "doc_name": "capitalization_policy",
        "section_path": "Section 3. Capitalization Thresholds",
    },
    {
        "text": "Liquidity refers to the ability to meet short-term obligations ...",
        "doc_name": "liquidity_policy",
        "section_path": "Section 1. Liquidity Overview",
    },
]

with open(CHUNKS_PATH, "w", encoding="utf-8") as f:
    for ch in chunks:
        f.write(json.dumps(ch, ensure_ascii=False) + "\n")

print(f"Wrote {len(chunks)} chunks to {CHUNKS_PATH}")