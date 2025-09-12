@echo off
echo Installing PyInstaller...
pip install pyinstaller pillow

echo Building executable...
pyinstaller --onefile --windowed --name "NominalwertRechner" --icon=logo.png nominalwert_rechner.py

echo Done! Check the 'dist' folder for your executable.
pause
