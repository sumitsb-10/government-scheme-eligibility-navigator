"""
agents/pipeline.py
LangGraph multi-agent orchestration pipeline.

Graph:  START → retrieve → check_eligibility → build_applications → explain → END

State flows through each node, accumulating results.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import TypedDict

from langgraph.graph import StateGraph, END

from agents.retrieval_agent import run_retrieval_agent
from agents.eligibility_agent import run_eligibility_agent, EligibilityResult
from agents.application_agent import run_application_agent, ApplicationGuide
from agents.explainer_agent import run_explainer_agent, ExplainerOutput


# ─── Pipeline State ──────────────────────────────────────────────────────────

class PipelineState(TypedDict):
    """Shared state dict passed between LangGraph nodes."""
    user_description: str

    # Populated by each node
    retrieved_docs: list          # List[Document]
    eligibility_results: list     # List[EligibilityResult]
    application_guides: list      # List[ApplicationGuide]
    explainer_output: dict        # serialised ExplainerOutput


# ─── Node Functions ───────────────────────────────────────────────────────────

def node_retrieve(state: PipelineState) -> PipelineState:
    """Retrieval Agent node: query ChromaDB for relevant schemes."""
    print("\n=== [Node 1/4] Retrieval Agent ===")
    docs = run_retrieval_agent(state["user_description"])
    return {**state, "retrieved_docs": docs}


def node_check_eligibility(state: PipelineState) -> PipelineState:
    """Eligibility Agent node: evaluate user against each scheme."""
    print("\n=== [Node 2/4] Eligibility Agent ===")
    results = run_eligibility_agent(
        state["user_description"],
        state["retrieved_docs"],
    )
    return {**state, "eligibility_results": results}


def node_build_applications(state: PipelineState) -> PipelineState:
    """Application Agent node: generate docs + steps for eligible schemes."""
    print("\n=== [Node 3/4] Application Agent ===")
    guides = run_application_agent(
        state["user_description"],
        state["eligibility_results"],
    )
    return {**state, "application_guides": guides}


def node_explain(state: PipelineState) -> PipelineState:
    """Explainer Agent node: produce plain-language citizen summary."""
    print("\n=== [Node 4/4] Explainer Agent ===")
    output = run_explainer_agent(
        state["user_description"],
        state["application_guides"],
    )
    return {
        **state,
        "explainer_output": {
            "plain_summary": output.plain_summary,
            "eligible_scheme_count": output.eligible_scheme_count,
            "scheme_titles": output.scheme_titles,
        },
    }


# ─── Graph Assembly ───────────────────────────────────────────────────────────

def build_graph() -> StateGraph:
    graph = StateGraph(PipelineState)

    graph.add_node("retrieve", node_retrieve)
    graph.add_node("check_eligibility", node_check_eligibility)
    graph.add_node("build_applications", node_build_applications)
    graph.add_node("explain", node_explain)

    graph.set_entry_point("retrieve")
    graph.add_edge("retrieve", "check_eligibility")
    graph.add_edge("check_eligibility", "build_applications")
    graph.add_edge("build_applications", "explain")
    graph.add_edge("explain", END)

    return graph.compile()


# Compiled graph — imported by backend and tests
navigator_graph = build_graph()


# ─── Convenience Function ─────────────────────────────────────────────────────

@dataclass
class NavigatorResult:
    """Clean result object returned to callers (API, Streamlit, tests)."""
    plain_summary: str
    eligible_scheme_count: int
    scheme_titles: list[str]
    application_guides: list[ApplicationGuide]
    eligibility_results: list[EligibilityResult]


def run_pipeline(user_description: str) -> NavigatorResult:
    """
    Run the full 4-agent pipeline for a citizen's description.

    Args:
        user_description: Citizen's plain-language situation.

    Returns:
        NavigatorResult with all outputs.
    """
    initial_state: PipelineState = {
        "user_description": user_description,
        "retrieved_docs": [],
        "eligibility_results": [],
        "application_guides": [],
        "explainer_output": {},
    }

    final_state = navigator_graph.invoke(initial_state)

    return NavigatorResult(
        plain_summary=final_state["explainer_output"].get("plain_summary", ""),
        eligible_scheme_count=final_state["explainer_output"].get("eligible_scheme_count", 0),
        scheme_titles=final_state["explainer_output"].get("scheme_titles", []),
        application_guides=final_state["application_guides"],
        eligibility_results=final_state["eligibility_results"],
    )
