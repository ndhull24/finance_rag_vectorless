# Architecture (Phase 1)

## Goals

- Build a local-first RAG pipeline tailored to finance documents.
- Prototype the hybrid idea: structured document intelligence + retrieval.
- Lay the groundwork for vectorless, reasoning-based retrieval in later phases.

## High-level components

1. **Ingestion & Structuring**
   - Input: PDFs in `data/raw/`
   - Process:
     - `unstructured` parses each PDF into elements.
     - `structure.py` converts elements into a simple JSON "document tree".
   - Output: `*.json` files in `data/processed/` with nodes:
     - `id`, `page`, `type`, `text`, `section_path`, `doc_name`.

2. **Indexing**
   - `embed_index.py` loads all nodes from `data/processed/`.
   - Builds embeddings using a local `sentence-transformers` model.
   - Stores them in a ChromaDB collection (`index/chroma/finance_docs`).

3. **Retrieval**
   - `retrieve.py` queries the Chroma collection:
     - Input: user query.
     - Output: top-k node texts + metadata.
   - `cli_demo.py` groups nodes by `(doc_name, section_path)` and prints the most relevant sections.

## Data flow

```text
PDF (10-K etc.)
   ↓  ingest.py/structure.py
elements (unstructured)
   ↓
document tree (JSON; nodes with section_path)
   ↓  embed_index.py
embeddings + metadata (ChromaDB)
   ↓  retrieve.py/cli_demo.py
grouped sections for a user query
```

## Future architecture (preview)

Later phases will add:

- A **document-intelligence layer** that builds a richer tree/graph:
  - Headings, tables, footnotes, entities, references.
- A **vectorless traversal engine**:
  - LLM-guided navigation of the tree to pick relevant nodes.
- A **query router**:
  - Decide when to use vectorless retrieval vs. traditional vector RAG or a mixture.
- A **local LLM worker** (e.g., via vLLM or ollama):
  - For reasoning over retrieved context and generating answers.

See `SYSTEM_DESIGN.md` for scaling considerations.