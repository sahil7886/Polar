UsersSchema = {
    "username": str,
    "email": str,
    "bias_score": float,
    "alignment": str,
    "videos_watched": [
        {
            "video_url": str,  
            "video_id": str
        }
    ]
}