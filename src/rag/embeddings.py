from sentence_transformers import SentenceTransformer

MODEL_NAME = "all-MiniLM-L6-v2"


def load_embedding_model():
    """Load the local sentence-transformer embedding model."""
    return SentenceTransformer(MODEL_NAME)


def generate_embeddings(chunks, model):
    """Generate embeddings for document chunks."""

    texts = [chunk["content"] for chunk in chunks]

    embeddings = model.encode(
        texts,
        convert_to_numpy=True
    )

    return embeddings