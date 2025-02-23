
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from database.dbOperations import videos_collection, users_collection
from bson.objectid import ObjectId

def get_top_k_similar(video_id, k=5):
    """Finds the top k most similar videos using cosine similarity."""
    target_video = videos_collection.find_one({"_id": ObjectId(video_id)})
    if not target_video or "embedding" not in target_video:
        return None

    target_vector = np.array(target_video["embedding"], dtype=np.float32)

    all_videos = list(videos_collection.find({"_id": {"$ne": ObjectId(video_id)}}, {"_id": 1, "embedding": 1}))

    if not all_videos:
        return None

    video_ids = [str(v["_id"]) for v in all_videos]
    all_vectors = np.array([v["embedding"] for v in all_videos], dtype=np.float32)

    similarities = cosine_similarity(target_vector.reshape(1, -1), all_vectors).flatten()
    top_k_indices = np.argsort(similarities)[::-1][:k]

    return [video_ids[i] for i in top_k_indices]


def calculate_user_bias(current_user_bias, pole_bias, user_num_poles):
    """Adjusts user bias dynamically."""
    alpha = 1 / (user_num_poles + 1)
    new_user_bias = (1 - alpha) * current_user_bias + alpha * pole_bias
    return new_user_bias


def get_random_video(user_id):
    """Fetches the best random video for a user to balance bias."""
    user = users_collection.find_one({"_id": ObjectId(user_id)})
    if not user:
        return {"error": f"User with ID {user_id} not found."}

    user_bias = user.get("bias_score", 0.0)
    user_num_poles = user.get("num_poles", 0)

    random_videos = list(videos_collection.aggregate([{"$sample": {"size": 10}}]))
    if not random_videos:
        return {"error": "No videos available in the database."}

    best_video = None
    closest_bias_to_zero = float('inf')

    for video in random_videos:
        video_bias = video.get("bias_score", 0.0)
        new_bias = calculate_user_bias(user_bias, video_bias, user_num_poles)

        if abs(new_bias) < closest_bias_to_zero:
            closest_bias_to_zero = abs(new_bias)
            best_video = video

    if best_video:
        return {
            "_id": str(best_video["_id"]),
            "uploader_id": best_video["uploader_id"],
            "url": best_video["url"],
            "bias_score": best_video["bias_score"]
        }
    else:
        return {"error": "No suitable video found."}
