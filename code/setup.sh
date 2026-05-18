#!/bin/bash
# Setup script for Generative AI Python project

echo "=================================================="
echo "🔧 Setting up Generative AI Python Environment"
echo "=================================================="

# Check if we're in the right directory
if [ ! -f "requirements.txt" ]; then
    echo "❌ Error: requirements.txt not found. Are you in the code/ directory?"
    exit 1
fi

# Create virtual environment
echo ""
echo "📦 Creating virtual environment..."
python3 -m venv venv

if [ $? -ne 0 ]; then
    echo "❌ Failed to create virtual environment"
    exit 1
fi

echo "✅ Virtual environment created"

# Activate virtual environment
echo ""
echo "🔌 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo ""
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Detect OS and suggest PyTorch installation
echo ""
echo "=================================================="
echo "📥 PyTorch Installation"
echo "=================================================="
echo ""
echo "Visit https://pytorch.org/get-started/locally/ to get the right command for your system."
echo ""
echo "Example commands:"
echo ""
echo "🐧 Linux/macOS with CUDA 11.8:"
echo "   pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118"
echo ""
echo "🍎 macOS (CPU/MPS):"
echo "   pip install torch torchvision torchaudio"
echo ""
echo "💻 Windows with CUDA 11.8:"
echo "   pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118"
echo ""
read -p "Press Enter to continue with CPU-only PyTorch, or Ctrl+C to install manually first..."

# Install PyTorch (CPU version as fallback)
pip install torch torchvision torchaudio

# Install other requirements
echo ""
echo "📚 Installing other dependencies..."
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ Some packages failed to install"
    echo "   You may need to install genaibook separately following book instructions"
else
    echo "✅ Dependencies installed"
fi

# Test setup
echo ""
echo "🧪 Testing device setup..."
python setup_device.py

echo ""
echo "=================================================="
echo "✅ Setup Complete!"
echo "=================================================="
echo ""
echo "To activate the environment in the future, run:"
echo "   source venv/bin/activate"
echo ""
echo "To deactivate:"
echo "   deactivate"
echo ""
echo "Happy learning! 🚀"
