# services/retriever.py

from langchain_community.vectorstores import FAISS

# Minimum cosine similarity a chunk must have to be included in context.
# Chunks below this threshold are likely from unrelated page sections.
SIMILARITY_THRESHOLD = 0.50


def get_relevant_chunks(
    vector_db: FAISS,
    query: str,
    k: int = 6,
) -> tuple[str, bool]:
    """
    Retrieve the top-k most relevant chunks for `query`.

    Returns:
        (context_text, found_relevant)
        - context_text: joined chunk text, or empty string
        - found_relevant: True if at least one chunk passed the threshold
    """
    # similarity_search_with_relevance_scores returns (doc, score) pairs
    # where score is cosine similarity in [0, 1]
    results = vector_db.similarity_search_with_relevance_scores(query, k=k)

    passing = [
        (doc, score)
        for doc, score in results
        if score >= SIMILARITY_THRESHOLD
    ]

    if not passing:
        return "", False

    context = "\n\n".join(doc.page_content for doc, _ in passing)
    return context, True