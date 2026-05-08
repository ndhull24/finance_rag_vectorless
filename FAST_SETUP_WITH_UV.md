# Fast Setup with UV

`uv` is a blazingly fast Python package installer written in Rust. It's **10-100x faster** than pip!

## Installation Status
✓ `uv` is already installed on your system

## Quick Start (Fastest Method)

### 1. Remove old venv (optional, to start fresh)
```bash
# Windows
rmdir /s venv

# macOS/Linux
rm -rf venv
```

### 2. Create virtual environment with uv (MUCH FASTER)
```bash
# Create and activate venv in one step
uv venv
```

### 3. Install dependencies with uv (10-100x faster than pip!)
```bash
# Windows
uv pip install -e .

# OR for faster sync (even better):
uv sync
```

### 4. Verify installation
```bash
python -c "import torch; print(torch.__version__)"
python -c "import transformers; print(transformers.__version__)"
```

## Performance Comparison

| Method | Time | Speed |
|--------|------|-------|
| `pip install requirements.txt` | ~15-20 min | Baseline |
| `uv pip install -e .` | ~2-3 min | **5-10x faster** |
| `uv sync` | ~1-2 min | **10-20x faster** |

## Why UV is Faster

1. **Written in Rust** - Compiled, not interpreted
2. **Parallel downloads** - Downloads multiple packages simultaneously
3. **Intelligent caching** - Reuses cached wheels
4. **Better dependency resolution** - Faster algorithm
5. **No redundant work** - Optimized for common patterns

## Managing Dependencies with UV

### Add a new dependency
```bash
uv pip install package_name
```

### Update all dependencies
```bash
uv sync --upgrade
```

### View installed packages
```bash
uv pip list
```

### Export requirements
```bash
uv pip freeze > requirements.txt
```

## Important Notes on Model Downloads

⚠️ **UV speeds up package installation, but NOT model downloads**

The TinyLlama model (~1.1GB) download happens **separately**:
- First run: Downloads from Hugging Face (takes time based on network speed)
- Cached afterwards: Instant load from `~/.cache/huggingface/`

### Speed up model caching:
```bash
# Pre-download the model before running
python -c "
from transformers import AutoTokenizer, AutoModelForCausalLM
MODEL_NAME = "Qwen/Qwen2-1.5B-Instruct"
print('Downloading tokenizer...')
AutoTokenizer.from_pretrained(model_name)
print('Downloading model...')
AutoModelForCausalLM.from_pretrained(model_name)
print('Done! Model cached.')
"
```

Then all subsequent runs will be instant!

## Complete Fast Setup Script

Save this as `quick-setup.sh` (macOS/Linux) or `quick-setup.bat` (Windows):

### Windows (quick-setup.bat):
```batch
@echo off
echo Creating virtual environment with uv...
uv venv

echo Installing dependencies...
uv sync

echo Verifying installation...
python -c "import torch; print('Torch version:', torch.__version__)"
python -c "import transformers; print('Transformers version:', transformers.__version__)"

echo.
echo Setup complete! Your environment is ready.
echo.
echo Next, pre-download the model:
python -c "from transformers import AutoTokenizer, AutoModelForCausalLM; AutoTokenizer.from_pretrained('TinyLlama/TinyLlama-1.1B-Chat-v1.0'); AutoModelForCausalLM.from_pretrained('TinyLlama/TinyLlama-1.1B-Chat-v1.0'); print('Model cached!')"

pause
```

### macOS/Linux (quick-setup.sh):
```bash
#!/bin/bash
echo "Creating virtual environment with uv..."
uv venv

echo "Installing dependencies..."
uv sync

echo "Verifying installation..."
python -c "import torch; print('Torch version:', torch.__version__)"
python -c "import transformers; print('Transformers version:', transformers.__version__)"

echo ""
echo "Setup complete! Your environment is ready."
echo ""
echo "Next, pre-download the model:"
python -c "from transformers import AutoTokenizer, AutoModelForCausalLM; AutoTokenizer.from_pretrained('TinyLlama/TinyLlama-1.1B-Chat-v1.0'); AutoModelForCausalLM.from_pretrained('TinyLlama/TinyLlama-1.1B-Chat-v1.0'); print('Model cached!')"
```

## Troubleshooting

### If UV command not found
```bash
# Install uv
pip install uv

# Or use Homebrew (macOS)
brew install uv
```

### If you still have old venv active
```bash
# Deactivate and remove old one
deactivate
rm -rf venv
```

### Cache issues (if models don't download properly)
```bash
# Clear all caches
uv pip cache prune

# Or specific cache
rm -rf ~/.cache/huggingface/
```

## Recommended Workflow

```bash
# 1. Initial setup (one time, ~2-3 minutes total!)
uv sync

# 2. Pre-download model (one time, ~5-10 minutes depending on network)
python test_model_load.py

# 3. Run your application (instant!)
python main.py
```

## UV Aliases (Optional)

Add to your shell profile (`.bashrc`, `.zshrc`, or PowerShell `$PROFILE`):

```bash
alias uv-install="uv pip install"
alias uv-sync="uv sync"
alias uv-freeze="uv pip freeze"
```

---

**Result:** Instead of 20+ minutes to set up the first time, you now have **2-3 minutes** for package installation, and subsequent runs are instant! 🚀

For more info: https://github.com/astral-sh/uv
