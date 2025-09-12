# 🍎 Mac Security Warning - NVC

## ⚠️ Gatekeeper Protection

Mac has a similar security system called **Gatekeeper** that blocks unsigned applications from unidentified developers.

## 🚨 Common Mac Warning Messages

### "Cannot be opened because it is from an unidentified developer"
### "App is damaged and can't be opened"
### "macOS cannot verify that this app is free from malware"

## 🔧 How to Run the App on Mac

### Method 1: Right-Click Override (Recommended)
1. **Right-click** (or Control+click) on `NominalwertRechner.app`
2. Select **"Open"** from context menu
3. Click **"Open"** in the security dialog
4. App will run and be trusted for future launches

### Method 2: System Preferences
1. Go to **System Preferences** → **Security & Privacy**
2. Click **"Open Anyway"** (appears after first attempt to run)
3. Enter your admin password if prompted

### Method 3: Remove Quarantine (Advanced)
```bash
# Open Terminal and run:
xattr -cr /Applications/NominalwertRechner.app
```

### Method 4: Temporary Gatekeeper Disable (Not recommended)
```bash
# Disable Gatekeeper temporarily
sudo spctl --master-disable

# Re-enable after installing
sudo spctl --master-enable
```

## 🔒 Why This Happens on Mac

- **Unsigned Application**: No Apple Developer Certificate ($99/year)
- **Downloaded from Internet**: Quarantine flag added by Safari/browsers
- **Unknown Developer**: "WUNDAGUAD" not registered with Apple
- **Gatekeeper Protection**: macOS security feature since 10.8

## 📱 macOS Version Differences

### macOS Catalina (10.15) and newer:
- Stricter notarization requirements
- May show "damaged" message even for valid apps

### macOS Big Sur/Monterey/Ventura:
- Additional security prompts
- May need multiple "Open" attempts

### Apple Silicon (M1/M2):
- Same security warnings
- App runs natively (no Rosetta needed)

## ✅ Is It Safe?

**Yes, completely safe:**
- ✅ **Open Source**: Full code on GitHub
- ✅ **No Network Access**: Works offline
- ✅ **No System Modifications**: Portable app
- ✅ **Virus Scan**: Scan with any Mac antivirus

## 🚀 Alternative Options for Mac Users

1. **Build from Source**:
   ```bash
   git clone https://github.com/wundaguad/NVC.git
   cd NVC
   pip3 install -r requirements.txt
   python3 nominalwert_rechner.py
   ```

2. **Web Version**: Use `NominalwertRechner_Exact.html` in Safari/Chrome

3. **Homebrew** (if we add it):
   ```bash
   brew install --cask nominalwert-rechner
   ```

## 🔐 System Requirements

- **macOS**: 10.14 (Mojave) or later
- **Architecture**: Intel x64 or Apple Silicon (M1/M2)
- **Permissions**: No special permissions needed
- **Dependencies**: None (all bundled in .app)

## 📞 Still Having Issues?

- **Check Console.app** for detailed error messages
- **Try different download method** (direct vs. browser)
- **Verify file integrity** with `shasum -a 256`
- **Contact support** via GitHub Issues

---

**This is standard macOS behavior for all unsigned applications. Popular apps like Discord, Spotify, and many indie games show similar warnings until they get expensive Apple certificates.**
