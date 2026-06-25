#!/bin/bash

# MKV Subtitle Translator Setup Script

set -e

echo "Starting installation for MKV Subtitle Translator..."

# 1. Check OS and install system dependencies
if [[ "$OSTYPE" == "macosx"* ]]; then
    echo "Detected macOS..."
    # Check if brew is installed
    if command -v brew >/dev/null; then
        brew install mkvtoolnix ffmpeg
    else
        echo "Error: Homebrew is not installed. Please install it from https://brew.sh/"
        exit 1
    fi
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "Detected Linux..."
    if command -v apt-get >/dev/null; then
        sudo apt-get update
        sudo apt-get install -y mkvtoolnix ffmpeg python3-pip python3-venv
    elif command -v dnf >/dev/null; then
        sudo dnf install -y mkvtoolnix ffmpeg python3-pip python3-devel
    else
        echo "Error: Unsupported Linux distribution. Please install mkvtoolnix and ffmpeg manually."
        exit 1
    fi
else
    echo "Unsupported OS. Please install mkvtoolnix and ffmpeg manually."
    exit 1
fi

# 2. Setup Virtual Environment
echo "Setting up Python virtual environment..."
python3 -m venv .venv
source .venv/bin/activate

# 3. Install Python packages
echo "Installing Python dependencies (ollama, pymkv)..."
pip install --upgrade pip
pip install -r requirements.txt

# 4. Ollama Setup Instructions
echo "-------------------------------------------------------"
echo "System dependencies installed successfully."
echo ""
echo "Next steps for AI:1. Ensure Ollama is running."
echo "2. Run the following command to download the model:"
echo "   ollama pull tranlategemma"
echo "-------------------------------------------------------"
