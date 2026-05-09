from typing import List, Tuple, Dict
import logging
from src.retrieve import search
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import time

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# NEW: quiet external libraries
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("huggingface_hub").setLevel(logging.WARNING)
logging.getLogger("transformers").setLevel(logging.WARNING)

MODEL_NAME = "Qwen/Qwen2-0.5B-Instruct"  # Replace with your local model name or path

_tokenizer = None
_model = None

def get_model():
    global _tokenizer, _model
    if _tokenizer is None or _model is None:
        try:
            start = time.time()
            logger.info(f"Loading local model: {MODEL_NAME}")
            _tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
            _model = AutoModelForCausalLM.from_pretrained(
                MODEL_NAME,
                torch_dtype="auto",
                device_map="auto",
            )
            elapsed = time.time() - start
            logger.info(f"✓ Model loaded successfully in {elapsed:.2f} seconds")
        except Exception as e:
            logger.error(f"Error loading model: {str(e)}")
            raise
    return _tokenizer, _model

def build_prompt(question: str, hits: List[Tuple[str, Dict]]) -> str:
    context_blocks = []
    for i, (text, meta) in enumerate(hits, 1):
        doc = meta.get("doc_name", "unknown_doc")
        section = meta.get("section_path", "unknown_section")
        block = f"[{i}] (doc: {doc}, section: {section})\n{text}"
        context_blocks.append(block)

    context_str = "\n\n".join(context_blocks)

    prompt = (
        "You are a finance analyst. Use only the context provided to answer.\n\n"
        f"Question: {question}\n\n"
        f"Context:\n{context_str}\n\n"
        "Answer the question in 3-6 sentences. "
        "Quote the document and section in parentheses when you reference them, "
        "for example: (capitalization_policy, Section 3. Capitalization Thresholds).\n\n"
        "Answer:\n"
    )
    return prompt

def generate_answer(question: str, k: int = 8, max_new_tokens: int = 128):
    """
    Returns (answer_text, metrics_dict)
    """
    try:
        t0 = time.time()
        hits = search(question, k=k)
        if not hits:
            logger.warning(f"No relevant context found for question: {question}")
            return "I couldn't find any relevant context in the indexed documents.", {
                "retrieval_time": 0.0,
                "generation_time": 0.0,
                "total_time": time.time() - t0,
                "num_context_chunks": 0,
                "context_chars": 0,
            }

        tokenizer, model = get_model()
        t1 = time.time()

        prompt = build_prompt(question, hits)
        context_str = "\n\n".join([h[0] for h in hits])

        inputs = tokenizer(prompt, return_tensors="pt")
        if torch.cuda.is_available():
            inputs = {k: v.to("cuda") for k, v in inputs.items()}

        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_new_tokens=max_new_tokens,
                do_sample=False,
                pad_token_id=tokenizer.eos_token_id,
            )

        t2 = time.time()
        full_text = tokenizer.decode(outputs[0], skip_special_tokens=True)

        if "Answer:" in full_text:
            answer = full_text.split("Answer:", 1)[-1].strip()
        else:
            answer = full_text.strip()

        metrics = {
            "retrieval_time": t1 - t0,
            "generation_time": t2 - t1,
            "total_time": t2 - t0,
            "num_context_chunks": len(hits),
            "context_chars": len(context_str),
        }

        logger.info(
            f"Timing – retrieval: {metrics['retrieval_time']:.2f}s, "
            f"generation: {metrics['generation_time']:.2f}s, "
            f"total: {metrics['total_time']:.2f}s"
        )

        return answer, metrics
    except Exception as e:
        logger.error(f"Error generating answer: {str(e)}")
        raise

def demo():
    logger.info("Starting Finance RAG – Answering demo")
    try:
        while True:
            q = input("\nQuestion (empty to quit): ").strip()
            if not q:
                logger.info("Exiting demo")
                break
            try:
                ans = generate_answer(q)
                print("\nAnswer:\n", ans, "\n")
            except Exception as e:
                logger.error(f"Error processing question: {str(e)}")
                print(f"Error: {str(e)}\n")
    except KeyboardInterrupt:
        logger.info("Demo interrupted by user")
        print("\nGoodbye!")

if __name__ == "__main__":
    demo()
