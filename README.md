# Finance Document Intelligence RAG (Hybrid Vectorless + Vector)

## Overview

This project is a local, hybrid RAG system for finance teams.

We combine:
- A **document-intelligence structuring layer** that converts unstructured finance documents into a navigable tree (sections, tables, entities).
- A **vectorless, reasoning-based retrieval step** that uses document structure to find the most relevant sections.
- A **traditional vector RAG layer** that uses embeddings for fast, approximate search across the corpus.

The goal: give FP&A, Treasury, and Accounting a copilot that can answer questions about 10‑K/10‑Q filings, internal reports, policies, and contracts with section‑level citations, while keeping everything on‑prem/local.

All components are designed to run locally (Python, open‑source models, local vector DB) with no external APIs by default.

---

## Core use case

> “Finance Document Copilot for FP&A and Treasury: answer questions over internal budgets, management reports, board decks, and external filings; surface relevant sections with traceable reasoning; and support audit/compliance queries.”

Example questions:
- “What are the main drivers of operating margin compression in FY 2024?”
- “Which covenants apply to our revolving credit facility?”
- “Where do we disclose assumptions behind stock‑based compensation expense?”
- “How did SG&A grow relative to revenue over the last three years, and why?”

---

## Architecture (Phase 1)

Phase 1 implements a minimal vertical slice:

1. **Ingestion**
   - Parse PDF documents (e.g., 10‑K) into elements using `unstructured`.
   - Store elements as a simple JSON “document tree” with nodes that know their section path and page.

2. **Indexing**
   - Build embeddings for each node with a local `sentence-transformers` model.
   - Store embeddings + metadata in a local ChromaDB collection.

3. **Retrieval**
   - Given a query, run vector search over nodes.
   - Group results by `doc_name` and `section_path` to approximate structure‑aware retrieval.
   - Present relevant sections to the user in a CLI interface.

Later phases add:
- An explicit vectorless traversal over the document tree.
- A query router between vectorless vs. vector retrieval.
- A local LLM for answer generation and reasoning.

---

## Repo structure

```text
finance-rag-hybrid/
  data/
    raw/          # Original PDFs / docs
    processed/    # Parsed JSON "trees"
  index/
    chroma/       # Vector DB files
  src/
    __init__.py
    config.py
    ingest.py
    structure.py
    embed_index.py
    retrieve.py
    cli_demo.py
  docs/
    ARCHITECTURE.md
    SYSTEM_DESIGN.md
    ROADMAP.md
    SETUP.md
    USAGE.md
    EVALUATION.md
```

---

## Quickstart (Phase 1)

1. Create and activate a virtualenv:

   ```bash
   python -m venv venv
   source venv/bin/activate   # Windows: venv\Scripts\activate
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Place 1–3 finance PDFs (e.g., 10‑Ks) into `data/raw/`.

4. Run the ingestion + structuring pipeline:

   ```bash
   python -m src.structure
   ```

5. Build the vector index:

   ```bash
   python -m src.embed_index
   ```

6. Run the CLI demo:

   ```bash
   python -m src.cli_demo
   ```

Ask questions like “revenue recognition policy” or “liquidity risk” and the CLI will print the most relevant sections across your filings.

---

## Status

- ✅ Phase 1: ingestion, simple structuring, vector index, CLI retrieval.
- ⏳ Phase 2: hybrid vectorless + vector retrieval, local LLM answers.
- ⏳ Phase 3: scale‑out, evaluation, and dashboarding.

See `docs/ROADMAP.md` for next steps.