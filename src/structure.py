import json
from pathlib import Path
from typing import List, Dict, Any
import logging
from .config import DATA_PROCESSED_DIR, DATA_RAW_DIR

from unstructured.partition.pdf import partition_pdf
import re

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def build_tree_from_elements(elements) -> Dict[str, Any]:
    """
    Improved heuristic:
    - Treat elements with category Title/Header as headings.
    - Also treat lines starting with patterns like '1.', '2.', 'Section' as headings.
    - Maintain a simple stack of section headings to build section_path.
    """
    doc_tree = {
        "nodes": []
    }

    section_stack: List[str] = []
    node_id = 0

    heading_pattern = re.compile(r"^(\d+(\.\d+)*)\.?\s+")  # matches '1.', '1.1.', etc.
    section_keyword_pattern = re.compile(r"^(Section\s+\d+|[A-Z][A-Za-z0-9\s]+Policy)")

    for el in elements:
        text = (el.text or "").strip()
        if not text:
            continue

        category = getattr(el, "category", "")
        is_heading = category in {"Title", "Header"}

        # Heuristic: also treat numbered or "Section X" lines as headings
        if not is_heading:
            if heading_pattern.match(text) or section_keyword_pattern.match(text):
                is_heading = True

        if is_heading:
            # Start a new section at top level for now
            section_stack = [text]
        else:
            if not section_stack:
                section_stack = ["ROOT"]

        node = {
            "id": node_id,
            "page": getattr(el, "page_number", None),
            "type": category or "Text",
            "text": text,
            "section_path": " > ".join(section_stack),
        }
        doc_tree["nodes"].append(node)
        node_id += 1

    return doc_tree

def process_pdf(pdf_path: Path):
    try:
        logger.info(f"Processing PDF: {pdf_path}")
        elements = partition_pdf(filename=str(pdf_path))
        logger.info(f"Extracted {len(elements)} elements from {pdf_path.name}")
        tree = build_tree_from_elements(elements)
        return tree
    except Exception as e:
        logger.error(f"Error processing {pdf_path}: {str(e)}")
        raise

def main():
    DATA_PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    pdf_files = list(DATA_RAW_DIR.glob("**/*.pdf"))
    
    if not pdf_files:
        logger.warning(f"No PDF files found in {DATA_RAW_DIR}")
        return

    logger.info(f"Found {len(pdf_files)} PDF files to process")
    
    for idx, pdf in enumerate(pdf_files, 1):
        try:
            logger.info(f"[{idx}/{len(pdf_files)}] Structuring {pdf.name}...")
            tree = process_pdf(pdf)
            out_path = DATA_PROCESSED_DIR / (pdf.stem + ".json")
            with open(out_path, "w", encoding="utf-8") as f:
                json.dump(tree, f, ensure_ascii=False, indent=2)
            logger.info(f" ✓ Saved {out_path} with {len(tree['nodes'])} nodes")
        except Exception as e:
            logger.error(f"Failed to process {pdf.name}: {str(e)}")
            continue

if __name__ == "__main__":
    main()

