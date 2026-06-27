import pymkv
from typing import List, Tuple, Dict
from langdetect import detect

class MKVExtractor:
    def __init__(self, file_path: str):
        # The user must ensure mkvmerge is in their system PATH
        # or configure mkvmerge_path.
        self.file_path = file_path
        self.mkv_file = pymkv.MKVFile(file_path)

    def extract_subtitle(self, track_id: int) -> str:
        """
        Extracts the subtitle text for a specific track ID.
        """
        import subprocess
        import os
        import tempfile

        # Use a temporary file to capture output from mkvextract
        with tempfile.NamedTemporaryFile(suffix=".srt", delete=False) as tmp:
            tmp_path = tmp.name

        try:
            # Construction of the command
            cmd = ["mkvextract", "tracks", self.file_path, f"{track_id}:{tmp_path}"]

            # Run the command and capture output/errors
            result = subprocess.run(cmd, check=True, capture_output=True, text=True)

            with open(tmp_path, 'r', encoding='utf-8') as f:
                content = f.read()
            return content
        except subprocess.CalledProcessError as e:
            # Print the actual error from the tool to help debug
            print(f"mkvextract error: {e.stderr}")
            return ""
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

    def save_track(self, track_id: int, content: str):
        """
        Saves the provided subtitle content to a file named after the track_id.
        """
        output_path = f"extracted_track_{track_id}.srt"
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Saved content to {output_path}")
            return output_path
        except Exception as e:
            print(f"Failed to save file: {e}")
            return None

    def get_subtitle_tracks(self) -> List[Tuple[int, str]]:
        """
        Returns a list of (track_id, language) for all subtitle tracks.
        """
        subtitle_tracks = []
        for track in self.mkv_file.tracks:
            if track.track_type == "subtitles":
                # Track ID and Language (defaulting to 'Unknown' if not set)
                language = track.language if track.language else "Unknown"
                subtitle_tracks.append((track.track_id, language))
        return subtitle_tracks

    def _normalize_language(self, lang_code: str) -> str:
        """
        Normalizes common 2-letter (ISO 639-1) codes to standard 3-letter (ISO 639-2) codes.
        """
        mapping = {
            "en": "eng",
            "fr": "fra",
            "de": "deu",
            "es": "spa",
            "it": "ita",
            "pt": "por",
            "ja": "jpn",
            "ru": "rus",
            "zh": "zho",
        }
        if lang_code.lower() in mapping:
            return mapping[lang_code.lower()]
        return lang_code

    def find_target_tracks_with_detection(self, target_languages=["eng", "fra"]) -> Dict[str, int]:
        """
        Finds and detects subtitle tracks with fallback to langdetect.
        """
        all_subs = self.get_subtitle_tracks()
        if not all_subs:
            print("Error: No subtitle tracks detected.")
            return {}

        print(f"Detected {len(all_subs)} subtitle tracks.")
        detected_tracks = {}

        for track_id, language in all_subs:
            # If the metadata already identifies it as one of our targets, add it.
            if language.lower() in target_languages:
                detected_tracks[language] = track_id
            else:
                # Otherwise, try to detect using langdetect on the first 40 lines.
                content = self.extract_subtitle(track_id)
                lines = [line for line in content.splitlines() if line.strip()][:40]
                if lines:
                    try:
                        raw_lang = detect(" ".join(lines))
                        normalized_lang = self._normalize_language(raw_lang)
                        # Assign even if it's not a target language, to ensure
                        # we see what was found during testing.
                        detected_tracks[normalized_lang] = track_id
                    except Exception as e:
                        print(f"Detection error: {e}")

        return detected_tracks


if __name__ == "__main__":
    try:
        extractor = MKVExtractor("movie_sample.mkv")
        all_tracks = []
        for track in extractor.mkv_file.tracks:
            print(f"Track ID: {track.track_id}, Type: {track.track_type}, Language: {track.language}")
            all_tracks.append(track)

        tracks = extractor.find_target_tracks_with_detection()
        print(f"Found {len(tracks)} target subtitle tracks:")
        for lang, track_id in tracks.items():
            print(f"- {lang}: {track_id}")
        print(F"{extractor.extract_subtitle(tracks['eng'])}")
    except FileNotFoundError as e:
        print(f"Error: {e}. Please ensure the file exists and mkvmerge is installed.")
    except Exception as e:
        print(f"An error occurred: {e}")
        import traceback
        traceback.print_exc()
