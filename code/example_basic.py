"""
Basic Example: Using Device Setup
==================================
Demonstrates how to use the device configuration in your experiments.
"""

import torch
import torch.nn as nn
from genaibook.core import get_device
from config import set_seed, print_config

# Set random seed for reproducibility
set_seed(42)

# Print configuration
print_config()

def main():
    """Basic example of model training with device setup."""
    
    print("🚀 Starting Basic Example\n")
    
    # Get device
    device = get_device()
    print(f"✅ Using device: {device}\n")
    
    # Define a simple model
    class SimpleModel(nn.Module):
        def __init__(self, input_size=784, hidden_size=128, output_size=10):
            super(SimpleModel, self).__init__()
            self.fc1 = nn.Linear(input_size, hidden_size)
            self.relu = nn.ReLU()
            self.fc2 = nn.Linear(hidden_size, output_size)
        
        def forward(self, x):
            x = self.fc1(x)
            x = self.relu(x)
            x = self.fc2(x)
            return x
    
    # Initialize model and move to device
    print("🏗️  Creating model...")
    model = SimpleModel().to(device)
    print(f"   Model parameters: {sum(p.numel() for p in model.parameters()):,}")
    print(f"   Model device: {next(model.parameters()).device}\n")
    
    # Create dummy data
    print("📊 Creating dummy data...")
    batch_size = 32
    input_size = 784
    
    # Input tensor (batch_size, input_size)
    x = torch.randn(batch_size, input_size).to(device)
    print(f"   Input shape: {x.shape}")
    print(f"   Input device: {x.device}\n")
    
    # Forward pass
    print("⚡ Running forward pass...")
    with torch.no_grad():
        output = model(x)
    
    print(f"   Output shape: {output.shape}")
    print(f"   Output device: {output.device}")
    print(f"   Sample output: {output[0][:5].cpu().numpy()}\n")
    
    # Memory usage (if CUDA)
    if device.type == "cuda":
        allocated = torch.cuda.memory_allocated(device) / (1024**2)
        cached = torch.cuda.memory_reserved(device) / (1024**2)
        print(f"💾 GPU Memory:")
        print(f"   Allocated: {allocated:.2f} MB")
        print(f"   Cached: {cached:.2f} MB\n")
    
    print("✅ Example completed successfully!\n")
    
    return model, device

if __name__ == "__main__":
    model, device = main()
    
    print("=" * 60)
    print("💡 Next Steps:")
    print("   1. Modify this script for your experiments")
    print("   2. Check the transformers/ folder for advanced examples")
    print("   3. Review config.py to adjust hyperparameters")
    print("=" * 60)
