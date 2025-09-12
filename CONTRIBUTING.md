# Contributing to NVC - Nominalwert Calculator

Thank you for your interest in contributing to NVC! This document provides guidelines for contributing to the project.

## 🚀 Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/yourusername/NVC.git`
3. Create a feature branch: `git checkout -b feature/amazing-feature`
4. Make your changes
5. Test thoroughly
6. Commit your changes: `git commit -m 'Add amazing feature'`
7. Push to your branch: `git push origin feature/amazing-feature`
8. Open a Pull Request

## 🛠️ Development Setup

### Prerequisites
- Python 3.8 or higher
- pip package manager
- Git

### Local Development
```bash
# Clone the repository
git clone https://github.com/wundaguad/NVC.git
cd NVC

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python nominalwert_rechner.py
```

## 📝 Code Style

- Follow PEP 8 Python style guidelines
- Use meaningful variable and function names
- Add comments for complex logic
- Keep functions focused and small
- Use type hints where appropriate

## 🧪 Testing

Before submitting a PR:

1. Test the application manually
2. Verify all calculations are correct
3. Test on different screen resolutions
4. Check both German and English interfaces
5. Ensure settings persistence works

## 🐛 Bug Reports

When reporting bugs, please include:

- Operating system and version
- Python version (if running from source)
- Steps to reproduce the issue
- Expected vs actual behavior
- Screenshots if applicable

## 💡 Feature Requests

For new features:

- Describe the feature clearly
- Explain the use case and benefits
- Consider backward compatibility
- Discuss implementation approach

## 📦 Building Releases

### Windows
```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name "NominalwertRechner" --icon="logo.png" --add-data "logo.png;." nominalwert_rechner.py
```

### Mac
```bash
chmod +x build_mac_github.sh
./build_mac_github.sh
```

## 🔄 Pull Request Process

1. Ensure your code follows the style guidelines
2. Update documentation if needed
3. Add yourself to contributors if it's your first contribution
4. Ensure the PR description clearly describes changes
5. Link any related issues

## 📋 Commit Message Format

Use clear, descriptive commit messages:

```
feat: add new leverage calculation method
fix: resolve stop-loss percentage validation
docs: update installation instructions
style: improve code formatting
refactor: simplify fee calculation logic
```

## 🌐 Internationalization

When adding new text:

1. Add entries to both German and English translations
2. Use the `get_text()` function for all user-facing strings
3. Test in both languages
4. Consider text length differences between languages

## 🏗️ Architecture

The application follows this structure:

- `nominalwert_rechner.py` - Main application file
- `positionsrechner_pro_settings.py` - Settings management
- `NominalwertRechner_Exact.html` - Web version
- `build_*.sh/bat` - Build scripts
- `requirements.txt` - Python dependencies

## 📞 Questions?

- Open an issue for questions
- Join our community discussions
- Contact the maintainers

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

**Thank you for contributing to NVC!** 🎉
