# 🔐 Gen‑Pass: Dynamic Password & Passphrase CLI

Gen‑Pass is a fast, secure, animated CLI for generating strong passwords and memorable passphrases, analyzing their strength, and exporting results — all from a single, self‑contained main.py. This README focuses on how to run it, what it does, and how it works under the hood, with practical Docker and venv examples.

---

## Quick start

```bash
# 1) Clone and enter
git clone https://github.com/Gen-Spider/Gen-pass.git
cd Gen-pass

# 2) (Recommended) Create a virtual environment
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# 3) Install essentials (auto-installs on first run if missing)
pip install -r requirements.txt

# 4) Launch the interactive CLI
python main.py
```

Tips:
- Minimal install works too: `pip install rich colorama` then `python main.py`.
- Exit anytime with Ctrl+C.

---

## What you can do

- Generate strong passwords with 5 complexity levels (minimum → military).
- Generate memorable passphrases with custom separators, numbers, and symbols.
- Analyze any string’s entropy, composition, vulnerabilities, and crack‑time estimates.
- Batch‑generate hundreds of passwords or passphrases with progress bars, then save to a file.
- Create cryptographic hashes (MD5, SHA1, SHA256, SHA512) for quick integrity needs.
- Enjoy a rich, animated terminal experience with banners, progress, and matrix effects.

---

## Common commands

Interactive mode (default):
```bash
python main.py
```

Command style usage:
```bash
# Generate 5 strong passwords of length 16
python main.py generate --length 16 --count 5 --complexity maximum

# Generate 3 passphrases of 6 words with symbols
python main.py passphrase --words 6 --count 3 --add-symbols --separator -

# Analyze a password (hidden prompt if omitted)
python main.py analyze "MyS3cureP@ss!"

# Batch mode (interactive menu has a guided flow)
python main.py interactive
```

---

## Inside the interactive menu

- Generate Password: choose length, complexity, character exclusions; get instant strength/entropy.
- Generate Passphrase: set words, separators, capitalization, numbers/symbols; see quality metrics.
- Analyze Password: hidden input, detailed report (entropy, composition, weaknesses, advice, crack‑time).
- Batch Generation: produce many items with a progress bar and save to a file with a sample preview.
- Hash Generator: quickly compute MD5/SHA1/SHA256/SHA512 for any text you enter.
- Security Audit (lightweight): sample entropy comparisons and pattern checks.
- System Info: environment overview including UI capability.
- Help: concise best practices and usage tips.

---

## How it works (under the hood)

- Cryptographically secure generation: uses Python’s `secrets` for random selection.
- Character sets: lower/upper/digits/symbols; optional exclusion of ambiguous/similar glyphs.
- Entropy calculation: approximates per‑character search space and computes bits via \(\text{entropy} = n \cdot \log_2(|\mathcal{C}|)\).
- Strength scoring: blends length, variety, and entropy to a 0–100 score with named levels.
- Crack‑time estimation: converts entropy to combinations and divides by scenario attempt rates.
- UI/UX: `rich` for panels/tables/progress, `colorama` for cross‑platform coloring.
- Single file: everything lives in `main.py` for easy sharing, while still cleanly structured.

---

## Virtual environment (venv) guide

```bash
# Create a venv in project root
python -m venv .venv

# Activate it
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

# Upgrade tooling and install deps
python -m pip install --upgrade pip
pip install -r requirements.txt

# Run the app
python main.py

# Deactivate when done
deactivate
```

Why venv?
- Keeps dependencies isolated from system Python.
- Lets you pin/upgrade without breaking other projects.
- Plays well with editors and CI.

---

## Docker usage

Run directly from a slim Python image and mount your working directory:

```bash
# Build a tiny throwaway image (optional)
cat > Dockerfile <<'EOF'
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY main.py ./
CMD ["python", "main.py"]
EOF

# Build
docker build -t genpass-cli:latest .

# Run interactively (attach your terminal)
docker run --rm -it genpass-cli:latest
```

Don’t want to build? Use a bind‑mount and run in a stock Python container:
```bash
docker run --rm -it -v "$PWD":/app -w /app python:3.12-slim \
  bash -lc "pip install --no-cache-dir -r requirements.txt && python main.py"
```

---

## Troubleshooting

- Terminal looks plain? Install `rich` and ensure your terminal supports ANSI colors.
- Unicode issues on Windows? Use a modern terminal (Windows Terminal/PowerShell 7+) and `chcp 65001` if needed.
- No internet on first run? Pre‑install with `pip install -r requirements.txt`.
- Module not found? Activate your venv before running.

---

## FAQ (short)

- Is this a password manager? No — it generates and analyzes; it does not store.
- Is generation predictable? Generation uses `secrets`, designed for cryptographic randomness.
- Can it run offline? Yes. All core features are local.
- Where are results saved? When you choose a path, a plain text file is created in that location.
