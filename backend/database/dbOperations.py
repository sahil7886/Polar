# ✅ Updated Schemas and Database Operations

from .dbConfig import db, fs  # Assuming GridFS and db are initialized
from datetime import datetime
from bson.objectid import ObjectId
import os

from ..recommends import get_bias_score
from ..transcript import transcribe_mp4
from ..vectorize_transcript import vectorize_transcript

# Collections
users_collection = db["users"]
videos_collection = db["videos"]

# 🔹 User Operations
def insert_user(username, email, bias_score):
    user = {
        "username": username,
        "email": email,
        "bias_score": bias_score
    }
    return users_collection.insert_one(user).inserted_id

def get_user(username):
    return users_collection.find_one({"username": username})

def update_user_bias(user_id, new_bias_score):
    return users_collection.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": {"bias_score": new_bias_score}}
    )

def delete_user(user_id):
    return users_collection.delete_one({"_id": ObjectId(user_id)})

# 🔹 Video Operations
def insert_video(file_path, uploader_id, bias_score):
    # Save the video file to GridFS
    with open(file_path, "rb") as video_file:
        gridfs_id = fs.put(video_file, filename=file_path.split("/")[-1])
    if os.path.isfile(file_path) and file_path.lower().endswith(".mp4"):
        transcript = transcribe_mp4(file_path)
    # Video metadata document
    video = {
        "uploader_id": uploader_id,
        "url": f"gridfs://{gridfs_id}",
        "transcript": transcript,
        "bias_score": bias_score,
        "uploaded_at": datetime.utcnow()
    }

    # Insert metadata and return the auto-generated _id
    result = videos_collection.insert_one(video)
    return result.inserted_id

def get_videos_by_uploader(uploader_id):
    return list(videos_collection.find({"uploader_id": uploader_id}))

def delete_video(video_id):
    video_data = videos_collection.find_one({"_id": ObjectId(video_id)})
    if video_data:
        gridfs_id = video_data["url"].split("gridfs://")[-1]
        fs.delete(ObjectId(gridfs_id))
        videos_collection.delete_one({"_id": ObjectId(video_id)})
        return True
    return False

def update_video_bias_scores():
    videos = videos_collection.find()
    for video in videos:
        transcript = video.get("transcript", "")
        if transcript:
            new_bias_score = get_bias_score(transcript)
            videos_collection.update_one(
                {"_id": video["_id"]},
                {"$set": {"bias_score": new_bias_score}}
            )
    print("✅ All video bias scores have been updated.")

def update_video_embeddings():
    videos = videos_collection.find()
    for video in videos:
        transcript = video.get("transcript", "")
        if transcript:
            embedding = vectorize_transcript(transcript)
            videos_collection.update_one(
                {"_id": video["_id"]},
                {"$set": {"embedding": embedding}}
            )
    print("✅ All video embeddings have been updated.")

def populate_sample_videos():
    user = get_user("0")
    if not user:
        user_id = insert_user("0", "user0@example.com", 0.0)
    else:
        user_id = user["_id"]
    test_data_dir = "/Users/avantikashah/Documents/Polar/test_data"
    for filename in os.listdir(test_data_dir):
        file_path = os.path.join(test_data_dir, filename)
        if os.path.isfile(file_path):
            insert_video(file_path, str(user_id), 0.0)
    print("✅ All sample videos from test_data have been uploaded.")
    
def get_video_closest_to_user_bias(user_id):
    # Step 1: Retrieve the user's bias score
    user = users_collection.find_one({"_id": ObjectId(user_id)})
    if not user:
        return f"User with ID {user_id} not found."
    
    user_bias = user.get("bias_score", 0.0)  # Default bias score is 0.0 if not found

    # Step 2: Randomly sample 10 videos from the database
    random_videos = list(videos_collection.aggregate([{"$sample": {"size": 10}}]))
    
    if not random_videos:
        return "No videos found in the database."

    # Step 3: Find the video with the bias score closest to the user's bias
    closest_video = min(random_videos, key=lambda video: abs(video["bias_score"] - user_bias))

    # Step 4: Return video details
    return {
        "_id": str(closest_video["_id"]),
        "uploader_id": closest_video["uploader_id"],
        "url": closest_video["url"],
        "bias_score": closest_video["bias_score"]
    }

