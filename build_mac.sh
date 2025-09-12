#!/bin/bash
# Build script for macOS

echo "Installing dependencies..."
pip3 install pyinstaller pillow

echo "Building macOS app..."
pyinstaller --onefile --windowed --name "NominalwertRechner" nominalwert_rechner.py

echo "Creating .app bundle..."
pyinstaller --windowed --name "NominalwertRechner" --add-data "logo.png:." nominalwert_rechner.py

echo "Done! Check the 'dist' folder for:"
echo "- NominalwertRechner (executable)"
echo "- NominalwertRechner.app (app bundle)"
