import subprocess
import json
import os
DEBUG = True
def get_mkv_metadata(input_file):
    """
    Uses ffprobe to get all stream information in JSON format.
    """
    command = [
        'ffprobe',
        '-v', 'quiet',
        '-print_format', 'json',
        '-show_streams',
        input_file
    ]
    result = subprocess.run(command, capture_output=True, text=True)
    if DEBUG: print(f"{result}")
    return json.loads(result.stdout)

def extract_english_subtitles(input_file, output_srt):
    """
    Locates the English subtitle track and extracts it.
    """
    metadata = get_mkv_metadata(input_file)
    streams = metadata.get('streams', [])

    target_track_index = None

    # Iterate through streams to find subtitles (codec_type == 'subtitle')
    # and language metadata ('eng')
    for stream in streams:
        if stream.get('codec_type') == 'subtitle':
            tags = stream.get('tags', {})
            language = tags.get('language', '').lower()

            if language == 'eng' or language == 'english':
                # We need the index relative to all subtitle streams for ffmpeg mapping
                # or the global index. Using global index 'index' is safest with -map 0:v / 0:a / 0:s
                target_track_index = stream.get('index')
                print(f"Found English subtitle at global index: {target_track_index}")
                break

    if target_track_index is None:
        print(f"No English subtitles found in {input_file}. Defaulting to first subtitle track.")
        target_track_index = "s:0" # Fallback to first subtitle track
    else:
        # Format for ffmpeg mapping
        target_track_index = f"0:{target_track_index}"

    # Execution of the extraction
    extraction_command = [
        'ffmpeg',
        '-i', input_file,
        '-map', str(target_track_index),
        '-y',
        output_srt
    ]

    try:
        subprocess.run(extraction_command, check=True, capture_output=True)
        print(f"Successfully extracted to: {output_srt}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error during extraction: {e}")
        return False

# Example Usage
video_source = "movie_sample.mkv"
subtitle_destination = "extracted_english.srt"
if DEBUG: print(f"Trying to extract {video_source} from {subtitle_destination}")

result = get_mkv_metadata(video_source)
# if os.path.exists(video_source):
#     extract_english_subtitles(video_source, subtitle_destination)
