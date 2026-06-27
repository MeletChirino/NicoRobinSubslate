# Development Context & Quick Start

This project is an AI-powered local tool for translating `.mkv` subtitles using Ollama.

## Features
- Extracts subtitle tracks from MKV containers.
- Seamless translation using local LLM inference.
- Re-inserts translated subtitles into the original file format.

## Core Commands
- **Setup:** `bash setup.sh` (installs system dependencies, sets up venv, and installs Python requirements).
- **Verify Installation:** Ensure `mkvtoolnix`, `ffmpeg`, and `ollama` are installed correctly via the `setup.sh` script instructions.
- **Model Pull:** `ollama pull tranlategemma` is required for translation.
- All packages are installed into virtual environment located on `.venv` folder.

## Project Architecture
- **Entry Point:** `main.py` (via `translate_mkv` function).
- **Core Logic:** Located in `src/core/`:
   - **Extractor (`extractor.py`):** Handles MKV container manipulation using `mkvextract` and `pymkv`. Supports intelligent language detection with a fallback to `langdetect` when metadata is missing or ambiguous.

  - **Translator (Planned/Partial):** Handles LLM interaction for translation logic.
  - **Inserter (Planned/Partial):** Handles re-inserting translated tracks into MKV files.

## Important Context & Gotchas
- **Environment:** The project uses a virtual environment (`.venv`) and requires `ffmpeg` for media processing.
- **External Tools:** Heavily relies on `mkvmerge` (from `mkvtoolnix`). Ensure the binary is accessible to the Python script.
- **LLM Integration:** Configured to use the `gemma4:12b-mlx` model via Ollama with a custom base URL (`http://192.168.1.57:11434/v1`). See `opencode.json` for provider details.
- **Language Codes:** The extractor identifies tracks using ISO 639-2 codes (e.g., 'eng', 'fra').
- **Sample Files:** Use `movie_sample.mkv` and its corresponding test outputs/debug files for local verification.

## Project Structure
```text
.
├── src/
│   ├── core/            # Core logic (extraction, translation, insertion)
│   │   ├── extractor.py
│   │   ├── translator.py
│   │   └── inserter.py
│   └── utils/           # Helper functions
│       └── helpers.py
│   └── main.py          # Entry point
├── doc/                  # Documentation (cheat sheets, guides)
├── tests/                # Unit and integration tests
└── requirements.txt      # Dependencies
```

