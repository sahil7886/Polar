from sentence_transformers import SentenceTransformer

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

def vectorize_transcript(text):
    return model.encode([text])[0].tolist()  
