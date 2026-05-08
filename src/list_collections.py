import chromadb
import logging
from .config import CHROMA_DIR

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    try:
        client = chromadb.PersistentClient(path=str(CHROMA_DIR))
        cols = client.list_collections()
        logger.info(f"CHROMA_DIR: {CHROMA_DIR}")
        logger.info(f"Found {len(cols)} collection(s):")
        for c in cols:
            logger.info(f"  • {c.name} ({c.count()} items)")
        if not cols:
            logger.warning("No collections found. Run src.embed_index to create one.")
    except Exception as e:
        logger.error(f"Error listing collections: {str(e)}")
        raise

if __name__ == "__main__":
    main()