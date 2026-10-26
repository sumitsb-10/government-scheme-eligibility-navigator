"""
agents/retrieval_agent.py
RAG-based agent: takes the user's plain-language description and
retrieves the most relevant scheme document chunks from ChromaDB.
"""
from __future__ import annotations

from langchain_core.documents import Document
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from agents.llm_factory import get_llm
from agents.vector_store import get_retriever


QUERY_EXPANSION_PROMPT = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are a search query specialist for Indian government welfare schemes. "
        "Given a citizen's description of their situation, generate a concise search query "
        "(under 30 words) that captures the key eligibility keywords: occupation, income level, "
        "category (SC/ST/OBC/General), age, gender, location (rural/urban), and specific needs. "
        "Return ONLY the search query, nothing else.",
    ),
    ("human", "{user_description}"),
])


def run_retrieval_agent(user_description: str, k: int = 5) -> list[Document]:
    """
    Expand the user's description into a focused search query,
    then retrieve the top-k relevant scheme chunks from ChromaDB.

    Args:
        user_description: The citizen's plain-language situation.
        k: Number of document chunks to retrieve.

    Returns:
        List of LangChain Document objects (scheme chunks + metadata).
    """
    llm = get_llm(temperature=0.0)

    # Step 1: Expand user description into an optimised search query
    query_chain = QUERY_EXPANSION_PROMPT | llm | StrOutputParser()
    search_query = query_chain.invoke({"user_description": user_description})
    print(f"[RetrieverAgent] Expanded query: {search_query.encode('ascii', 'replace').decode()}")

    # Step 2: Retrieve relevant chunks from ChromaDB
    retriever = get_retriever(k=k)
    docs = retriever.invoke(search_query)

    # Deduplicate by scheme id — keep only best chunk per scheme
    seen_ids: set[str] = set()
    unique_docs: list[Document] = []
    for doc in docs:
        scheme_id = doc.metadata.get("id", doc.metadata.get("source", "unknown"))
        if scheme_id not in seen_ids:
            seen_ids.add(scheme_id)
            unique_docs.append(doc)

    print(f"[RetrieverAgent] Retrieved {len(unique_docs)} unique schemes.")
    return unique_docs
