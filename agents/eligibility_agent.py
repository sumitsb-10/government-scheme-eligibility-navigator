"""
agents/eligibility_agent.py
Evaluates the user's details against each retrieved scheme's eligibility
criteria and returns a structured verdict for each scheme.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from langchain_core.documents import Document
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from agents.llm_factory import get_llm


ELIGIBILITY_PROMPT = ChatPromptTemplate.from_messages([
    (
        "system",
        """You are a strict government scheme eligibility officer.
Given a citizen's description and a scheme's document excerpt, determine eligibility.

Respond with EXACTLY this JSON format (no markdown, no extra text):
{{
  "eligible": true or false,
  "confidence": "high" or "medium" or "low",
  "matched_criteria": ["criterion 1", "criterion 2"],
  "disqualifiers": ["reason 1 if not eligible"],
  "notes": "one sentence explanation"
}}

Rules:
- Set eligible=true only if the citizen clearly meets the core criteria.
- Set eligible=false if any hard exclusion applies.
- Set confidence=low if key information is missing from the description.
- matched_criteria: list the specific criteria the citizen meets.
- disqualifiers: list reasons for ineligibility (empty list if eligible).
""",
    ),
    (
        "human",
        "Citizen description:\n{user_description}\n\nScheme document:\n{scheme_content}\n\nScheme title: {scheme_title}",
    ),
])


@dataclass
class EligibilityResult:
    scheme_id: str
    scheme_title: str
    ministry: str
    eligible: bool
    confidence: str  # "high" | "medium" | "low"
    matched_criteria: list[str] = field(default_factory=list)
    disqualifiers: list[str] = field(default_factory=list)
    notes: str = ""
    raw_content: str = ""  # full scheme text, passed downstream


def _parse_llm_response(raw: str) -> dict:
    """Parse JSON from LLM response, with fallback."""
    import json
    import re

    # Strip markdown code fences if present
    raw = re.sub(r"```(?:json)?", "", raw).strip()

    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        # Fallback: return a conservative default
        return {
            "eligible": False,
            "confidence": "low",
            "matched_criteria": [],
            "disqualifiers": ["Could not parse eligibility response"],
            "notes": raw[:200],
        }


def run_eligibility_agent(
    user_description: str,
    retrieved_docs: list[Document],
) -> list[EligibilityResult]:
    """
    For each retrieved scheme document, ask the LLM whether the citizen
    is eligible. Returns a list of EligibilityResult objects.

    Args:
        user_description: The citizen's plain-language description.
        retrieved_docs: Documents from the Retrieval Agent.

    Returns:
        List of EligibilityResult, sorted: eligible first, then by confidence.
    """
    import time

    llm = get_llm(temperature=0.0)
    chain = ELIGIBILITY_PROMPT | llm | StrOutputParser()
    results: list[EligibilityResult] = []

    for i, doc in enumerate(retrieved_docs):
        scheme_title = doc.metadata.get("title", "Unknown Scheme")
        scheme_id = doc.metadata.get("id", "unknown")
        ministry = doc.metadata.get("ministry", "")

        # Free-tier rate limit: 5 RPM → wait 13s between calls (after first)
        if i > 0:
            time.sleep(13)

        print(f"[EligibilityAgent] Checking: {scheme_title.encode('ascii', 'replace').decode()}")

        raw_response = chain.invoke({
            "user_description": user_description,
            "scheme_content": doc.page_content,
            "scheme_title": scheme_title,
        })

        parsed = _parse_llm_response(raw_response)

        result = EligibilityResult(
            scheme_id=scheme_id,
            scheme_title=scheme_title,
            ministry=ministry,
            eligible=parsed.get("eligible", False),
            confidence=parsed.get("confidence", "low"),
            matched_criteria=parsed.get("matched_criteria", []),
            disqualifiers=parsed.get("disqualifiers", []),
            notes=parsed.get("notes", ""),
            raw_content=doc.page_content,
        )
        results.append(result)

    # Sort: eligible+high first, then eligible+medium, then rest
    confidence_order = {"high": 0, "medium": 1, "low": 2}
    results.sort(
        key=lambda r: (not r.eligible, confidence_order.get(r.confidence, 3))
    )

    eligible_count = sum(1 for r in results if r.eligible)
    print(f"[EligibilityAgent] {eligible_count}/{len(results)} schemes passed eligibility.")
    return results
