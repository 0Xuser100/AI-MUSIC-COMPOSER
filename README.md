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

## Project Layout
- `main.py` – entrypoint placeholder
- `pyproject.toml` – project metadata and dependencies
- `.env.example` – expected environment variables
- `uv.lock` – lockfile for `uv`

## License
GPL-3.0 (see `LICENSE`).
