from pathlib import Path
import logging
from unstructured.partition.pdf import partition_pdf
from .config import DATA_RAW_DIR, DATA_PROCESSED_DIR

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def ingest_pdf(pdf_path: Path):
    try:
        logger.info(f"Ingesting PDF: {pdf_path}")
        elements = partition_pdf(filename=str(pdf_path))
        logger.info(f"Successfully ingested {len(elements)} elements from {pdf_path.name}")
        return elements
    except Exception as e:
        logger.error(f"Error ingesting {pdf_path}: {str(e)}")
        raise

def main():
    DATA_PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    
    pdf_files = list(DATA_RAW_DIR.glob("**/*.pdf"))
    if not pdf_files:
        logger.warning(f"No PDF files found in {DATA_RAW_DIR}")
        return
    
    logger.info(f"Found {len(pdf_files)} PDF files")
    
    for idx, pdf in enumerate(pdf_files, 1):
        try:
            logger.info(f"[{idx}/{len(pdf_files)}] Parsing {pdf.name}...")
            elements = ingest_pdf(pdf)
            logger.info(f" ✓ Extracted {len(elements)} elements")
        except Exception as e:
            logger.error(f"Failed to parse {pdf.name}: {str(e)}")
            continue

if __name__ == "__main__":
    main()