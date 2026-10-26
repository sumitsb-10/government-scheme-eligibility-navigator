"""
agents/gemini_embeddings.py

A lightweight LangChain-compatible embedding class that calls the
Gemini Embeddings REST API directly (v1beta), bypassing the broken
gRPC stack in langchain-google-genai 2.x.

Model used: models/gemini-embedding-001  (3072 dims, free tier)
"""
from __future__ import annotations

import httpx
from typing import List
from langchain_core.embeddings import Embeddings

import config

_BASE_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-embedding-001"


class GeminiRESTEmbeddings(Embeddings):
    """
    Calls the Gemini embedContent REST endpoint directly.
    Works regardless of google-ai-generativelanguage version conflicts.
    """

    def __init__(self, api_key: str | None = None):
        self.api_key = api_key or config.GOOGLE_API_KEY

    def _embed_single(self, text: str) -> List[float]:
        url = f"{_BASE_URL}:embedContent?key={self.api_key}"
        payload = {
            "model": "models/gemini-embedding-001",
            "content": {"parts": [{"text": text}]},
        }
        resp = httpx.post(url, json=payload, timeout=30)
        if resp.status_code != 200:
            raise RuntimeError(
                f"Gemini embedding API error {resp.status_code}: {resp.text[:300]}"
            )
        return resp.json()["embedding"]["values"]

    def _embed_batch(self, texts: List[str]) -> List[List[float]]:
        """Batch embed via batchEmbedContents endpoint."""
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-embedding-001:batchEmbedContents?key={self.api_key}"
        requests_payload = [
            {
                "model": "models/gemini-embedding-001",
                "content": {"parts": [{"text": t}]},
            }
            for t in texts
        ]
        resp = httpx.post(
            url, json={"requests": requests_payload}, timeout=60
        )
        if resp.status_code != 200:
            raise RuntimeError(
                f"Gemini batch embedding API error {resp.status_code}: {resp.text[:300]}"
            )
        return [e["values"] for e in resp.json()["embeddings"]]

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Embed a list of documents in batches of 100 (API limit)."""
        all_embeddings: List[List[float]] = []
        batch_size = 100
        for i in range(0, len(texts), batch_size):
            batch = texts[i : i + batch_size]
            all_embeddings.extend(self._embed_batch(batch))
        return all_embeddings

    def embed_query(self, text: str) -> List[float]:
        """Embed a single query string."""
        return self._embed_single(text)
