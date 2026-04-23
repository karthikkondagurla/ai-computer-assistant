#!/bin/bash
# macOS Build Script for AI Computer Assistant
# Run this script on macOS to build the executable

echo "========================================"
echo "Building AI Computer Assistant for macOS"
echo "========================================"

# Install PyInstaller if not present
pip install pyinstaller

# Build the executable
pyinstaller --onefile --console --name "AI-Assistant" \
  --target-arch universal2 \
  --add-data "src:src" \
  --hidden-import langchain_groq \
  --hidden-import langchain \
  --hidden-import langchain_core \
  --hidden-import langgraph \
  --hidden-import groq \
  --hidden-import pyautogui \
  --hidden-import psutil \
  --hidden-import pyperclip \
  --hidden-import pillow \
  --hidden-import keyring \
  --hidden-import secretstorage \
  --hidden-import jeepney \
  --hidden-import pyscreeze \
  --hidden-import pygetwindow \
  --hidden-import pymsgbox \
  --hidden-import pytweening \
  --hidden-import mouseinfo \
  --collect-all langchain \
  --collect-all langchain_groq \
  --collect-all langgraph \
  --collect-all keyring \
  ai_computer_assistant.py

if [ $? -eq 0 ]; then
    echo ""
    echo "========================================"
    echo "Build successful!"
    echo "Executable location: dist/AI-Assistant"
    echo "========================================"
else
    echo ""
    echo "========================================"
    echo "Build failed!"
    echo "========================================"
    exit 1
fi

echo ""
echo "To create DMG, run: create-dmg or hdiutil"
echo "Example: hdiutil create -volname 'AI Assistant' -srcfolder dist/AI-Assistant.app -ovf AI-Assistant.dmg"