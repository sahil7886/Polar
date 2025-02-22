from database.db_config import db
from datetime import datetime
from bson.objectid import ObjectId

users_collection = db["users"]
videos_collection = db["videos"]

def insert_user(username, email, bias_score, alignment):
    user = {
        "username": username,
        "email": email,
        "bias_score": bias_score,
        "alignment": alignment,
    }
    return users_collection.insert_one(user).inserted_id

def get_user(username):
    return users_collection.find_one({"username": username})

def update_user_bias(user_id, new_bias_score, new_alignment):
    return users_collection.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": {"bias_score": new_bias_score, "alignment": new_alignment}}
    )

def delete_user(user_id):
    return users_collection.delete_one({"_id": ObjectId(user_id)})

def insert_video(uploader_id, title, topic_id, bias_score):
    video = {
        "uploader_id": uploader_id,
        "title": title,
        "topic_id": topic_id,
        "bias_score": bias_score,
        "views_count": 0,
        "likes_count": 0,
        "dislikes_count": 0,
        "engagement": {"shares": 0, "reports": 0}
    }
    return videos_collection.insert_one(video).inserted_id

def get_videos_by_topic(topic_id):
    return list(videos_collection.find({"topic_id": topic_id}))

def increment_video_views(video_id):
    return videos_collection.update_one({"_id": ObjectId(video_id)}, {"$inc": {"views_count": 1}})

# 🔹 Update Video Engagement (Likes, Dislikes, Shares, Reports)
def update_video_engagement(video_id, likes=None, dislikes=None, shares=None, reports=None):
    update_data = {}
    if likes is not None:
        update_data["likes_count"] = likes
    if dislikes is not None:
        update_data["dislikes_count"] = dislikes
    if shares is not None:
        update_data["engagement.shares"] = shares
    if reports is not None:
        update_data["engagement.reports"] = reports
    
    return videos_collection.update_one({"_id": ObjectId(video_id)}, {"$set": update_data})

# 🔹 Delete a Video
def delete_video(video_id):
    return videos_collection.delete_one({"_id": ObjectId(video_id)})
