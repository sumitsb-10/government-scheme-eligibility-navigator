"""
agents/application_agent.py
For each eligible scheme, generates a structured application guide:
required documents + numbered step-by-step application instructions.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from agents.llm_factory import get_llm
from agents.eligibility_agent import EligibilityResult


APPLICATION_PROMPT = ChatPromptTemplate.from_messages([
    (
        "system",
        """You are a government scheme application guide specialist.
Given a scheme document and a citizen's situation, extract precise application guidance.

Respond with EXACTLY this JSON format (no markdown, no extra text):
{{
  "required_documents": [
    "Document 1 description",
    "Document 2 description"
  ],
  "application_steps": [
    "Step 1: ...",
    "Step 2: ...",
    "Step 3: ..."
  ],
  "apply_url": "official URL or 'Visit nearest government office'",
  "helpline": "helpline number or null",
  "estimated_time": "e.g. '2-4 weeks' or 'Instant'",
  "tips": ["Tip 1 specific to this citizen's situation", "Tip 2"]
}}

Rules:
- Extract documents and steps DIRECTLY from the scheme text - do not invent.
- Tips should be personalised to the citizen's specific situation.
- Keep steps concise but complete.
""",
    ),
    (
        "human",
        "Citizen description:\n{user_description}\n\nScheme document:\n{scheme_content}\n\nScheme title: {scheme_title}",
    ),
])


@dataclass
class ApplicationGuide:
    scheme_id: str
    scheme_title: str
    ministry: str
    required_documents: list[str] = field(default_factory=list)
    application_steps: list[str] = field(default_factory=list)
    apply_url: str = ""
    helpline: str = ""
    estimated_time: str = ""
    tips: list[str] = field(default_factory=list)
    # Carried from eligibility for downstream use
    matched_criteria: list[str] = field(default_factory=list)
    notes: str = ""


def _parse_llm_response(raw: str) -> dict:
    import json, re
    raw = re.sub(r"```(?:json)?", "", raw).strip()
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return {
            "required_documents": ["See official scheme document"],
            "application_steps": ["Visit the official scheme portal for instructions"],
            "apply_url": "",
            "helpline": "",
            "estimated_time": "Varies",
            "tips": [],
        }


def run_application_agent(
    user_description: str,
    eligibility_results: list[EligibilityResult],
) -> list[ApplicationGuide]:
    """
    For each ELIGIBLE scheme, generate a detailed application guide.

    Args:
        user_description: Citizen's plain-language situation.
        eligibility_results: Output from the Eligibility Agent.

    Returns:
        List of ApplicationGuide for qualifying schemes only.
    """
    import time

    llm = get_llm(temperature=0.1)
    chain = APPLICATION_PROMPT | llm | StrOutputParser()
    guides: list[ApplicationGuide] = []

    eligible = [r for r in eligibility_results if r.eligible]

    for i, result in enumerate(eligible):
        # Free-tier rate limit: 5 RPM → wait 13s between calls (after first)
        if i > 0:
            time.sleep(13)

        print(f"[ApplicationAgent] Building guide for: {result.scheme_title.encode('ascii', 'replace').decode()}")

        raw_response = chain.invoke({
            "user_description": user_description,
            "scheme_content": result.raw_content,
            "scheme_title": result.scheme_title,
        })

        parsed = _parse_llm_response(raw_response)

        guide = ApplicationGuide(
            scheme_id=result.scheme_id,
            scheme_title=result.scheme_title,
            ministry=result.ministry,
            required_documents=parsed.get("required_documents", []),
            application_steps=parsed.get("application_steps", []),
            apply_url=parsed.get("apply_url", ""),
            helpline=str(parsed.get("helpline", "")) if parsed.get("helpline") else "",
            estimated_time=parsed.get("estimated_time", ""),
            tips=parsed.get("tips", []),
            matched_criteria=result.matched_criteria,
            notes=result.notes,
        )
        guides.append(guide)

    print(f"[ApplicationAgent] Generated guides for {len(guides)} eligible schemes.")
    return guides
