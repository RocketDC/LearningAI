"""
CUDA Device Setup
=================
Script to detect and assign CUDA device for generative AI experiments.
Uses genaibook.core library from the O'Reilly book.
"""

from genaibook.core import get_device
import torch

def main():
    """Detect and display available compute device."""
    
    print("=" * 50)
    print("🔧 Device Detection & Setup")
    print("=" * 50)
    
    # Get the optimal device (CUDA if available, else CPU)
    device = get_device()
    
    print(f"\n✅ Selected Device: {device}")
    print(f"   Device Type: {device.type}")
    
    # Additional CUDA information if available
    if device.type == "cuda":
        print(f"\n🎮 CUDA Device Information:")
        print(f"   CUDA Available: {torch.cuda.is_available()}")
        print(f"   CUDA Version: {torch.version.cuda}")
        print(f"   Device Count: {torch.cuda.device_count()}")
        print(f"   Current Device: {torch.cuda.current_device()}")
        print(f"   Device Name: {torch.cuda.get_device_name(0)}")
        print(f"   Device Capability: {torch.cuda.get_device_capability(0)}")
        
        # Memory information
        total_memory = torch.cuda.get_device_properties(0).total_memory / (1024**3)
        print(f"   Total Memory: {total_memory:.2f} GB")
        
        allocated_memory = torch.cuda.memory_allocated(0) / (1024**3)
        print(f"   Allocated Memory: {allocated_memory:.2f} GB")
        
        cached_memory = torch.cuda.memory_reserved(0) / (1024**3)
        print(f"   Cached Memory: {cached_memory:.2f} GB")
    else:
        print(f"\n⚠️  CUDA not available. Running on CPU.")
        print(f"   Consider using Google Colab or a cloud GPU for better performance.")
    
    print("\n" + "=" * 50)
    
    return device

if __name__ == "__main__":
    device = main()
    
    # Test with a simple tensor
    print("\n🧪 Testing device with a sample tensor...")
    test_tensor = torch.randn(3, 3).to(device)
    print(f"   Test tensor created on: {test_tensor.device}")
    print(f"   Tensor shape: {test_tensor.shape}")
    print("\n✅ Device setup complete!")
