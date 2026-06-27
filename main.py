from src.core.extractor import MKVExtractor
from src.core.translator import Translator

# Configuration
input_file = "movie_sample.mkv"
anime_title = "My Hero Academia"

def main():
    # 1. Initialize Extractor and find target subtitle tracks
    extractor = MKVExtractor(input_file)
    target_tracks = extractor.find_target_tracks_with_detection(target_languages=["eng"])

    if not target_tracks:
        print("No English tracks found.")
        return

    # Get the first English track ID found
    track_id = list(target_tracks.values())[0]
    print(f"Found English track at ID: {track_id}")

    # 2. Extract the raw subtitle content
    raw_content = extractor.extract_subtitle(track_id)
    if not raw_content:
        print("Failed to extract content.")
        return

    # 3. Initialize Translator and perform translation
    translator = Translator()
    print(f"Translating {len(raw_content.splitlines())} lines...")
    
    translated_content = translator.translate_subtitle_track(
        content=raw_content, 
        title=anime_title
    )

    # 4. Display or save the result
    print("Translation complete:")
    print(translated_content)

if __name__ == "__main__":
    main()
