# Evaluation Plan

## Goals

- Measure whether the hybrid retrieval approach actually improves:
  - Relevance of retrieved sections for finance queries.
  - Trust and usability for finance analysts.
- Compare:
  - Pure vector RAG vs.
  - Hybrid (vector + structured / vectorless) approaches.

## Phase 1 – Manual spot checks

- Create a small set (20–30) of evaluation questions:
  - Risk disclosures, policies, margin drivers, etc.
- For each question:
  - Run the current retrieval.
  - Manually judge whether the top 3 sections contain the correct answer.

Metrics:
- Top‑1 and Top‑3 "contains answer" rate.

## Phase 2 – Structured evaluation set

- Build a small QA dataset (question, answer, source section).
- For each retrieval variant (vector‑only vs. hybrid):
  - Compute:
    - Hit rate: does any retrieved node overlap the labeled source section?
    - MRR / NDCG-style metrics on rank.

## Phase 3 – Latency vs. quality tradeoff

- Measure:
  - Retrieval time for vector‑only vs hybrid.
  - Answer generation time with local LLM.
- Plot tradeoff curves:
  - More reasoning steps vs. more latency vs. better hit rate.

## Qualitative evaluation

- Ask finance‑literate users (or yourself in a finance‑analyst mindset) to:
  - Perform a realistic analysis task (e.g. “understand liquidity risk factors across 3 years”).
  - Record:
    - How often retrieved context was enough.
    - How often they needed to open the underlying PDF.

Use this feedback to refine:
- Query routing.
- Context selection strategy.
- Presentation in the UI.