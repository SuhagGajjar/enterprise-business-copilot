import numpy as np


def cosine_similarity(query_embedding, document_embeddings):
    """Calculate cosine similarity between a query and document embeddings."""

    query_norm = np.linalg.norm(query_embedding)
    document_norms = np.linalg.norm(
        document_embeddings,
        axis=1
    )

    similarities = np.dot(
        document_embeddings,
        query_embedding
    ) / (document_norms * query_norm)

    return similarities


def build_index(chunks, model):
    """Create an in-memory embedding index for document chunks."""

    document_embeddings = model.encode(
        [chunk["content"] for chunk in chunks],
        convert_to_numpy=True
    )

    return document_embeddings


def retrieve_chunks(
    query,
    chunks,
    document_embeddings,
    model,
    top_k=3
):
    """Retrieve the most relevant document chunks for a query."""

    query_embedding = model.encode(
        query,
        convert_to_numpy=True
    )

    similarities = cosine_similarity(
        query_embedding,
        document_embeddings
    )

    ranked_indices = np.argsort(
        similarities
    )[::-1]

    results = []

    for index in ranked_indices[:top_k]:
        result = chunks[index].copy()
        result["similarity"] = float(similarities[index])
        results.append(result)

    return results