"""
config.py — Central configuration loaded from .env
"""
import os
from dotenv import load_dotenv

load_dotenv()

# LLM
LLM_PROVIDER: str = os.getenv("LLM_PROVIDER", "gemini")
GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite")
GROQ_MODEL: str = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")
GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY", "")
GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")

# ChromaDB
CHROMA_PERSIST_DIR: str = os.getenv("CHROMA_PERSIST_DIR", "./data/chroma_db")
CHROMA_COLLECTION_NAME: str = "scheme_docs"

# Documents
SCHEME_DOCS_DIR: str = os.getenv("SCHEME_DOCS_DIR", "./data/scheme_docs")

# Retrieval
TOP_K_RETRIEVAL: int = 5  # How many chunks to fetch per query

# Backend
BACKEND_URL: str = os.getenv("BACKEND_URL", "http://localhost:8000")

# ── Startup validation ────────────────────────────────────────────────────────
_PLACEHOLDERS = {"your_google_gemini_api_key_here", "your_groq_api_key_here", ""}

def validate_api_keys():
    """
    Call this before any LLM/embedding operation.
    Raises a clear RuntimeError if the active provider's key is a placeholder.
    """
    if LLM_PROVIDER == "gemini":
        if GOOGLE_API_KEY in _PLACEHOLDERS:
            raise RuntimeError(
                "\n\n"
                "===========================================================\n"
                "  ERROR: GOOGLE_API_KEY is not set in your .env file.\n"
                "===========================================================\n"
                "  Get a FREE Gemini API key in 30 seconds:\n"
                "    1. Go to https://aistudio.google.com/app/apikey\n"
                "    2. Click 'Create API key'\n"
                "    3. Copy the key\n"
                "    4. Open your .env file and replace:\n"
                "         GOOGLE_API_KEY=your_google_gemini_api_key_here\n"
                "       with:\n"
                "         GOOGLE_API_KEY=AIza...your_real_key_here\n"
                "    5. Re-run: python ingestion/ingest.py\n"
                "===========================================================\n"
            )
    elif LLM_PROVIDER == "groq":
        if GROQ_API_KEY in _PLACEHOLDERS:
            raise RuntimeError(
                "\n\n"
                "===========================================================\n"
                "  ERROR: GROQ_API_KEY is not set in your .env file.\n"
                "===========================================================\n"
                "  Get a FREE Groq API key:\n"
                "    1. Go to https://console.groq.com/keys\n"
                "    2. Sign up / log in and click 'Create API Key'\n"
                "    3. Copy the key\n"
                "    4. Open your .env file and replace:\n"
                "         GROQ_API_KEY=your_groq_api_key_here\n"
                "       with:\n"
                "         GROQ_API_KEY=gsk_...your_real_key_here\n"
                "    5. Also set: LLM_PROVIDER=groq\n"
                "    6. Re-run: python ingestion/ingest.py\n"
                "===========================================================\n"
            )
    else:
        raise RuntimeError(
            f"Unknown LLM_PROVIDER '{LLM_PROVIDER}' in .env. "
            "Set it to 'gemini' or 'groq'."
        )
