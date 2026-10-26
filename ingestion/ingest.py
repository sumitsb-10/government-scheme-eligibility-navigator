"""
ingestion/ingest.py
Loads scheme data from data/sample_schemes.py into ChromaDB.
Also supports loading real PDF/DOCX files from data/scheme_docs/.

Usage:
    python ingestion/ingest.py
"""
import sys
import os

# Allow imports from project root
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

import config
from agents.vector_store import get_vectorstore
from data.sample_schemes import SAMPLE_SCHEMES


def load_sample_schemes() -> list[Document]:
    """Convert SAMPLE_SCHEMES dicts into LangChain Documents."""
    docs = []
    for scheme in SAMPLE_SCHEMES:
        doc = Document(
            page_content=scheme["content"].strip(),
            metadata={
                "id": scheme["id"],
                "title": scheme["title"],
                "ministry": scheme["ministry"],
                "tags": ", ".join(scheme.get("tags", [])),
                "source": "sample_schemes",
            },
        )
        docs.append(doc)
    print(f"[ingest] Loaded {len(docs)} scheme documents from sample data.")
    return docs


def load_pdf_docs() -> list[Document]:
    """Load any PDF files placed in data/scheme_docs/."""
    from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader

    docs = []
    docs_dir = config.SCHEME_DOCS_DIR

    if not os.path.exists(docs_dir):
        return docs

    for fname in os.listdir(docs_dir):
        fpath = os.path.join(docs_dir, fname)
        try:
            if fname.lower().endswith(".pdf"):
                loader = PyPDFLoader(fpath)
                loaded = loader.load()
                for d in loaded:
                    d.metadata["source"] = fname
                docs.extend(loaded)
                print(f"[ingest] Loaded PDF: {fname} ({len(loaded)} pages)")
            elif fname.lower().endswith(".docx"):
                loader = Docx2txtLoader(fpath)
                loaded = loader.load()
                for d in loaded:
                    d.metadata["source"] = fname
                docs.extend(loaded)
                print(f"[ingest] Loaded DOCX: {fname}")
        except Exception as e:
            print(f"[ingest] WARNING: Could not load {fname}: {e}")

    return docs


def split_documents(docs: list[Document]) -> list[Document]:
    """Split large documents into smaller chunks for better retrieval."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100,
        separators=["\n\n", "\n", ". ", " "],
    )
    chunks = splitter.split_documents(docs)
    print(f"[ingest] Split into {len(chunks)} chunks.")
    return chunks


def ingest():
    """Main ingestion pipeline: load → split → embed → store."""
    # Validate API key before doing any work
    from config import validate_api_keys
    validate_api_keys()

    print("[ingest] Starting ingestion pipeline...")

    # Gather documents
    all_docs = load_sample_schemes() + load_pdf_docs()

    if not all_docs:
        print("[ingest] No documents found. Exiting.")
        return

    # Split into chunks
    chunks = split_documents(all_docs)

    # Get vectorstore and add documents
    vs = get_vectorstore()

    # Clear existing collection to avoid duplicates on re-run
    vs.delete_collection()
    # Re-initialise after deletion
    from agents.vector_store import reset_vectorstore
    reset_vectorstore()
    vs = get_vectorstore()

    # Add chunks in batches of 50 to avoid rate-limit issues
    batch_size = 50
    for i in range(0, len(chunks), batch_size):
        batch = chunks[i : i + batch_size]
        vs.add_documents(batch)
        print(f"[ingest] Embedded batch {i // batch_size + 1} ({len(batch)} chunks)")

    print(f"[ingest] Done! Ingestion complete. {len(chunks)} chunks stored in ChromaDB.")


if __name__ == "__main__":
    ingest()
