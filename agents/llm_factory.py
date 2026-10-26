"""
agents/llm_factory.py
Returns a configured LangChain chat model based on LLM_PROVIDER in .env.
Supports Gemini (free tier) and Groq (free tier).
"""
from langchain_core.language_models import BaseChatModel
import config


def get_llm(temperature: float = 0.2) -> BaseChatModel:
    """Return the configured LLM instance."""
    config.validate_api_keys()
    provider = config.LLM_PROVIDER.lower()

    if provider == "gemini":
        from langchain_google_genai import ChatGoogleGenerativeAI
        return ChatGoogleGenerativeAI(
            model=config.GEMINI_MODEL,
            google_api_key=config.GOOGLE_API_KEY,
            temperature=temperature,
        )

    if provider == "groq":
        from langchain_groq import ChatGroq
        return ChatGroq(
            model=config.GROQ_MODEL,
            groq_api_key=config.GROQ_API_KEY,
            temperature=temperature,
        )

    raise ValueError(
        f"Unsupported LLM_PROVIDER '{provider}'. Choose 'gemini' or 'groq'."
    )
