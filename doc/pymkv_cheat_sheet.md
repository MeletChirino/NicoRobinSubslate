### 📘 REFERENCE DOCUMENTATION FOR AGENT: `pymkv` Core Usage

Use this official syntax and structure of the `pymkv` library to implement the project. Do not hallucinate or use methods outside of this specification.

#### 1. Library Overview

`pymkv` is a Python wrapper around `mkvtoolnix` (`mkvmerge` and `mkvextract`). It models an MKV file as an object containing a list of tracks.

#### 2. Reading and Inspecting an MKV File

To load an MKV file and inspect its contents, use the `MKVFile` class. The `.tracks` attribute is a list containing all video, audio, and subtitle tracks.

Python

```
from pymkv import MKVFile

# Load the file
mkv = MKVFile('movie.mkv')

# Inspect tracks
for track in mkv.tracks:
    # Key properties available in every track object:
    track_id = track.track_id      # Integer (0, 1, 2...) representing the track ID
    track_type = track.track_type  # String: 'video', 'audio', or 'subtitles'
    language = track.language      # String (ISO 639-2): 'eng', 'fre', 'spa', etc.
    name = track.track_name        # String or None (e.g., 'SDH', 'Commentary')
    
    print(f"Track {track_id}: Type={track_type}, Lang={language}")
```

#### 3. Extracting Subtitles (Demuxing)

`pymkv` handles verification, but the actual extraction of a specific track to an external file (like `.srt`) requires invoking `mkvextract` via `subprocess`, mapping the correct `track_id` found during inspection:

Python

```
import subprocess

def extract_subtitle(mkv_path, track_id, output_srt_path):
    # Syntax: mkvextract tracks <source-file> <track_id>:<output-file>
    cmd = ["mkvextract", "tracks", mkv_path, f"{track_id}:{output_srt_path}"]
    subprocess.run(cmd, check=True)
```

#### 4. Creating and Muxing a New MKV File

To wrap an existing video and inject a newly translated subtitle file, use `MKVTrack` and add it to the `MKVFile` object before calling `.mux()`.

Python

```
from pymkv import MKVFile, MKVTrack

# 1. Load the original MKV (keeps all original audio/video/subs)
mkv = MKVFile('original.mkv')

# 2. Instantiate the new subtitle track
# Parameters: track_path (str), language (str, 3 letters), title (str, optional)
new_track = MKVTrack('translated_spanish.srt', language='spa', title='Español (Gemma AI)')

# 3. Append the track to the MKV object
mkv.add_track(new_track)

# 4. Compile the final container to disk
mkv.mux('output_final.mkv')
```

