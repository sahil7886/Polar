from fastapi import FastAPI, UploadFile, File
from sentence_transformers import SentenceTransformer
import numpy as np
from database.video_model import videos_collection
from backend.vectorize_transcript import vectorize_transcript
from backend.similarity import find_similar_videos

app = FastAPI()

@app.post("/upload_transcript/")
async def upload_transcript(video_id: str, title: str, file: UploadFile = File(...)):
    """
    Uploads a transcript, vectorizes it, and stores in MongoDB.
    """
    transcript_text = (await file.read()).decode("utf-8")

    # Generate vector embedding
    embedding = vectorize_transcript(transcript_text)

    # Store in MongoDB
    videos_collection.update_one(
        {"_id": video_id},
        {"$set": {"title": title, "transcript": transcript_text, "embedding": embedding}},
        upsert=True
    )

    return {"message": "Transcript uploaded and vectorized successfully"}

@app.get("/similar_videos/{video_id}")
async def get_similar_videos(video_id: str):
    """
    Retrieve similar videos based on transcript embeddings.
    """
    similar_videos = find_similar_videos(video_id)
    return similar_videos
