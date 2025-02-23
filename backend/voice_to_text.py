import os
import tempfile
import subprocess
import whisper
import gridfs
from bson.objectid import ObjectId
from pymongo import MongoClient
from tqdm import tqdm

# -----------------------------------------------------------------------------
# 1) CONNECT TO MONGODB
# -----------------------------------------------------------------------------
def connect_to_db():
    """
    Connects to MongoDB and returns (db, fs).
    Adjust the connection string, db name, and collection name as needed.
    """
    try:
        # Example connecting to local or Atlas
        client = MongoClient("mongodb://localhost:27017")  
        # client = MongoClient("mongodb+srv://<username>:<password>@<cluster-url>/")
        print("✅ Successfully connected to MongoDB!")
        db = client["YOUR_DATABASE_NAME"]  # <-- Change this
        fs = gridfs.GridFS(db)
        return db, fs
    except Exception as e:
        print(f"❌ Error connecting to MongoDB: {e}")
        raise e

db, fs = connect_to_db()

# -----------------------------------------------------------------------------
# 2) FETCH VIDEO BY GRIDFS _id
# -----------------------------------------------------------------------------
def get_video_bytes(gridfs_id: str) -> bytes:
    """
    Fetches the binary data of a video from MongoDB GridFS given its file ObjectId.
    """
    try:
        gridfs_obj_id = ObjectId(gridfs_id)
        grid_out = fs.get(gridfs_obj_id)
        return grid_out.read()
    except Exception as e:
        print(f"❌ Error retrieving video bytes: {e}")
        raise e

# -----------------------------------------------------------------------------
# 3) EXTRACT AUDIO WITH FFMPEG (SHOW AN APPROXIMATE PROGRESS BAR)
# -----------------------------------------------------------------------------
def extract_audio_from_video(video_bytes: bytes) -> str:
    """
    Takes raw video bytes, writes to a temp MP4, and uses ffmpeg to extract audio as WAV.
    Returns the path to the temporary WAV file. Includes an approximate progress bar.
    """
    # 3a) Write the video bytes to a temp .mp4 file
    video_file = tempfile.NamedTemporaryFile(suffix=".mp4", delete=False)
    video_file_path = video_file.name
    video_file.write(video_bytes)
    video_file.close()

    # 3b) Prepare the audio output path (temp .wav)
    audio_file = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
    audio_file_path = audio_file.name
    audio_file.close()

    # 3c) Build ffmpeg command manually (for easier progress capturing)
    command = [
        "ffmpeg",
        "-i", video_file_path,
        "-acodec", "pcm_s16le",
        "-ac", "1",       # mono
        "-ar", "16000",   # 16k sample rate (faster for speech models)
        "-y",             # overwrite
        audio_file_path
    ]

    print("Extracting audio with ffmpeg...")
    process = subprocess.Popen(command, stderr=subprocess.PIPE, stdout=subprocess.DEVNULL, text=True)

    # 3d) We'll parse lines from stderr to approximate progress
    #     FFmpeg typically outputs something like:
    #     "size= ... time=00:00:02.12 bitrate=..."
    #     We'll track the "time=" to guess progress.
    pbar = tqdm(desc="Audio Extraction", total=100, unit="%")
    current_percent = 0
    while True:
        line = process.stderr.readline()
        if not line:
            break

        # If we detect a "time=" sequence, we can do a naive increment
        if "time=" in line:
            # Just increment progress by a small step, up to 100
            if current_percent < 95:
                current_percent += 5
                pbar.n = current_percent
                pbar.refresh()

    process.wait()
    pbar.n = 100
    pbar.close()
    print("Audio extraction complete.")

    # Optionally remove the temp video file
    os.remove(video_file_path)

    return audio_file_path

# -----------------------------------------------------------------------------
# 4) TRANSCRIBE AUDIO WITH WHISPER (SHOW A SIMPLE PROGRESS BAR)
# -----------------------------------------------------------------------------
def transcribe_audio(audio_path: str) -> str:
    """
    Transcribes a WAV audio file to text using the Whisper 'tiny' model.
    Returns the text transcript and shows a progress bar.
    """
    # We load the small 'tiny' model for speed. Larger models = better accuracy but slower.
    model = whisper.load_model("tiny")  # or "base", "small", "medium", "large"
    print("Transcribing with Whisper. Please wait...")

    # We can’t easily track partial progress within the .transcribe() call,
    # so we’ll just spin a fake bar to indicate activity.
    # The bigger/longer your file, the longer the call will block.
    with tqdm(desc="Transcribing", total=1, unit="segments") as pbar:
        result = model.transcribe(audio_path)
        pbar.update(1)  # Done
    return result["text"]

# -----------------------------------------------------------------------------
# 5) WRAPPER: GET TRANSCRIPT
# -----------------------------------------------------------------------------
def get_transcript(gridfs_id: str) -> str:
    """
    High-level function that fetches the video from GridFS, extracts audio, and
    returns a transcription string.
    """
    # 5a) Fetch the video file’s raw bytes
    video_data = get_video_bytes(gridfs_id)

    # 5b) Extract audio
    audio_path = extract_audio_from_video(video_data)

    # 5c) Transcribe
    transcript = transcribe_audio(audio_path)

    # Cleanup: remove the temp audio file
    os.remove(audio_path)

    return transcript

# -----------------------------------------------------------------------------
# 6) MAIN: CLI usage
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python voice_to_text.py <gridfs_file_id>")
        sys.exit(1)

    video_id_input = sys.argv[1]
    text_transcript = get_transcript(video_id_input)
    print("\nFinal Transcript:\n", text_transcript)
