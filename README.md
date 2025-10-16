# 🔐 Gen-Pass

**A Professional Password Generator for Enhanced Security**

[![Python](https://img.shields.io/badge/Python-3.7%2B-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Security](https://img.shields.io/badge/Security-Enterprise%20Grade-red.svg)]()

---

## 🚀 Overview

Gen-Pass is a comprehensive, security-focused password generator designed for developers, security professionals, and anyone who values strong authentication. Built with Python's `secrets` module for cryptographically secure randomness, it offers both traditional passwords and memorable passphrases.

### ✨ Key Features

- **🔒 Cryptographically Secure**: Uses Python's `secrets` module for true randomness
- **🎛️ Highly Customizable**: Control length, character sets, and complexity
- **📝 Passphrase Generation**: Create memorable yet secure passphrases
- **💪 Strength Analysis**: Built-in password strength checker with detailed feedback
- **⚡ CLI Interface**: Easy-to-use command-line interface
- **📊 Batch Generation**: Generate multiple passwords at once
- **💾 Export Options**: Save generated passwords to files
- **🚫 Ambiguity Prevention**: Option to exclude confusing characters

---

## 📦 Installation

### Prerequisites
- Python 3.7 or higher
- No external dependencies required (uses standard library only)

### Quick Start

```bash
# Clone the repository
git clone https://github.com/Gen-Spider/Gen-pass.git
cd Gen-pass

# Make the script executable (Linux/macOS)
chmod +x main.py

# Run the generator
python main.py
```

---

## 🛠️ Usage

### Basic Password Generation

```bash
# Generate a default 12-character password
python main.py

# Generate a 16-character password
python main.py --length 16

# Generate 5 passwords at once
python main.py --count 5
```

### Advanced Options

```bash
# Generate without symbols
python main.py --no-symbols

# Generate without ambiguous characters (0, O, 1, l, I)
python main.py --exclude-ambiguous

# Generate a passphrase instead
python main.py --passphrase --words 5

# Custom passphrase with different separator
python main.py --passphrase --separator "_" --words 3
```

### Password Analysis

```bash
# Check the strength of an existing password
python main.py --check "YourPassword123!"
```

### Save to File

```bash
# Generate and save passwords to a file
python main.py --count 10 --save passwords.txt
```

---

## 📋 Command Line Options

| Option | Description | Default |
|--------|-------------|---------|
| `-l, --length` | Password length | 12 |
| `-c, --count` | Number of passwords to generate | 1 |
| `--no-uppercase` | Exclude uppercase letters | False |
| `--no-lowercase` | Exclude lowercase letters | False |
| `--no-digits` | Exclude digits | False |
| `--no-symbols` | Exclude symbols | False |
| `--exclude-ambiguous` | Exclude ambiguous characters | False |
| `--passphrase` | Generate passphrase instead | False |
| `--words` | Number of words in passphrase | 4 |
| `--separator` | Passphrase word separator | - |
| `--check` | Check strength of provided password | None |
| `--save` | Save passwords to file | None |

---

## 🔧 Programming Interface

### Using Gen-Pass in Your Code

```python
from main import PasswordGenerator

# Create generator instance
generator = PasswordGenerator()

# Generate a custom password
password = generator.generate_password(
    length=16,
    use_uppercase=True,
    use_lowercase=True,
    use_digits=True,
    use_symbols=True,
    exclude_ambiguous=True
)

# Generate a passphrase
passphrase = generator.generate_passphrase(
    word_count=4,
    separator="-",
    capitalize=True,
    add_numbers=True
)

# Check password strength
analysis = generator.check_strength("MyPassword123!")
print(f"Strength: {analysis['strength']}")
print(f"Score: {analysis['score']}/100")
```

---

## 🛡️ Security Features

### Cryptographic Security
- Uses `secrets.SystemRandom()` for cryptographically secure random generation
- No predictable patterns in generated passwords
- Secure shuffling of password components

### Character Set Options
- **Lowercase**: a-z (26 characters)
- **Uppercase**: A-Z (26 characters)  
- **Digits**: 0-9 (10 characters)
- **Symbols**: !@#$%^&*()_+-=[]{}|;:,.<>? (23 characters)
- **Ambiguous Exclusion**: Optionally excludes 0, O, 1, l, I

### Password Strength Analysis
The built-in strength checker evaluates:
- Length adequacy
- Character variety
- Common password detection
- Provides actionable feedback

---

## 📖 Examples

### Example Outputs

**Standard Password:**
```
$ python main.py --length 16
Password 1: K#9mP2$vX@4nL8qZ
```

**Passphrase:**
```
$ python main.py --passphrase --words 4
Passphrase 1: Magic-Thunder-Ocean-Dream-47
```

**Strength Analysis:**
```
$ python main.py --check "MyPassword123!"

Password Strength Analysis:
Password: MyPassword123!
Strength: Strong
Score: 75/100
Length: 13
Character Types:
  - Lowercase: ✓
  - Uppercase: ✓
  - Digits: ✓
  - Symbols: ✓
```

### Batch Generation
```bash
$ python main.py --count 3 --length 14
Password 1: 8mK@2vP#5nX9qL
Password 2: R7$jD4&zM1@sF6
Password 3: Q3!wE8*tY5#uI0
```

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

### Development Setup

```bash
git clone https://github.com/Gen-Spider/Gen-pass.git
cd Gen-pass
python -m pytest tests/  # Run tests (when available)
```

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🔗 Links

- **Repository**: [Gen-Spider/Gen-pass](https://github.com/Gen-Spider/Gen-pass)
- **Issues**: [Report a Bug](https://github.com/Gen-Spider/Gen-pass/issues)
- **Security**: For security concerns, please email the maintainer

---

## ⚡ Quick Reference

```bash
# Most common use cases
python main.py                          # Basic 12-char password
python main.py -l 20 -c 5              # 5 passwords, 20 chars each
python main.py --passphrase             # Memorable passphrase
python main.py --check "password"       # Check password strength
python main.py --exclude-ambiguous      # No confusing characters
```

---

**Made with ❤️ by Gen-Spider** | **Stay Secure!** 🔐