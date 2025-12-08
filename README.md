# AI Music Composer

Starter scaffold for experimenting with AI-assisted music composition. The repo currently ships a simple Python entrypoint (`main.py`) and a dependency set geared toward building a Groq + LangChain powered composer that can generate symbolic music (via `music21`), render audio (`synthesizer`), and expose a small UI (`streamlit`).

## Requirements
- Python 3.12 (see `.python-version`)
- Optional: [`uv`](https://docs.astral.sh/uv) for reproducible installs (`uv.lock` is checked in)

## Setup
1) Create a virtual environment (e.g., `python -m venv .venv && source .venv/bin/activate`).
2) Install dependencies: `pip install -e .` (or `uv sync` if you use `uv`).
3) Copy `.env.example` to `.env` and fill in `GROQ_API_KEY` for Groq-backed LLM calls.

## Usage
- Run the current entrypoint: `python main.py` (prints a placeholder message). Extend this file with LangChain/Groq calls, MIDI generation with `music21`, and audio synthesis as you build out the composer.
- For Streamlit experiments, add a script and start it with `streamlit run <script>.py`.

## Docker
- Build the image: `docker build -t ai-music-composer .`
- Run with your `.env` (no quotes around the key) and expose Streamlit: `docker run --rm -p 8501:8501 --env-file .env ai-music-composer`
- If you prefer inline env vars: `docker run --rm -p 8501:8501 -e GROQ_API_KEY=sk_... ai-music-composer`

## Project Layout
- `main.py` – entrypoint placeholder
- `pyproject.toml` – project metadata and dependencies
- `.env.example` – expected environment variables
- `uv.lock` – lockfile for `uv`

## MusicLLM Function I/O
Here’s the **input → output** for every function in your `MusicLLM` class (including what type you should expect):

### 1) `__init__(self, temperature=0.7)`

**Input:**

* `temperature` (float, optional) — e.g. `0.7`

**Output:**

* No direct return (`None`)
* Side effect: creates and stores `self.llm` (a `ChatGroq` chat model instance)

---

### 2) `generate_melody(self, user_input)`

**Input:**

* `user_input` (str) — free text description of the melody you want
  مثال: `"happy upbeat pop melody"`

**Output:**

* (str) — **space-separated notes**
  مثال: `"C4 D4 E4 G4 A4"`

---

### 3) `generate_harmony(self, melody)`

**Input:**

* `melody` (str) — the melody notes, space-separated
  مثال: `"C4 D4 E4 G4 A4"`

**Output:**

* (str) — **chords** where each chord is notes separated by `-`, and chords separated by spaces
  مثال: `"C4-E4-G4 F4-A4-C5 G4-B4-D5"`

---

### 4) `generate_rhythm(self, melody)`

**Input:**

* `melody` (str) — the melody notes, space-separated
  مثال: `"C4 D4 E4 G4 A4"`

**Output:**

* (str) — **durations in beats**, space-separated numbers
  مثال: `"1.0 0.5 0.5 1.0 2.0"`

---

### 5) `adapt_style(self, style, melody, harmony, rhythm)`

**Input:**

* `style` (str) — style name
  مثال: `"jazz"`
* `melody` (str) — space-separated notes
* `harmony` (str) — chord string (notes with `-`, chords with spaces)
* `rhythm` (str) — space-separated beat durations

**Output:**

* (str) — a **single-string summary** that “adapts” or describes the given melody/harmony/rhythm in the target style
  مثال: `"Jazz swing feel melody (C4 D4 ...) with extended ii-V-I harmony ..."`

If you want, I can also show you a tiny “validation” function for each output format (notes/chords/durations) so you can detect when the LLM returns something off-format.

# 🔧 **Development Tooling**

## 🔍 Linters

### **Ruff**

Install:

```bash
uv add ruff
```

Lint:

```bash
uv run ruff check
```

Auto-fix:

```bash
uv run ruff check --fix
```

### **Autoflake** (optional if using Ruff)

```bash
uv add autoflake
uv run autoflake --in-place --recursive --remove-all-unused-imports .
```

---

## 🎨 Formatters

### **Ruff Formatter (recommended)**

```bash
uv run ruff format
```

### **isort (if not using Ruff)**

```bash
uv run isort .
```

### **Black (if not using Ruff)**

```bash
uv run black .
```

---

## 🧠 Type Checker (Mypy)

Install:

```bash
uv add mypy
```

Run:

```bash
uv run mypy .
```

## License
GPL-3.0 (see `LICENSE`).
