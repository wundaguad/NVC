# 🍎 Mac Installation Guide - Nominalwert-Rechner

## Quick Install (Recommended)

### Option 1: DMG Installer
1. Download `NominalwertRechner-Mac.dmg` from GitHub Releases
2. Double-click the DMG file to mount it
3. Drag `NominalwertRechner.app` to the Applications folder
4. **First run**: Right-click the app → "Open" (bypasses Gatekeeper)
5. Click "Open" in the security dialog

### Option 2: Web Version (No Installation)
1. Download `NominalwertRechner_Exact.html`
2. Double-click to open in Safari/Chrome/Firefox
3. Works offline - bookmark for easy access

## Building from Source

### Prerequisites
```bash
# Install Homebrew (if not installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python 3
brew install python3
```

### Build Steps
```bash
# Clone repository
git clone https://github.com/yourusername/nominalwert-rechner.git
cd nominalwert-rechner

# Make build script executable
chmod +x build_mac_github.sh

# Build the app
./build_mac_github.sh
```

## Troubleshooting

### Security & Gatekeeper Issues

**Problem**: "App can't be opened because it's from an unidentified developer"
**Solution**:
1. Right-click the app → "Open"
2. Click "Open" in the dialog
3. Or: System Preferences → Security & Privacy → "Open Anyway"

**Problem**: "App is damaged and can't be opened"
**Solution**:
```bash
# Remove quarantine attribute
xattr -cr /Applications/NominalwertRechner.app
```

### Python Method (Alternative)

If the app doesn't work, run directly with Python:
```bash
# Install dependencies
pip3 install pillow customtkinter

# Run the app
python3 nominalwert_rechner.py
```

### Apple Silicon (M1/M2) Notes
- App is built with universal binaries
- Should work natively on both Intel and Apple Silicon
- If issues occur, try the Python method above

## System Requirements
- macOS 10.14 (Mojave) or later
- 50MB free disk space
- No internet connection required (offline app)

## Uninstall
Simply drag the app from Applications to Trash.

Settings are stored in: `~/Library/Application Support/NominalwertRechner/`
