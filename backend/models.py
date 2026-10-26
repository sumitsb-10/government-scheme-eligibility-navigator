"""
backend/models.py
Pydantic request/response models for the FastAPI API.
"""
from __future__ import annotations
from pydantic import BaseModel, Field
from typing import Optional


class QueryRequest(BaseModel):
    description: str = Field(
        ...,
        min_length=10,
        max_length=2000,
        description="Citizen's plain-language description of their situation",
        examples=["I am a 35-year-old farmer with 2 acres of land in rural Maharashtra. My family income is below 1 lakh per year. I have an Aadhaar card and a bank account."],
    )


class EligibilityResultResponse(BaseModel):
    scheme_id: str
    scheme_title: str
    ministry: str
    eligible: bool
    confidence: str
    matched_criteria: list[str]
    disqualifiers: list[str]
    notes: str


class ApplicationGuideResponse(BaseModel):
    scheme_id: str
    scheme_title: str
    ministry: str
    required_documents: list[str]
    application_steps: list[str]
    apply_url: str
    helpline: str
    estimated_time: str
    tips: list[str]
    matched_criteria: list[str]
    notes: str


class NavigatorResponse(BaseModel):
    plain_summary: str
    eligible_scheme_count: int
    scheme_titles: list[str]
    application_guides: list[ApplicationGuideResponse]
    eligibility_results: list[EligibilityResultResponse]


class HealthResponse(BaseModel):
    status: str
    version: str
    indexed_schemes: Optional[int] = None
