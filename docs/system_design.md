# System Design & Scalability Notes

This document captures system-design thinking for the finance RAG tool.

## Core design ideas

- Separate **offline** work (parsing, structuring, embedding) from **online** work (retrieval and answering).
- Use **metadata filtering + lightweight retrieval** to keep query-time costs low.
- Combine **vectorless**, structure-aware retrieval with **vector-based** search to get both precision and scalability.

## Components and responsibilities

1. **Ingestion Pipeline**
   - Batch job processing new/updated documents.
   - Responsibilities:
     - Parse raw files into elements.
     - Infer basic structure (`section_path`).
     - Persist JSON trees and update indices.

2. **Indexing Service**
   - Embedding index (vector RAG).
   - Future: additional indexes (BM25, keyword, graph).
   - Needs:
     - Idempotent indexing.
     - Ability to re-index specific docs when structure improves.

3. **Retrieval Service**
   - Exposes a function like `retrieve(query)` for the app.
   - Current: vector search only.
   - Future:
     - Query router (structured vs. unstructured doc types).
     - Multi-step retrieval (candidate doc selection → structural traversal).

4. **Application Layer**
   - CLI now, UI later.
   - Interacts only with the retrieval service and, later, the LLM service.

5. **LLM Service (future)**
   - Local model runner (vLLM/ollama).
   - Handles:
     - Structured traversal prompts.
     - Answer generation prompts.

## Scaling dimensions

### 1. Corpus size (number of documents / nodes)

- Challenge:
  - Thousands of long docs ⇒ millions of nodes.
- Mitigations:
  - Use metadata filters on `doc_type`, `year`, `company` up-front.
  - Use BM25/keyword or vector search to select a small candidate set of docs (e.g., 5–10) for deeper traversal.
  - Build separate indexes per doc type or per entity if needed.

### 2. Indexing cost

- Structuring and embedding are CPU/GPU heavy.
- Strategy:
  - Run indexing as an offline job.
  - Use queues (e.g., simple filesystem queue or task runner) for new documents.
  - Support incremental updates (per-document re-index).

### 3. Query latency

Target query latency < 3–5 seconds for interactive use.

- Vector search is fast; the heavy cost will be:
  - LLM traversal (vectorless retrieval).
  - Answer generation.
- Techniques:
  - Keep context windows small via good candidate selection.
  - Cache:
    - Embeddings.
    - Common queries and their retrieved nodes.
    - Traversal paths for repeated patterns.

### 4. Local-only constraints

- No SaaS services; everything runs on local hardware.
- Implications:
  - Need to choose models that fit GPU/CPU memory and performance.
  - Must design for graceful degradation:
    - Smaller models with faster response.
    - Optional "deep reasoning" mode that users can toggle.

## Future design questions

- How to encode the document tree:
  - JSON + SQLite vs. a proper graph DB?
- How to specify and store "traversal traces":
  - For each query, record which sections were visited and why.
- How to evaluate retrieval quality at scale:
  - See `EVALUATION.md`.
