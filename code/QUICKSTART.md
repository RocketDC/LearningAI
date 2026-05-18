# 🚀 Quick Start Guide

Get up and running with your generative AI Python environment in 5 minutes!

---

## Step 1: Navigate to Project

```bash
cd ~/openclaw/workspace/learning/generative-ai-transformers-diffusion/code
```

---

## Step 2: Run Setup Script

**Option A: Automatic Setup (Recommended)**
```bash
./setup.sh
```

**Option B: Manual Setup**
```bash
# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate

# Install PyTorch (visit pytorch.org for your specific setup)
pip install torch torchvision torchaudio

# Install other dependencies
pip install -r requirements.txt
```

---

## Step 3: Test CUDA Setup

```bash
# Activate environment if not already active
source venv/bin/activate

# Run device setup script
python setup_device.py
```

**Expected Output:**
```
==================================================
🔧 Device Detection & Setup
==================================================

✅ Selected Device: cuda:0
   Device Type: cuda

🎮 CUDA Device Information:
   CUDA Available: True
   CUDA Version: 11.8
   Device Count: 1
   Current Device: 0
   Device Name: NVIDIA GeForce RTX 3080
   ...
```

---

## Step 4: Run Example Script

```bash
python example_basic.py
```

This will:
- Load the device configuration
- Create a simple neural network
- Run a forward pass
- Display memory usage

---

## Step 5: Start Experimenting!

### Check Configuration
```bash
python config.py
```

### Explore Folders
```
code/
├── transformers/    # Put transformer experiments here
├── diffusion/       # Put diffusion model experiments here
└── projects/        # Put end-to-end projects here
```

### Create Your First Experiment
```python
# your_experiment.py
from genaibook.core import get_device
from config import set_seed, BATCH_SIZE, LEARNING_RATE

set_seed(42)
device = get_device()

# Your code here...
```

---

## 🔧 Common Commands

**Activate environment:**
```bash
source venv/bin/activate
```

**Deactivate environment:**
```bash
deactivate
```

**Install new package:**
```bash
pip install package-name
pip freeze > requirements.txt  # Update requirements
```

**Update dependencies:**
```bash
pip install --upgrade -r requirements.txt
```

---

## 🐛 Troubleshooting

### "CUDA not available"
- **Check GPU:** `nvidia-smi` (Linux/Windows with NVIDIA GPU)
- **Reinstall PyTorch with CUDA:** Visit https://pytorch.org
- **Use alternatives:** Google Colab, Kaggle Notebooks (free GPUs)

### "genaibook not found"
- Follow the book's instructions to install the companion library
- It may be in a specific GitHub repo mentioned in the book

### "Out of memory"
- Reduce `BATCH_SIZE` in `config.py`
- Use smaller models for testing
- Clear CUDA cache: `torch.cuda.empty_cache()`

---

## 📚 Resources

- **Book Code:** Check O'Reilly platform
- **PyTorch Tutorial:** https://pytorch.org/tutorials/
- **Hugging Face Docs:** https://huggingface.co/docs

---

## ✅ You're Ready!

Start with Chapter 1 of the book and use this environment for all hands-on exercises.

**Happy learning! 🎓**
