# Usage Guide

This guide explains how a finance user can interact with the Phase 1 CLI interface.

## Starting the CLI

Activate your virtualenv and run:

```bash
source venv/bin/activate   # or venv\Scripts\activate on Windows
python -m src.cli_demo
```

You will see:

```text
Finance RAG Phase 1 – CLI demo
Type a question about your finance docs. Empty to exit.
```

## Asking questions

Type natural language questions such as:

- "What does the company say about liquidity risk in 2024?"
- "Where is revenue recognition policy described?"
- "What are the main drivers of operating margin changes last year?"

For each question, the tool:

1. Searches the vector index over all parsed nodes.
2. Groups results by document and section.
3. Prints the top sections with a couple of snippet bullets.

Example output:

```text
== ACME_2024_10K :: ROOT > Item 7. Management's Discussion and Analysis ==
- The company experienced increased SG&A expenses due to higher labor and marketing spend ...
- Operating margin decreased from 12.4% to 10.1% ...

== ACME_2024_10K :: ROOT > Note 2. Summary of Significant Accounting Policies ==
- Revenue is recognized upon transfer of control to the customer ...
```

## Limitations (Phase 1)

- Answers are not generated yet; you see relevant sections/snippets.
- Structured hierarchy is simple (`section_path` heuristic).
- Only PDF ingestion is supported.

Future phases will add:
- Local LLM answer generation with citations.
- More robust document structure and vectorless traversal.
- A simple web UI instead of CLI.