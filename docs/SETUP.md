# Setup Guide

## 1. Prerequisites

- Python 3.10+
- Git
- VS Code (recommended)
- Optional: local GPU if you plan to run larger LLMs later

## 2. Clone and create virtual environment

```bash
git clone <your-repo-url> finance-rag-hybrid
cd finance-rag-hybrid

python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
```

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

If you don't have `requirements.txt` yet, you can start with:

```text
unstructured[chardet,pdf]
chromadb
sentence-transformers
rank-bm25
```

and then run:

```bash
pip install unstructured[chardet,pdf] chromadb sentence-transformers rank-bm25
pip freeze > requirements.txt
```

## 4. Data folders

Make sure these folders exist:

```text
data/raw/
data/processed/
index/chroma/
```

Put your sample finance PDFs (10‑K, 10‑Q, internal finance docs) into `data/raw/`.

## 5. First run

1. Build structured JSON trees:

   ```bash
   python -m src.structure
   ```

2. Build vector index:

   ```bash
   python -m src.embed_index
   ```

3. Start CLI demo:

   ```bash
   python -m src.cli_demo
   ```

You are now ready to ask questions over your documents.