# 🛡️ Windows Security Warning - NVC

## ⚠️ "Windows protected your PC" Message

When downloading and running `NominalwertRechner.exe`, Windows may show this security warning. **This is completely normal** for unsigned software.

## 🔧 How to Run the App

### Method 1: SmartScreen Bypass
1. Click **"More info"** in the warning dialog
2. Click **"Run anyway"** 
3. The app will start normally

### Method 2: Unblock File
1. Right-click `NominalwertRechner.exe`
2. Select **"Properties"**
3. Check **"Unblock"** at the bottom
4. Click **"OK"**
5. Double-click to run normally

### Method 3: Add Exception
If your antivirus blocks it:
1. Add `NominalwertRechner.exe` to antivirus exceptions
2. Or temporarily disable real-time protection

## 🔒 Why This Happens

- **Unsigned Software**: The app isn't code-signed with an expensive certificate
- **Unknown Publisher**: Windows doesn't recognize "WUNDAGUAD" as verified publisher
- **New File**: Downloaded executables are treated as potentially unsafe

## ✅ Is It Safe?

**Yes, completely safe:**
- ✅ **Open Source**: Full code available on GitHub
- ✅ **No Network**: App works offline, no data sent anywhere
- ✅ **No Installation**: Portable executable, no system changes
- ✅ **Virus Scan**: You can scan with any antivirus

## 🚀 Alternative Options

If you prefer not to bypass security warnings:

1. **Web Version**: Use `NominalwertRechner_Exact.html` in browser
2. **Python Source**: Run directly with `python nominalwert_rechner.py`
3. **Wait for Updates**: Future versions may include code signing

## 📞 Still Concerned?

- **Scan the file** with your antivirus before running
- **Check the source code** on GitHub: https://github.com/wundaguad/NVC
- **Use web version** if you prefer browser-based tools

---

**This warning is standard for all unsigned executables downloaded from the internet. Major software like OBS Studio, 7-Zip, and many indie games show the same warning.**
