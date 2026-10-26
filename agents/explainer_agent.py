"""
agents/explainer_agent.py
Summarises the full pipeline results into plain, simple language
that any citizen can understand — no jargon, no legalese.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from agents.llm_factory import get_llm
from agents.application_agent import ApplicationGuide


EXPLAINER_PROMPT = ChatPromptTemplate.from_messages([
    (
        "system",
        """You are a friendly and empathetic citizen-services officer who explains
government schemes in simple, plain language. Your audience may be first-time users,
people with limited formal education, or those unfamiliar with government processes.

Given a summary of eligible schemes, write a warm, clear explanation.

Format your response as:
1. A short opening (1-2 sentences) acknowledging the citizen's situation.
2. For each scheme: a 2-3 sentence plain-language summary of what it offers and why they qualify.
3. A short closing with encouragement and the most important next step.

Rules:
- Use simple words. No acronyms without explanation.
- Be warm and encouraging - many citizens don't know their rights.
- Mention the helpline number for each scheme.
- Keep the entire response under 400 words.
""",
    ),
    (
        "human",
        "Citizen's situation: {user_description}\n\nEligible schemes summary:\n{schemes_summary}",
    ),
])

NO_SCHEMES_PROMPT = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are a helpful citizen-services officer. Be empathetic and constructive.",
    ),
    (
        "human",
        """A citizen described their situation as: {user_description}

Unfortunately, no government schemes were found that clearly match their profile
from the currently indexed database.

Write a 3-4 sentence empathetic response that:
1. Acknowledges their situation kindly.
2. Suggests they visit their nearest Common Service Centre (CSC) or Jan Seva Kendra for personalised help.
3. Mentions they can also check india.gov.in for a full list of central schemes.
4. Encourages them to re-describe their situation with more details (age, income, occupation, category).
""",
    ),
])


@dataclass
class ExplainerOutput:
    plain_summary: str
    eligible_scheme_count: int
    scheme_titles: list[str] = field(default_factory=list)


def _build_schemes_summary(guides: list[ApplicationGuide]) -> str:
    """Convert ApplicationGuide list into a compact text summary for the LLM."""
    lines = []
    for i, g in enumerate(guides, 1):
        lines.append(f"{i}. {g.scheme_title} ({g.ministry})")
        lines.append(f"   Why eligible: {g.notes}")
        lines.append(f"   Benefit: {g.matched_criteria[0] if g.matched_criteria else 'See scheme details'}")
        lines.append(f"   Helpline: {g.helpline or 'Not available'}")
        lines.append(f"   First step: {g.application_steps[0] if g.application_steps else 'Visit official portal'}")
        lines.append("")
    return "\n".join(lines)


def run_explainer_agent(
    user_description: str,
    application_guides: list[ApplicationGuide],
) -> ExplainerOutput:
    """
    Produce a plain-language summary for the citizen.

    Args:
        user_description: The citizen's original description.
        application_guides: Output from the Application Agent.

    Returns:
        ExplainerOutput with a human-friendly summary.
    """
    llm = get_llm(temperature=0.4)

    if not application_guides:
        # No eligible schemes found
        chain = NO_SCHEMES_PROMPT | llm | StrOutputParser()
        plain_text = chain.invoke({"user_description": user_description})
        return ExplainerOutput(
            plain_summary=plain_text,
            eligible_scheme_count=0,
            scheme_titles=[],
        )

    schemes_summary = _build_schemes_summary(application_guides)
    chain = EXPLAINER_PROMPT | llm | StrOutputParser()
    plain_text = chain.invoke({
        "user_description": user_description,
        "schemes_summary": schemes_summary,
    })

    print(f"[ExplainerAgent] Summary generated for {len(application_guides)} schemes.")

    return ExplainerOutput(
        plain_summary=plain_text,
        eligible_scheme_count=len(application_guides),
        scheme_titles=[g.scheme_title for g in application_guides],
    )
