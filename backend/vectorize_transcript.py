from sentence_transformers import SentenceTransformer

# Load model
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

def vectorize_transcript(text):
    """
    Vectorizes the transcript text using MiniLM.
    :param text: str, transcript of the video
    :return: list, 384-dimensional embedding vector
    """
    return model.encode([text])[0].tolist()  # Convert NumPy array to list
