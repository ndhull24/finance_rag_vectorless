import json
from pathlib import Path
from typing import List, Dict
import logging
import chromadb
from sentence_transformers import SentenceTransformer
from .config import CHROMA_DIR, EMBED_MODEL_NAME, DATA_PROCESSED_DIR

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def load_nodes() -> List[Dict]:
    try:
        nodes = []
        json_files = list(DATA_PROCESSED_DIR.glob("**/*.json"))
        
        if not json_files:
            logger.warning(f"No JSON files found in {DATA_PROCESSED_DIR}")
            return nodes
        
        logger.info(f"Loading {len(json_files)} JSON files...")
        
        for fp in json_files:
            try:
                with open(fp, "r", encoding="utf-8") as f:
                    doc = json.load(f)
                for n in doc.get("nodes", []):
                    n["doc_name"] = fp.stem
                    nodes.append(n)
                logger.debug(f"Loaded {len(doc.get('nodes', []))} nodes from {fp.name}")
            except Exception as e:
                logger.error(f"Error loading {fp}: {str(e)}")
                continue
        
        logger.info(f"Total nodes loaded: {len(nodes)}")
        return nodes
    except Exception as e:
        logger.error(f"Error loading nodes: {str(e)}")
        raise

def main():
    try:
        CHROMA_DIR.mkdir(parents=True, exist_ok=True)
        nodes = load_nodes()
        
        if not nodes:
            logger.warning("No processed JSONs found. Run src.structure first.")
            return
        
        logger.info(f"Indexing {len(nodes)} nodes...")

        client = chromadb.PersistentClient(path=str(CHROMA_DIR))
        collection = client.get_or_create_collection("finance_docs")

        logger.info(f"Loading embedding model: {EMBED_MODEL_NAME}")
        model = SentenceTransformer(EMBED_MODEL_NAME)

        texts = [n["text"] for n in nodes]
        ids = [str(n["id"]) + "_" + n["doc_name"] for n in nodes]
        metadatas = [{"doc_name": n["doc_name"], "section_path": n["section_path"]} for n in nodes]
        
        logger.info("Generating embeddings...")
        embeddings = model.encode(texts, batch_size=32, show_progress_bar=True)

        # Add in batches to respect ChromaDB's max batch size
        batch_size = 5000
        total_batches = (len(ids) + batch_size - 1) // batch_size
        for batch_num, i in enumerate(range(0, len(ids), batch_size), 1):
            batch_ids = ids[i:i+batch_size]
            batch_embeddings = embeddings[i:i+batch_size].tolist()
            batch_metadatas = metadatas[i:i+batch_size]
            batch_texts = texts[i:i+batch_size]
            
            collection.add(
                ids=batch_ids,
                embeddings=batch_embeddings,
                metadatas=batch_metadatas,
                documents=batch_texts
            )
            logger.info(f"Added batch {batch_num}/{total_batches} ({len(batch_ids)} items)")

        logger.info(f"✓ Indexing complete. Total nodes indexed: {len(ids)}")
    except Exception as e:
        logger.error(f"Error during indexing: {str(e)}")
        raise

if __name__ == "__main__":
    main()