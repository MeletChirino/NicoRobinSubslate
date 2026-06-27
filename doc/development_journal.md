# Development Journal: MKV Subtitle Translator

## Project Overview
An AI-powered CLI tool designed to automate the translation of subtitles within `.mkv` containers using local LLM inference (Ollama with `tranlategemma`).

## Setup and Environment
- **Virtual Environment:** Established a Python virtual environment in `.venv`.
- **Dependencies:** 
  - `ollama`: For model interaction.
  - `pymkv`: A wrapper around `mkvtoolnix` for handling MKV contents.
- **System Requirements:** Identified need for `ffmpeg` and `mkvtoolnix` (for `mkvmerge`) on macOS/Linux/Windows.
- **Automation:** Created `setup.sh` to automate the installation of system dependencies and virtual environment setup.

## Project Structure & Modules
- `src/core/extractor.py`: Handles initial processing of MKV files.
  - Features: Track identification, language checking, and filtering (e.g., identifying English or French tracks).
- `doc/`: Repository for documentation and cheat sheets.
- `tests/`: Area reserved for unit and integration testing.

## Key Milestones Completed
1. **Project Initialization:** Established directory structure (`src`, `core`, `utils`, `doc`).
2. **Documentation:** Initialized `README.md` with installation, prerequisites (Ollama/FFmpeg), and basic usage instructions.
3. **Dependency Management:** Created `requirements.txt` and successfully installed packages within a managed `.venv`.
4. **Subtitles Extraction Core:** Implemented `MKVExtractor` using `pymkv`. Features include track identification and intelligent language detection (using `langdetect` as a fallback for unknown tracks). Verified it correctly identifies and filters multiple subtitle tracks.
5. **Language Normalization:** Added logic to map common 2-letter codes (e.g., 'en', 'fr') to standard ISO 639-2 codes ('eng', 'fra').

## Knowledge Base Reference
- Registered a `doc/` folder specifically for repository documentation, including a cheat sheet for the `pymkv` library to ensure consistent API usage across modules.
