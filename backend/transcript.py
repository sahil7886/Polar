import os
import math
import requests
from pydub import AudioSegment
import subprocess
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("HUGGINGFACE_API_KEY")
# Hugging Face API settings
API_URL = "https://api-inference.huggingface.co/models/openai/whisper-large"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}



# Step 1: Extract audio from the MP4 file using ffmpeg
def extract_audio(mp4_path):
    audio_path = mp4_path.replace(".mp4", ".mp3")
    command = ["ffmpeg", "-i", mp4_path, "-vn", "-acodec", "mp3", audio_path]
    subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return audio_path


# Step 2: Split the audio into chunks (30 seconds each by default)
def split_audio(audio_path, chunk_length_ms=20000):  # 30 seconds per chunk
    """Splits the audio file into smaller chunks."""
    audio = AudioSegment.from_file(audio_path)
    chunks = []
    num_chunks = math.ceil(len(audio) / chunk_length_ms)

    for i in range(num_chunks):
        start = i * chunk_length_ms
        end = (i + 1) * chunk_length_ms
        chunk = audio[start:end]
        chunk_path = f"chunk_{i}.mp3"
        chunk.export(chunk_path, format="mp3")
        chunks.append(chunk_path)

    return chunks


# Step 3: Transcribe each audio chunk using Hugging Face API
def transcribe_audio_chunk(audio_path):
    """Sends the extracted audio chunk to Hugging Face Whisper API and returns the transcript."""
    with open(audio_path, "rb") as f:
        response = requests.post(API_URL, headers=HEADERS, files={"file": f})

    if response.status_code != 200:
        print(f"Error: {response.status_code}, {response.text}")
        return "Transcription failed due to request error."

    result = response.json()

    if 'error' in result:
        print(f"API Error: {result['error']}")
        return "Transcription failed due to API error."

    return result.get("text", "Transcription failed.")


# Step 4: Transcribe the full MP4 video
def transcribe_mp4(mp4_path):
    audio_path = extract_audio(mp4_path)
    chunks = split_audio(audio_path)
    full_transcript = ""

    for chunk in chunks:
        transcript = transcribe_audio_chunk(chunk)
        full_transcript += transcript + " "
        os.remove(chunk)  # Remove chunk after processing

    os.remove(audio_path)  # Remove the extracted audio after processing
    return full_transcript.strip()


# Example usage
mp4_file_path = "../test_data/Video-12.mp4"  # Path to your MP4 file
transcript = transcribe_mp4(mp4_file_path)
print(transcript)
