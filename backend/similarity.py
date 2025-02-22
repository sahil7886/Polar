import numpy as np
import faiss
from database.video_model import videos_collection

def find_similar_videos(video_id, top_k=5):
    video = videos_collection.find_one({"_id": video_id})
    if not video or "embedding" not in video:
        return {"error": "Video not found or missing embeddings"}

    target_vector = np.array(video["embedding"], dtype=np.float32)

    all_videos = list(videos_collection.find({"_id": {"$ne": video_id}}, {"_id": 1, "embedding": 1}))

    if not all_videos:
        return {"error": "No other videos found"}

    video_ids = [v["_id"] for v in all_videos]
    all_vectors = np.array([v["embedding"] for v in all_videos], dtype=np.float32)

    dim = target_vector.shape[0]
    index = faiss.IndexFlatL2(dim)
    index.add(all_vectors)

    _, top_indices = index.search(target_vector.reshape(1, -1), top_k)
    top_video_ids = [video_ids[i] for i in top_indices[0]]

    return {"similar_videos": top_video_ids}
