# ✅ Updated Schemas and Database Operations

from dbConfig import db, fs  # Assuming GridFS and db are initialized
from datetime import datetime
from bson.objectid import ObjectId

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

    # Video metadata document
    video = {
        "uploader_id": uploader_id,
        "url": f"gridfs://{gridfs_id}",
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

