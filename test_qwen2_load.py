from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

MODEL_NAME = "Qwen/Qwen2-0.5B-Instruct"

print("Loading tokenizer...")
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

print("Loading model...")
model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    torch_dtype="auto",
    device_map="auto",
)

print("Model loaded successfully")

prompt = "You are a finance analyst. Explain what a capitalization threshold is in one short paragraph."
inputs = tokenizer(prompt, return_tensors="pt")
if torch.cuda.is_available():
    inputs = {k: v.to("cuda") for k, v in inputs.items()}

print("Generating...")
with torch.no_grad():
    outputs = model.generate(
        **inputs,
        max_new_tokens=128,
        do_sample=False,
        pad_token_id=tokenizer.eos_token_id,
    )

print("\n=== Output ===\n")
print(tokenizer.decode(outputs[0], skip_special_tokens=True))