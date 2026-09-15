from src.data.documents import load_documents, chunk_documents
from src.rag.embeddings import load_embedding_model
from src.rag.retriever import build_index


def create_rag_index():
    """Load documents, create chunks, load the embedding model, and build the index."""

    documents = load_documents()
    chunks = chunk_documents(documents)

    model = load_embedding_model()
    document_embeddings = build_index(chunks, model)

    return {
        "chunks": chunks,
        "model": model,
        "document_embeddings": document_embeddings,
    }