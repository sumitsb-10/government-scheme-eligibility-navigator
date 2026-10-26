"""
agents/vector_store.py
Singleton wrapper around ChromaDB so every agent shares the same collection.
Uses langchain-chroma (the official up-to-date integration).
"""
from __future__ import annotations

from langchain_chroma import Chroma
import config

_vectorstore: Chroma | None = None


def _get_embeddings():
    """
    Return an embedding model.
    - Gemini provider → GeminiRESTEmbeddings (direct REST, avoids gRPC conflicts)
    - Groq provider  → local Sentence Transformers (free, no API key needed)
    """
    provider = config.LLM_PROVIDER.lower()
    if provider == "gemini":
        from agents.gemini_embeddings import GeminiRESTEmbeddings
        return GeminiRESTEmbeddings(api_key=config.GOOGLE_API_KEY)
    # Groq has no embedding API — use a lightweight local model
    from langchain_community.embeddings import SentenceTransformerEmbeddings
    return SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")


def get_vectorstore() -> Chroma:
    """Return (and cache) the shared Chroma vectorstore."""
    global _vectorstore
    if _vectorstore is None:
        _vectorstore = Chroma(
            collection_name=config.CHROMA_COLLECTION_NAME,
            embedding_function=_get_embeddings(),
            persist_directory=config.CHROMA_PERSIST_DIR,
        )
    return _vectorstore


def get_retriever(k: int = config.TOP_K_RETRIEVAL):
    """Return a LangChain retriever over the scheme collection."""
    return get_vectorstore().as_retriever(
        search_type="similarity",
        search_kwargs={"k": k},
    )


def reset_vectorstore():
    """Clear the in-memory cache (used by ingestion after collection deletion)."""
    global _vectorstore
    _vectorstore = None
