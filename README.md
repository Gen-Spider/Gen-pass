<div align="center">

<!-- Brand header with animated typing -->
<img src="https://readme-typing-svg.herokuapp.com?font=Orbitron&size=44&duration=3200&pause=700&color=22FF88&center=true&vCenter=true&width=900&height=80&lines=🕷%20GIT%20SPIDER%20SECURITY;GEN%E2%80%91PASS%20ENTERPRISE%20CLI;FAST%20%E2%80%A2%20SECURE%20%E2%80%A2%20ELEGANT" alt="Git Spider Animated Title"/>

<!-- Soft gradient brand banner -->
<p>
  <img src="https://img.shields.io/badge/Brand-Git%20Spider-22ff88?style=for-the-badge&logo=github&logoColor=0b0b0b&labelColor=0b0b0b"/>
  <img src="https://img.shields.io/badge/App-Gen%E2%80%91Pass-0ad17a?style=for-the-badge&logo=python&logoColor=0b0b0b&labelColor=0b0b0b"/>
  <img src="https://img.shields.io/badge/UI-Rich%20Terminal-14cba8?style=for-the-badge&logo=markdown&logoColor=0b0b0b&labelColor=0b0b0b"/>
</p>

<!-- Floating brand card (static compatible) -->
<div style="max-width:900px;padding:18px;border-radius:14px;background:linear-gradient(135deg,#0b0b0b,#0f1f16);box-shadow:0 10px 30px rgba(34,255,136,.08), inset 0 0 0 1px rgba(34,255,136,.18);">
  <h2 style="color:#22ff88;margin:0;">Gen‑Pass • Password & Passphrase CLI</h2>
  <p style="color:#cfeadb;margin:6px 0 0;">A polished, animated terminal experience for secure generation, analysis, and batch workflows — branded by Git Spider.</p>
</div>

</div>

---

## ✨ Visual overview

<div align="center">

<!-- Feature tiles -->
<img src="https://img.shields.io/badge/Generate-Passwords-1f2a24?style=flat&logoColor=22ff88&labelColor=0b0b0b&color=1f2a24"> 
<img src="https://img.shields.io/badge/Generate-Passphrases-1f2a24?style=flat&logoColor=22ff88&labelColor=0b0b0b&color=1f2a24"> 
<img src="https://img.shields.io/badge/Analyze-Strength-1f2a24?style=flat&logoColor=22ff88&labelColor=0b0b0b&color=1f2a24"> 
<img src="https://img.shields.io/badge/Batch-Workflows-1f2a24?style=flat&logoColor=22ff88&labelColor=0b0b0b&color=1f2a24"> 
<img src="https://img.shields.io/badge/Matrix-Animation-1f2a24?style=flat&logoColor=22ff88&labelColor=0b0b0b&color=1f2a24"> 
<img src="https://img.shields.io/badge/Rich-UI-1f2a24?style=flat&logoColor=22ff88&labelColor=0b0b0b&color=1f2a24">

</div>

> Smooth gradients, neon‑green accents, and a subtle Matrix vibe give Gen‑Pass a modern brand feel that’s unmistakably Git Spider.

---

## 🚀 Quick start (venv)

```bash
# Clone & enter
git clone https://github.com/Gen-Spider/Gen-pass.git
cd Gen-pass

# Create a dedicated virtual environment
python -m venv .venv
# Activate
#  - Windows: .venv\Scripts\activate
#  - macOS/Linux: source .venv/bin/activate

# Install UI deps (rich auto-installs on first run if missing)
pip install -r requirements.txt

# Launch the animated CLI
python main.py
```

---

## 🎛️ What you’ll see

- Brand banner with neon Git Spider identity and soft glow accents.
- Smooth loading spinner and Matrix‑style glyph rain effect.
- Elegant menus, tables, and progress bars powered by Rich.
- Live, color‑coded feedback for strength, entropy, and crack‑time.

> The UI favors calm motion and readable contrast — animations enhance, not distract.

---

## 🧩 Core commands

```bash
# 1) Interactive experience
python main.py

# 2) Generate passwords (max polish, max strength)
python main.py generate --length 16 --count 5 --complexity maximum

# 3) Generate passphrases with symbols
python main.py passphrase --words 6 --count 3 --add-symbols --separator -

# 4) Analyze (hidden prompt if you omit the arg)
python main.py analyze "MyS3cureP@ss!"
```

---

## 🌈 Brand visuals in terminal

Gen‑Pass uses a neon green palette on a deep charcoal background to echo Git Spider’s identity. In the terminal this appears as:

- Soft **Matrix‑like** rain for transitions
- **Neon headers** and accents for hierarchy
- **Glass‑card panels** and **rounded tables** via Rich
- **Subtle progress** animations that feel smooth, not busy

> Everything lives in `main.py`, so the visual identity travels with the app.

---

## 🐳 Docker (with visuals)

```bash
# Create a tiny image with fonts & colors tuned for pretty output
cat > Dockerfile <<'EOF'
FROM python:3.12-slim
ENV PYTHONUNBUFFERED=1
# Optional: install a nicer monospace and set UTF-8 locale
RUN apt-get update && apt-get install -y --no-install-recommends \
    locales fonts-dejavu-core && rm -rf /var/lib/apt/lists/* && \
    sed -i 's/# en_US.UTF-8/en_US.UTF-8/' /etc/locale.gen && locale-gen
ENV LANG=en_US.UTF-8 LC_ALL=en_US.UTF-8 TERM=xterm-256color
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY main.py ./
CMD ["python", "main.py"]
EOF

# Build & run
docker build -t git-spider/genpass:visual .
docker run --rm -it git-spider/genpass:visual
```

> TIP: Use a terminal that supports 24‑bit color to enjoy the full palette.

---

## 🧠 Under the hood (visual + logic)

- `secrets` drives cryptographically secure generation with curated character sets.
- Entropy is computed as \( H = n\,\log_2 |\mathcal{C}| \), rendered with color for clarity.
- Strength levels map to color ramps (red → yellow → green) for instant readability.
- Progress bars and spinners use easing‑like timing for a smoother feel.
- Matrix effect paints ephemeral glyphs without blocking the flow.

---

## 🎨 Brand kit (README visuals)

- Animated typing header for identity cues
- Dark card with neon border for hero section
- Flat tiles to summarize capabilities
- Minimal text + strong hierarchy for skimmability

If you want even more brand energy, consider adding a centered SVG logo (neon spider) and a lightweight GIF preview of the terminal in action.
