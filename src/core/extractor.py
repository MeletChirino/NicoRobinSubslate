import pymkv
from typing import List, Tuple

class MKVExtractor:
    def __init__(self, file_path: str):
        # The user must ensure mkvmerge is in their system PATH 
        # or configure mkvmerge_path.
        self.file_path = file_path
        self.mkv_file = pymkv.MKVFile(file_path)

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

if __name__ == "__main__":
    # Example usage:
    # Note: This will fail unless an actual .mkv file exists and mkvmerge is installed.
    try:
        extractor = MKVExtractor("movie_sample.mkv")
        tracks = extractor.get_subtitle_tracks()
        print(f"Found {len(tracks)} subtitle tracks:")
        for track_id, lang in tracks:
            print(f"- ID: {track_id}, Language: {lang}")
    except FileNotFoundError as e:
        print(f"Error: {e}. Please ensure the file exists and mkvmerge is installed.")
    except Exception as e:
        print(f"An error occurred: {e}")
