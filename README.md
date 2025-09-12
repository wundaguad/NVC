# 🧮 NVC - Nominalwert Calculator

**Professional Trading Position Calculator with Leverage Support**

Created with ❤️ by **WUNDAGUAD** for our community

[![GitHub release](https://img.shields.io/github/release/wundaguad/NVC.svg)](https://github.com/wundaguad/NVC/releases)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Mac%20%7C%20Linux-lightgrey.svg)](https://github.com/wundaguad/NVC/releases)

## 🚀 Features

- **Multi-Platform Support**: Windows, Mac, Linux
- **Leverage Trading**: 1x to 125x leverage calculation
- **Risk Management**: Precise stop-loss and take-profit calculations
- **Multi-Language**: German and English interface
- **Dark Theme**: Professional trading interface
- **Fee Calculation**: Maker/Taker fees included
- **Copy to Clipboard**: Easy result sharing
- **Offline Ready**: No internet connection required

## 📥 Quick Download

| Platform | Download | Size |
|----------|----------|------|
| 🪟 **Windows** | [NominalwertRechner.exe](../../releases/latest/download/NominalwertRechner.exe) | ~15MB |
| 🍎 **Mac** | [NominalwertRechner-Mac.dmg](../../releases/latest/download/NominalwertRechner-Mac.dmg) | ~20MB |
| 🐧 **Linux** | [Source Code](../../archive/refs/heads/main.zip) | Run with Python |

## 🛠️ Installation

### Windows
1. Download `NominalwertRechner.exe` from [Releases](../../releases)
2. **Security Warning**: Windows may show "Windows protected your PC"
   - Click **"More info"** → **"Run anyway"**
   - Or: Right-click .exe → Properties → **"Unblock"** → OK
3. Run the executable - no installation needed

### Mac
1. Download `NominalwertRechner-Mac.dmg` from [Releases](../../releases)
2. Open DMG and drag app to Applications folder
3. **Security Warning**: macOS may show "unidentified developer" warning
   - **Right-click** app → **"Open"** → **"Open"** (bypass Gatekeeper)
   - Or: System Preferences → Security & Privacy → **"Open Anyway"**

### Alternative: Web Version
For users who prefer browser-based tools, a web version is also available in the releases.

### Linux / Source Code
```bash
# Clone repository
git clone https://github.com/wundaguad/NVC.git
cd NVC

# Install dependencies
pip install -r requirements.txt

# Run application
python nominalwert_rechner.py
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

## 📊 Calculation Logic

Professional trading formulas:

```
Margin Required = Max Loss / Effective Percentage
Nominal Value = Margin Required × Leverage
Effective Percentage = (Stop-Loss % + Fees) / 100
```

**Example**: 10€ max loss, 0.51% SL, 25x leverage
- Margin required: ~19.61€ 
- Nominal value: ~490€ (25x larger position)
- Actual risk: exactly 10€ at stop-loss

## 🔧 Advanced Features

### Trading Fees
- Configurable maker/taker fees
- Automatic fee calculation in P&L
- Support for different exchange structures

### Take-Profit Configuration
- Multiple TP levels (25%, 50%, 75%, 100%)
- Automatic profit calculation
- Risk-reward ratio display

### Settings
- Language selection (German/English)
- Number format (German/US)
- Persistent settings storage

## 🌐 Multi-Language Support

- **Deutsch**: Complete German interface
- **English**: Full English translation
- **Dynamic**: Switch without restart (web version)
- **Persistent**: Language preference saved

## 🛡️ Security & Privacy

- **Offline Operation**: No data sent to servers
- **Local Storage**: All settings stored locally
- **No Tracking**: No analytics or data collection
- **Open Source**: Full code transparency

## 🐛 Troubleshooting

### Windows Issues
- **"Windows protected your PC"**: Click "More info" → "Run anyway"
- **Antivirus blocking**: Add to antivirus exceptions if needed
- **File blocked**: Right-click .exe → Properties → "Unblock" → OK

### Mac Issues
- **"Cannot be opened because it is from an unidentified developer"**: Right-click app → "Open" → "Open"
- **"App is damaged"**: Run `xattr -cr /Applications/NominalwertRechner.app` in Terminal
- **Gatekeeper blocking**: System Preferences → Security & Privacy → "Open Anyway"
- **M1/M2**: Native Apple Silicon support included

### Linux Issues
- **Dependencies**: `sudo apt install python3-tk`
- **Display**: Requires X11 or Wayland

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🏷️ Changelog

See [Releases](../../releases) for detailed version history and downloads.

## 📞 Support

- 🐛 **Bug Reports**: [GitHub Issues](../../issues)
- 💡 **Feature Requests**: [GitHub Issues](../../issues)
- 💬 **Community**: [Discussions](../../discussions)

---

**Created with ❤️ by WUNDAGUAD**

*Professional trading tools for the community*

![WUNDAGUAD](https://img.shields.io/badge/WUNDAGUAD-Trading%20Tools-yellow?style=for-the-badge)
