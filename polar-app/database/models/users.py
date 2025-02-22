UsersSchema = {
    "username": str,
    "email": str,
    "bias_score": float,
    "alignment": str,
    "videos_watched": [
        {
            "video_url": str,  # Video URL acts as a unique identifier
            "watched_at": str   # Timestamp of when it was watched
        }
    ]
}