import sys
import logging
from pathlib import Path

# Configure encoding for Windows compatibility
if sys.platform == "win32":
    import os
    os.environ['PYTHONIOENCODING'] = 'utf-8'

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    """Finance RAG main entry point - orchestrate the complete pipeline"""
    logger.info("=" * 60)
    logger.info("Finance RAG System")
    logger.info("=" * 60)
    
    from src.config import DATA_PROCESSED_DIR, CHROMA_DIR
    
    print("""
┌───────────────────────────────────────────────────────────────┐
│         Finance RAG Copilot v0.1.0                            │
│  A Hybrid Vectorless + Vector RAG System                      │
└───────────────────────────────────────────────────────────────┘

Please choose an option:
  1. Structure PDFs                  (parse PDFs -> JSON trees)
  2. Build Vector Index              (generate embeddings & index)
  3. Run CLI Query Demo              (interactive retrieval)
  4. Run Answer Generation Demo      (retrieval + generation)
  5. Test Model Loading              (verify GPU/model setup)
  6. List Indexed Collections        (show what's indexed)
  
  0. Exit
""")
    
    choice = input("Enter your choice (0-6): ").strip()
    
    try:
        if choice == "1":
            logger.info("Starting PDF structuring pipeline...")
            from src.structure import main as structure_main
            structure_main()
            
        elif choice == "2":
            logger.info("Starting vector index building pipeline...")
            if not list(DATA_PROCESSED_DIR.glob("**/*.json")):
                logger.warning("No processed JSON files found. Run option 1 first.")
                return
            from src.embed_index import main as embed_main
            embed_main()
            
        elif choice == "3":
            logger.info("Starting CLI retrieval demo...")
            if not list(CHROMA_DIR.glob("**/*")):
                logger.warning("No index found. Run option 2 first.")
                return
            from src.retrieve import demo as retrieve_demo
            retrieve_demo()
            
        elif choice == "4":
            logger.info("Starting answer generation demo...")
            if not list(CHROMA_DIR.glob("**/*")):
                logger.warning("No index found. Run option 2 first.")
                return
            from src.answer import demo as answer_demo
            answer_demo()
            
        elif choice == "5":
            logger.info("Testing model setup...")
            import test_qwen2_load
            test_qwen2_load.test_model_load()
            
        elif choice == "6":
            logger.info("Listing indexed collections...")
            from src.list_collections import main as list_main
            list_main()
            
        elif choice == "0":
            logger.info("Exiting Finance RAG")
            sys.exit(0)
        else:
            logger.warning(f"Invalid choice: {choice}")
            
    except KeyboardInterrupt:
        logger.info("Process interrupted by user")
        print("\nGoodbye!")
    except Exception as e:
        logger.error(f"Error during execution: {str(e)}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()
