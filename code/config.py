"""
Project Configuration
=====================
Centralized configuration for all experiments.
"""

import torch
from pathlib import Path

# Project Paths
PROJECT_ROOT = Path(__file__).parent
DATA_DIR = PROJECT_ROOT / "data"
MODELS_DIR = PROJECT_ROOT / "models"
OUTPUTS_DIR = PROJECT_ROOT / "outputs"
LOGS_DIR = PROJECT_ROOT / "logs"

# Create directories if they don't exist
for directory in [DATA_DIR, MODELS_DIR, OUTPUTS_DIR, LOGS_DIR]:
    directory.mkdir(exist_ok=True, parents=True)

# Device Configuration
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
USE_AMP = torch.cuda.is_available()  # Automatic Mixed Precision

# Training Configuration
BATCH_SIZE = 32 if torch.cuda.is_available() else 8
NUM_WORKERS = 4
LEARNING_RATE = 1e-4
NUM_EPOCHS = 10

# Model Configuration
MAX_LENGTH = 512
SEED = 42

# Logging
VERBOSE = True
LOG_INTERVAL = 10  # Log every N batches

# Set random seeds for reproducibility
def set_seed(seed: int = SEED):
    """Set random seeds for reproducibility."""
    import random
    import numpy as np
    
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    
    if torch.cuda.is_available():
        torch.cuda.manual_seed(seed)
        torch.cuda.manual_seed_all(seed)
        torch.backends.cudnn.deterministic = True
        torch.backends.cudnn.benchmark = False

# Print configuration
def print_config():
    """Display current configuration."""
    print("\n" + "=" * 60)
    print("⚙️  PROJECT CONFIGURATION")
    print("=" * 60)
    print(f"\n📁 Paths:")
    print(f"   Project Root: {PROJECT_ROOT}")
    print(f"   Data: {DATA_DIR}")
    print(f"   Models: {MODELS_DIR}")
    print(f"   Outputs: {OUTPUTS_DIR}")
    
    print(f"\n🎮 Device:")
    print(f"   Device: {DEVICE}")
    print(f"   CUDA Available: {torch.cuda.is_available()}")
    print(f"   Mixed Precision: {USE_AMP}")
    
    print(f"\n🔧 Training:")
    print(f"   Batch Size: {BATCH_SIZE}")
    print(f"   Learning Rate: {LEARNING_RATE}")
    print(f"   Epochs: {NUM_EPOCHS}")
    print(f"   Random Seed: {SEED}")
    
    print("\n" + "=" * 60 + "\n")

if __name__ == "__main__":
    print_config()
