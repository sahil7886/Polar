from flask import Flask, Response, request
from flask_cors import CORS
from bson.objectid import ObjectId
import gridfs
from database.dbOperations import videos_collection, users_collection
import random
import os
import requests

app = Flask(__name__)
CORS(app)

# Connect GridFS
fs = gridfs.GridFS(videos_collection.database)

# In-memory store: user_id -> set of visited video _id
user_visited_videos = {}

@app.route("/randomize_feed", methods=["GET"])
def randomize_feed():
    """API endpoint to fetch a random video that hasn't been returned yet."""
    user_id = request.args.get("user_id")
    if not user_id:
        return {"error": "Missing user_id parameter"}, 400

    # If this user hasn't been seen, init their visited set
    if user_id not in user_visited_videos:
        user_visited_videos[user_id] = set()

    visited_ids = user_visited_videos[user_id]

    # Count how many videos have not been visited by this user
    unvisited_count = videos_collection.count_documents({"_id": {"$nin": list(visited_ids)}})
    if unvisited_count == 0:
        return {"error": "No more new videos available."}, 403

    # Pick a random index in [0, unvisited_count - 1]
    random_index = random.randint(0, unvisited_count - 1)

    # Skip to that random index to fetch a single document
    random_video_cursor = videos_collection.find({"_id": {"$nin": list(visited_ids)}}).skip(random_index).limit(1)
    random_video = random_video_cursor.next()

    # Validate that the "url" field is present and starts with "gridfs://"
    if not random_video or "url" not in random_video or not random_video["url"].startswith("gridfs://"):
        return {"error": "No valid videos available in the database."}, 403

    # Mark this video as visited for the user
    visited_ids.add(random_video["_id"])

    # Extract GridFS ID from the "gridfs://" URL format
    gridfs_id = random_video["url"].replace("gridfs://", "")

    return {
        "_id": str(random_video["_id"]),
        "uploader_id": random_video["uploader_id"],
        "gridfs_id": gridfs_id,
        "bias_score": random_video.get("bias_score")
    }

@app.route("/stream/<video_id>")
def stream_video(video_id):
    """Streams an MP4 video stored in MongoDB GridFS."""
    try:
        video_file = fs.get(ObjectId(video_id))
    except gridfs.errors.NoFile:
        return {"error": "Video not found"}, 404

    def generate():
        while chunk := video_file.read(8192):
            yield chunk

    return Response(generate(), content_type="video/mp4")



#TODO: make this function work and make it connect to frontend
@app.route("/summary/<video_id>")
def generate_summary_from_video(video_id: str) -> str:
    """
    Generates a concise title and summary from a given video_id by fetching its transcript from MongoDB.
    Returns the generated response as a string.
    """
    # Load environment variables
    API_KEY = os.environ.get("HUGGINGFACE_API_KEY")
    if not API_KEY:
        raise ValueError("HUGGINGFACE_API_KEY is not set in environment variables.")

    # Fetch video document from MongoDB
    print("Received video_id: ", video_id)
    video_document = videos_collection.find_one({"_id": ObjectId(video_id)})
    
    if not video_document or "transcript" not in video_document:
        return {"error": "Transcript not found for the provided video_id."}
    
    transcript = video_document["transcript"]
    if (transcript != ""):
        print("Transcript fetched")
    elif (transcript == ""):
        print("Transcript empty")
    else:
        print("Transcript fetch unsuccessful:", type(transcript))

    # Hugging Face API settings
    API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.3"
    HEADERS = {"Authorization": f"Bearer {API_KEY}"}

    # Create the API request prompt
    prompt = f"""
    You are an AI assistant that summarizes transcripts into a compelling and neutral title (3 words or less) and a brief description.

    Based on the following transcript, generate a *concise and informative title* along with a *description* summarizing the topic.

    After that provide 2 lines on why this topic is politically contended. Do not make bullet points. Make paragraphs

    Transcript:
    {transcript}
    """

    # Send request to Hugging Face API
    response = requests.post(API_URL, headers=HEADERS, json={"inputs": prompt})

    if response.status_code == 200:
        result = response.json()
        generated_text = result[0]['generated_text']
        trimmed_response = generated_text[len(prompt):].strip()
        return trimmed_response
    else:
        return f"Error {response.status_code}: {response.text}"

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)