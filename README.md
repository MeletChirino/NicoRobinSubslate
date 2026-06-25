# MKV Subtitle Translator

An AI-powered CLI tool to translate subtitles in `.mkv` files using the **tranlategemma** model via **Ollama**.

## Features
- Extracts subtitle tracks from MKV containers.
- Seamless translation using local LLM inference.
- Re-inserts translated subtitles into the original file format.

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

## Features
- Extracts subtitle tracks from MKV containers.
- Seamless translation using local LLM inference.
- Re-inserts translated subtitles into the original file format.

## Installation
...

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/username/mkv-translator-repo.git
   cd mkv-translator-repo
   ```

2. **Setup Virtual Environment:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows: .\.venv\Scripts\activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Prerequisites:**
   - Ensure [Ollama](https://ollama.ai/) is installed and running.
   - Pull the required model:
     ```bash
     ollama pull tranlategemma
     ```
    - Ensure `ffmpeg` is installed on your system for media handling.
    - Install **MKVToolNix** (for `mkvmerge`):

      **macOS:**
      ```bash
      brew install mkvtoolnix
      ```

      **Linux (Ubuntu/Debian):**
      ```bash
      sudo apt update
      sudo apt install mkvtoolnix
      ```
      
      **Linux (Fedora):**
      ```bash
      sudo dnf install mkvtoolnix
      ```
    
   
## Usage
```python
from main import translate_mkv

translate_mkv(
    input_file="input.mkv",
    output_file="output_en.mkv",
    target_language="English"
)
```
