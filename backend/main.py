"""
backend/main.py
FastAPI application exposing the multi-agent pipeline as REST endpoints.

Endpoints:
  GET  /health          — liveness check + ChromaDB document count
  POST /query           — run the full 4-agent pipeline for a citizen query
  GET  /schemes         — list all indexed schemes (titles + IDs)
  POST /ingest          — trigger re-ingestion of scheme documents
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Force UTF-8 output so Unicode characters in prompts/logs don't crash on Windows cp1252
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware

from backend.models import (
    QueryRequest,
    NavigatorResponse,
    ApplicationGuideResponse,
    EligibilityResultResponse,
    HealthResponse,
)
from agents.pipeline import run_pipeline
from agents.vector_store import get_vectorstore


app = FastAPI(
    title="Government Scheme Eligibility Navigator",
    description="A multi-agent AI system that helps citizens discover eligible government schemes.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ─── Health ───────────────────────────────────────────────────────────────────

@app.get("/health", response_model=HealthResponse, tags=["System"])
def health_check():
    """Liveness + readiness check."""
    try:
        vs = get_vectorstore()
        count = vs._collection.count()
    except Exception:
        count = None
    return HealthResponse(status="ok", version="1.0.0", indexed_schemes=count)


# ─── Query Pipeline ───────────────────────────────────────────────────────────

@app.post("/query", response_model=NavigatorResponse, tags=["Navigator"])
def query_schemes(request: QueryRequest):
    """
    Run the full 4-agent pipeline:
    Retrieval → Eligibility → Application → Explainer

    Returns eligible schemes with documents, steps, and plain-language summary.
    """
    try:
        result = run_pipeline(request.description)
    except Exception as e:
        safe_msg = str(e).encode("ascii", "replace").decode()
        raise HTTPException(status_code=500, detail=f"Pipeline error: {safe_msg}")

    return NavigatorResponse(
        plain_summary=result.plain_summary,
        eligible_scheme_count=result.eligible_scheme_count,
        scheme_titles=result.scheme_titles,
        application_guides=[
            ApplicationGuideResponse(
                scheme_id=g.scheme_id,
                scheme_title=g.scheme_title,
                ministry=g.ministry,
                required_documents=g.required_documents,
                application_steps=g.application_steps,
                apply_url=g.apply_url,
                helpline=g.helpline,
                estimated_time=g.estimated_time,
                tips=g.tips,
                matched_criteria=g.matched_criteria,
                notes=g.notes,
            )
            for g in result.application_guides
        ],
        eligibility_results=[
            EligibilityResultResponse(
                scheme_id=r.scheme_id,
                scheme_title=r.scheme_title,
                ministry=r.ministry,
                eligible=r.eligible,
                confidence=r.confidence,
                matched_criteria=r.matched_criteria,
                disqualifiers=r.disqualifiers,
                notes=r.notes,
            )
            for r in result.eligibility_results
        ],
    )


# ─── List Schemes ─────────────────────────────────────────────────────────────

@app.get("/schemes", tags=["Navigator"])
def list_schemes():
    """Return all indexed scheme titles and IDs."""
    try:
        vs = get_vectorstore()
        collection = vs._collection.get(include=["metadatas"])
        seen = {}
        for meta in collection["metadatas"]:
            sid = meta.get("id", meta.get("source", "unknown"))
            if sid not in seen:
                seen[sid] = {
                    "id": sid,
                    "title": meta.get("title", "Unknown"),
                    "ministry": meta.get("ministry", ""),
                    "tags": meta.get("tags", ""),
                }
        return {"count": len(seen), "schemes": list(seen.values())}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ─── Re-ingest ────────────────────────────────────────────────────────────────

def _run_ingest():
    from ingestion.ingest import ingest
    ingest()


@app.post("/ingest", tags=["System"])
def trigger_ingest(background_tasks: BackgroundTasks):
    """
    Trigger re-ingestion of scheme documents in the background.
    Useful after adding new PDFs to data/scheme_docs/.
    """
    background_tasks.add_task(_run_ingest)
    return {"message": "Ingestion started in background. Check server logs for progress."}


# ─── Entry point ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
