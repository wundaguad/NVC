# 🍎 Mac Version - Nominalwert-Rechner

## Option 1: Python direkt ausführen (Einfachste Lösung)

**Mac-User brauchen:**
```bash
# Python 3 installieren (falls nicht vorhanden)
brew install python3

# Dependencies installieren
pip3 install pillow

# App ausführen
python3 nominalwert_rechner.py
```

## Option 2: Executable für Mac erstellen

**Du brauchst einen Mac oder macOS VM:**
```bash
# Dependencies installieren
pip3 install pyinstaller pillow

# Executable erstellen
pyinstaller --onefile --windowed --name "NominalwertRechner" nominalwert_rechner.py

# Oder als .app Bundle
pyinstaller --windowed --name "NominalwertRechner" nominalwert_rechner.py
```

## Option 3: Cross-Platform mit cx_Freeze

**Alternative zu PyInstaller:**
```bash
pip install cx_Freeze
python setup.py build
```

## Option 4: Web-Version (Alle Plattformen)

**Mit Streamlit oder Flask:**
- Läuft im Browser
- Funktioniert auf Windows, Mac, Linux
- Keine Installation nötig

## 📦 Verteilung für Mac-User

**Einfachste Lösung:**
1. Schicke das Python-Script + requirements.txt
2. Mac-User führen es mit Python aus

**Professionelle Lösung:**
1. Erstelle .app Bundle auf einem Mac
2. Signiere die App (für Gatekeeper)
3. Erstelle .dmg Installer
