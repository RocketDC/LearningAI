# Generative AI Python Project

Python environment for hands-on experiments with transformers and diffusion models.

---

## 🚀 Quick Setup

### 1. Create Virtual Environment

```bash
# Navigate to project directory
cd learning/generative-ai-transformers-diffusion/code

# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate  # On macOS/Linux
# OR
venv\Scripts\activate     # On Windows
```

### 2. Install Dependencies

```bash
# Upgrade pip first
pip install --upgrade pip

# Install PyTorch (with CUDA support if available)
# Visit https://pytorch.org/get-started/locally/ for your specific setup
# Example for CUDA 11.8:
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# Install other requirements
pip install -r requirements.txt

# Install genaibook (book's companion library)
# Follow book instructions or:
pip install genaibook
```

### 3. Test CUDA Setup

```bash
python setup_device.py
```

Expected output:
- ✅ Device information (CUDA or CPU)
- 🎮 GPU details (if available)
- 🧪 Test tensor creation

---

## 📁 Project Structure

```
code/
├── README.md              # This file
├── requirements.txt       # Python dependencies
├── setup_device.py        # CUDA detection script
├── transformers/          # Transformer experiments
├── diffusion/             # Diffusion model experiments
└── projects/              # End-to-end projects
```

---

## 🔧 Scripts

### `setup_device.py`
Detects and configures CUDA device for training/inference.

**Usage:**
```python
from setup_device import main
device = main()

# Use in your code
import torch
model = YourModel().to(device)
```

---

## 💡 Tips

**No GPU?** Use these alternatives:
- **Google Colab:** Free GPU access (T4, sometimes A100)
- **Kaggle Notebooks:** Free P100 GPUs
- **Cloud Platforms:** AWS, GCP, Azure (paid)

**Memory Issues?**
- Use smaller batch sizes
- Enable gradient checkpointing
- Use mixed precision training (fp16)

---

## 📚 Resources

- **Book Code:** Check O'Reilly platform for official repository
- **PyTorch Docs:** https://pytorch.org/docs/
- **Hugging Face:** https://huggingface.co/docs

---

## ✅ Verification Checklist

- [ ] Virtual environment created
- [ ] Dependencies installed
- [ ] CUDA device detected (or CPU confirmed)
- [ ] Test script runs successfully

**Ready to start experimenting! 🚀**
