#!/bin/bash
# Mac Build Script for GitHub Release - Nominalwert-Rechner
# Run this on macOS to create distributable Mac version

set -e  # Exit on any error

echo "🍎 Building Nominalwert-Rechner for macOS..."
echo "============================================"

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3 first:"
    echo "   brew install python3"
    exit 1
fi

# Check if pip is available
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 not found. Please install pip3 first"
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"

# Create virtual environment for clean build
echo "📦 Creating virtual environment..."
python3 -m venv venv_build
source venv_build/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install --upgrade pip
pip install pyinstaller pillow customtkinter

# Verify logo.png exists
if [ ! -f "logo.png" ]; then
    echo "⚠️  Warning: logo.png not found. App will work but without icon."
fi

# Create executable (single file)
echo "🔨 Building single executable..."
pyinstaller --onefile \
    --windowed \
    --name "NominalwertRechner" \
    --icon="logo.png" \
    --add-data "logo.png:." \
    --hidden-import="PIL._tkinter_finder" \
    nominalwert_rechner.py

# Create .app bundle (recommended for Mac distribution)
echo "📱 Building .app bundle..."
pyinstaller --windowed \
    --name "NominalwertRechner" \
    --icon="logo.png" \
    --add-data "logo.png:." \
    --hidden-import="PIL._tkinter_finder" \
    nominalwert_rechner.py

# Clean up build files but keep dist
echo "🧹 Cleaning up..."
rm -rf build/
rm -rf __pycache__/
rm -f *.spec

# Create release folder structure
echo "📁 Creating release structure..."
mkdir -p releases/mac/
cp -r dist/NominalwertRechner.app releases/mac/
cp dist/NominalwertRechner releases/mac/NominalwertRechner_executable

# Create DMG (if hdiutil available)
if command -v hdiutil &> /dev/null; then
    echo "💿 Creating DMG installer..."
    mkdir -p dmg_temp
    cp -r dist/NominalwertRechner.app dmg_temp/
    
    # Create symbolic link to Applications folder
    ln -sf /Applications dmg_temp/Applications
    
    hdiutil create -volname "Nominalwert-Rechner" \
        -srcfolder dmg_temp \
        -ov -format UDZO \
        releases/mac/NominalwertRechner-Mac.dmg
    
    rm -rf dmg_temp
    echo "✅ DMG created: releases/mac/NominalwertRechner-Mac.dmg"
fi

# Deactivate virtual environment
deactivate
rm -rf venv_build

echo ""
echo "🎉 Mac build completed successfully!"
echo "📂 Files created in releases/mac/:"
echo "   • NominalwertRechner.app (recommended - drag to Applications)"
echo "   • NominalwertRechner_executable (single file executable)"
if command -v hdiutil &> /dev/null; then
    echo "   • NominalwertRechner-Mac.dmg (installer)"
fi
echo ""
echo "📋 Next steps for GitHub release:"
echo "1. Test the .app on different Mac versions"
echo "2. Upload to GitHub Releases"
echo "3. Add installation instructions to README"
echo ""
echo "⚠️  Note: For distribution outside App Store, users may need to:"
echo "   System Preferences → Security & Privacy → Allow apps from identified developers"
