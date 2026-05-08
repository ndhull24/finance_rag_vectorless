# Roadmap

## Phase 1 – Minimal vertical slice (current)

- [x] Ingest PDFs using `unstructured`.
- [x] Build simple JSON document trees (nodes with `section_path`).
- [x] Index nodes with sentence-transformer embeddings in Chroma.
- [x] CLI retrieval demo that returns relevant sections per query.

## Phase 2 – Hybrid retrieval and local LLM

- [ ] Introduce query router:
  - Classify queries as "structured-doc" vs "unstructured/memo".
- [ ] Add BM25/keyword index for cheap candidate document selection.
- [ ] Implement simple vectorless traversal:
  - For top candidate 10‑K/policy docs, use LLM to navigate sections.
- [ ] Integrate a local LLM for:
  - Traversal (deciding which sections to read).
  - Answer generation with citations.
- [ ] Replace CLI with a basic Streamlit UI.

## Phase 3 – Scaling and evaluation

- [ ] Expand corpus to hundreds of documents:
  - Multiple 10‑Ks/10‑Qs, synthetic internal reports, policies.
- [ ] Implement caching and richer metadata filters.
- [ ] Add logging and basic metrics for:
  - Latency (retrieval + LLM).
  - Retrieval quality (manual labels).
- [ ] Evaluate hybrid vs. pure vector retrieval on a small test set.

## Phase 4 – “Production-style” polish (optional)

- [ ] Authentication / simple user management.
- [ ] Dockerize the stack (app + vector DB + model server).
- [ ] Add a basic admin panel to inspect indexing status and logs.