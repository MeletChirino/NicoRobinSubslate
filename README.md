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
├── tests/                # Unit and integration tests
└── requirements.txt      # Dependencies
```

## Features

## Installation
```bash
pip install ollama pymkv
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
