from sentence_transformers import SentenceTransformer


# Load the SentenceTransformer model for embeddings
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

def embed_text(text):
    embedding = embedding_model.encode(text)
    return embedding