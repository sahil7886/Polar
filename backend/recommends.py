from transformers import pipeline
from bertopic import BERTopic
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from umap import UMAP
from database.dbOperations import videos_collection, users_collection  # Import from database
from bson.objectid import ObjectId

# Load the zero-shot classification model
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

# Labels for classification
labels = ["progressive policies", "conservative policies", "neutral"]


def get_top_k_similar(video_id, k=5):
    """
    Finds the top k most similar videos from the database using cosine similarity.

    :param video_id: ID of the target video
    :param k: Number of top similar videos to retrieve
    :return: List of top k similar video IDs
    """
    target_video = videos_collection.find_one({"_id": ObjectId(video_id)})
    if not target_video or "embedding" not in target_video:
        return {"error": "Video not found or missing embeddings."}

    target_vector = np.array(target_video["embedding"], dtype=np.float32)

    all_videos = list(videos_collection.find({"_id": {"$ne": ObjectId(video_id)}}, {"_id": 1, "embedding": 1}))

    if not all_videos:
        return {"error": "No other videos found."}

    video_ids = [str(v["_id"]) for v in all_videos]
    all_vectors = np.array([v["embedding"] for v in all_videos], dtype=np.float32)

    similarities = cosine_similarity(target_vector.reshape(1, -1), all_vectors).flatten()
    top_k_indices = np.argsort(similarities)[::-1][:k]

    return [video_ids[i] for i in top_k_indices]


def get_bias_score(text):
    result = classifier(text, labels)
    scores = {label: score for label, score in zip(result["labels"], result["scores"])}
    bias_score = scores["conservative policies"] - scores["progressive policies"]
    return bias_score


def calculate_user_bias(current_user_bias, pole_bias, user_num_poles):
    alpha = 1 / (user_num_poles + 1)
    new_user_bias = (1 - alpha) * current_user_bias + alpha * pole_bias
    return new_user_bias


def randomize_feed(user_id):
    user = users_collection.find_one({"_id": ObjectId(user_id)})
    if not user:
        return f"User with ID {user_id} not found."
    
    user_bias = user.get("bias_score", 0.0)
    user_num_poles = user.get("num_poles", 0)

    random_videos = list(videos_collection.aggregate([{"$sample": {"size": 10}}]))
    if not random_videos:
        return "No videos available in the database."
    
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
        return "No suitable video found."
