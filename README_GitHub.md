# 🧮 NVC - Nominalwert Calculator

**Professional Trading Position Calculator with Leverage Support**

Created with ❤️ by **WUNDAGUAD** for our community

## 🚀 Features

- **Multi-Platform Support**: Windows, Mac, Linux, Web
- **Leverage Trading**: 1x to 125x leverage calculation
- **Risk Management**: Precise stop-loss and take-profit calculations
- **Multi-Language**: German and English interface
- **Dark Theme**: Professional trading interface
- **Fee Calculation**: Maker/Taker fees included
- **Copy to Clipboard**: Easy result sharing
- **Offline Ready**: No internet connection required

## 📥 Download & Installation

### Windows
1. Download `NominalwertRechner.exe` from [Releases](../../releases)
2. Run the executable - no installation needed
3. Windows may show security warning - click "More info" → "Run anyway"

### Mac
1. Download `NominalwertRechner-Mac.dmg` from [Releases](../../releases)
2. Open DMG and drag app to Applications folder
3. First run: Right-click app → "Open" (bypass Gatekeeper)

### Linux
1. Download source code or clone repository
2. Install Python 3 and dependencies:
   ```bash
   sudo apt install python3 python3-pip python3-tk
   pip3 install pillow customtkinter
   ```
3. Run: `python3 nominalwert_rechner.py`

### Web Version (All Platforms)
1. Download `NominalwertRechner_Exact.html`
2. Open in any web browser
3. Works offline - no installation needed

## 🛠️ Building from Source

### Prerequisites
- Python 3.8+
- pip package manager

### Windows Build
```bash
# Install dependencies
pip install -r requirements.txt

# Build executable
build_app.bat
```

### Mac Build
```bash
# Make script executable
chmod +x build_mac_github.sh

# Build app
./build_mac_github.sh
```

### Dependencies
```
customtkinter>=5.2.0
pillow>=10.0.0
pyinstaller>=5.13.0
```

## 📖 Usage

1. **Select Direction**: Long or Short position
2. **Enter Price**: Current market price
3. **Set Max Loss**: Maximum risk amount (€)
4. **Set Stop-Loss**: Percentage for stop-loss
5. **Adjust Leverage**: Use slider (1x-125x)
6. **Configure Fees**: Optional maker/taker fees
7. **Set Take-Profit**: Optional profit targets
8. **Calculate**: Get position size and risk metrics

## 🔧 Advanced Features

### Trading Fees
- Configurable maker/taker fees
- Automatic fee calculation in P&L
- Support for different exchange fee structures

### Take-Profit Configuration
- Multiple TP levels (25%, 50%, 75%, 100%)
- Automatic profit calculation
- Risk-reward ratio display

### Settings
- Language selection (German/English)
- Number format (German/US)
- Persistent settings storage

## 📊 Calculation Logic

The calculator uses professional trading formulas:

```
Margin Required = Max Loss / Effective Percentage
Nominal Value = Margin Required × Leverage
Effective Percentage = (Stop-Loss % + Fees) / 100
```

**Key Benefits:**
- Exact risk control regardless of leverage
- Professional fee integration
- Accurate position sizing
- Real-time P&L calculation

## 🌐 Multi-Language Support

- **German**: Complete German interface
- **English**: Full English translation
- **Persistent**: Language preference saved
- **Dynamic**: Switch without restart (web version)

## 🎨 Interface

- **Dark Theme**: Professional trading appearance
- **Responsive**: Works on all screen sizes
- **Intuitive**: Clean, easy-to-use interface
- **Visual Feedback**: Clear result display
- **Copy Function**: One-click result copying

## 🔒 Privacy & Security

- **Offline Operation**: No data sent to servers
- **Local Storage**: All settings stored locally
- **No Tracking**: No analytics or tracking
- **Open Source**: Full code transparency

## 🐛 Troubleshooting

### Windows
- **Security Warning**: Normal for unsigned executables
- **Antivirus**: May flag as false positive
- **Solution**: Add to antivirus exceptions

### Mac
- **Gatekeeper**: Right-click → Open for first run
- **Permissions**: May need to allow in Security settings
- **M1/M2**: Native Apple Silicon support

### Linux
- **Dependencies**: Install python3-tk package
- **Display**: Requires X11 or Wayland
- **Permissions**: Make sure Python has GUI access

## 📝 License

This project is open source. Feel free to use, modify, and distribute.

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Make your changes
4. Test thoroughly
5. Submit pull request

## 📞 Support

- **Issues**: Use GitHub Issues for bug reports
- **Features**: Request new features via Issues
- **Community**: Join our trading community

## 🏷️ Version History

See [Releases](../../releases) for detailed changelog and download links.

---

**Created with ❤️ by WUNDAGUAD**

*Professional trading tools for the community*
