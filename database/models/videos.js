VideosSchema = {
    "uploader_id": str,
    "title": str,
    "topic_id": str,
    "bias_score": float,
    "views_count": int,
    "likes_count": int,
    "dislikes_count": int,
    "like-dislike-ratio" : float,

    "engagement": {
        "shares": int,
        "reports": int
    }
}