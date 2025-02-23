from dbOperations import videos_collection

# Add missing fields to existing documents (if they don't already exist)
videos_collection.update_many(
    {}, 
    {
        "$set": {
            "bias_score": 0.0,  # Default value
            "embedding": [],    # Default empty list
            "transcript": ""    # Default empty string (if missing)
        }
    }
)
print("Schema update applied successfully.")
