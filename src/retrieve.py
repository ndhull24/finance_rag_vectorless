# src/retrieve.py
import chromadb
import logging
from .config import CHROMA_DIR

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def get_collection():
    try:
        client = chromadb.PersistentClient(path=str(CHROMA_DIR))
        # IMPORTANT: use the existing collection name from list_collections
        collection = client.get_or_create_collection("finance_docs")
        return collection
    except Exception as e:
        logger.error(f"Error accessing collection: {str(e)}")
        raise

def search(query: str, k: int = 5):
    try:
        collection = get_collection()
        results = collection.query(
            query_texts=[query],
            n_results=k,
        )
        docs = results["documents"][0]
        metas = results["metadatas"][0]
        logger.debug(f"Search returned {len(docs)} results for query: {query[:50]}...")
        return list(zip(docs, metas))
    except Exception as e:
        logger.error(f"Error during search: {str(e)}")
        return []

def demo():
    logger.info("Starting Finance RAG – Retrieval demo")
    try:
        while True:
            q = input("\nQuery (empty to quit): ").strip()
            if not q:
                logger.info("Exiting demo")
                break
            hits = search(q, k=5)
            if not hits:
                print("\nNo results found")
                continue
                
            print("\nTop matches:")
            for i, (text, meta) in enumerate(hits, 1):
                print(f"\n[{i}] {meta['doc_name']} | {meta['section_path']}")
                print(text[:400], "..." if len(text) > 400 else "")
    except KeyboardInterrupt:
        logger.info("Demo interrupted by user")
        print("\nGoodbye!")

if __name__ == "__main__":
    demo()