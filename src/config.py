# src/config.py
from pathlib import Path
import os
import logging
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load .env into environment
BASE_DIR = Path(__file__).resolve().parent.parent
env_path = BASE_DIR / ".env"

if env_path.exists():
    load_dotenv(env_path)
    logger.debug(f"Loaded environment from {env_path}")
else:
    logger.debug(f"No .env file found at {env_path}")

# Map your custom name to HF_TOKEN for libraries that expect it
if os.getenv("hf_token") and not os.getenv("HF_TOKEN"):
    os.environ["HF_TOKEN"] = os.getenv("hf_token")
    logger.debug("Mapped hf_token to HF_TOKEN environment variable")

DATA_RAW_DIR = BASE_DIR / "data" / "raw"
DATA_PROCESSED_DIR = BASE_DIR / "data" / "processed"
CHROMA_DIR = BASE_DIR / "index" / "chroma_db"

EMBED_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

# Create directories if they don't exist
for d in [DATA_RAW_DIR, DATA_PROCESSED_DIR, CHROMA_DIR]:
    d.mkdir(parents=True, exist_ok=True)

logger.debug(f"BASE_DIR: {BASE_DIR}")
logger.debug(f"DATA_RAW_DIR: {DATA_RAW_DIR}")
logger.debug(f"DATA_PROCESSED_DIR: {DATA_PROCESSED_DIR}")
logger.debug(f"CHROMA_DIR: {CHROMA_DIR}")