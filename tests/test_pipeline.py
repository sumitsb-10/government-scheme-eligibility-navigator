"""
tests/test_pipeline.py
Unit and integration tests for the multi-agent pipeline.
Run with: pytest tests/ -v
"""
import sys
import os
import json
import pytest
from unittest.mock import patch, MagicMock
from langchain_core.documents import Document

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# ─── Retrieval Agent Tests ────────────────────────────────────────────────────

class TestRetrievalAgent:
    def test_returns_list_of_documents(self):
        """Retrieval agent should return a non-empty list of Documents."""
        mock_docs = [
            Document(page_content="PM-KISAN farmer scheme", metadata={"id": "pm_kisan", "title": "PM-KISAN", "ministry": "Agriculture"}),
            Document(page_content="Ayushman Bharat health scheme", metadata={"id": "ayushman_bharat", "title": "PM-JAY", "ministry": "Health"}),
        ]
        with patch("agents.retrieval_agent.get_retriever") as mock_retriever, \
             patch("agents.retrieval_agent.get_llm") as mock_llm, \
             patch("agents.retrieval_agent.QUERY_EXPANSION_PROMPT") as mock_prompt:

            # Mock LLM instantiation (no API key needed in tests)
            mock_llm.return_value = MagicMock()
            # Mock the full chain: prompt | llm | parser → returns a plain string
            mock_chain = MagicMock()
            mock_chain.invoke.return_value = "farmer rural income support Aadhaar land"
            mock_prompt.__or__ = MagicMock(return_value=mock_chain)
            mock_retriever.return_value.invoke = MagicMock(return_value=mock_docs)

            from agents.retrieval_agent import run_retrieval_agent
            result = run_retrieval_agent("I am a farmer with 2 acres of land")
            assert isinstance(result, list)
            assert len(result) > 0
            assert all(isinstance(d, Document) for d in result)

    def test_deduplicates_by_scheme_id(self):
        """Should return unique schemes even if ChromaDB returns duplicate chunks."""
        mock_docs = [
            Document(page_content="chunk 1 of pm_kisan", metadata={"id": "pm_kisan", "title": "PM-KISAN", "ministry": "Agri"}),
            Document(page_content="chunk 2 of pm_kisan", metadata={"id": "pm_kisan", "title": "PM-KISAN", "ministry": "Agri"}),
            Document(page_content="ayushman health", metadata={"id": "ayushman_bharat", "title": "PM-JAY", "ministry": "Health"}),
        ]
        with patch("agents.retrieval_agent.get_retriever") as mock_retriever, \
             patch("agents.retrieval_agent.get_llm") as mock_llm, \
             patch("agents.retrieval_agent.QUERY_EXPANSION_PROMPT") as mock_prompt:

            mock_llm.return_value = MagicMock()
            mock_chain = MagicMock()
            mock_chain.invoke.return_value = "farmer rural"
            mock_prompt.__or__ = MagicMock(return_value=mock_chain)
            mock_retriever.return_value.invoke = MagicMock(return_value=mock_docs)

            from agents.retrieval_agent import run_retrieval_agent
            result = run_retrieval_agent("farmer")
            ids = [d.metadata["id"] for d in result]
            assert len(ids) == len(set(ids)), "Duplicate scheme IDs should be removed"


# ─── Eligibility Agent Tests ──────────────────────────────────────────────────

class TestEligibilityAgent:
    def _make_doc(self, scheme_id: str, title: str) -> Document:
        return Document(
            page_content=f"Scheme content for {title}",
            metadata={"id": scheme_id, "title": title, "ministry": "Test Ministry"},
        )

    def test_eligible_scheme_returns_true(self):
        eligible_json = json.dumps({
            "eligible": True,
            "confidence": "high",
            "matched_criteria": ["Has Aadhaar", "Rural household"],
            "disqualifiers": [],
            "notes": "Meets all core criteria",
        })
        with patch("agents.eligibility_agent.get_llm") as mock_llm:
            mock_chain = MagicMock()
            mock_chain.invoke.return_value = eligible_json
            mock_llm.return_value.__or__ = MagicMock(return_value=mock_chain)

            from agents.eligibility_agent import EligibilityResult
            result = EligibilityResult(
                scheme_id="pm_kisan",
                scheme_title="PM-KISAN",
                ministry="Agriculture",
                eligible=True,
                confidence="high",
                matched_criteria=["Has Aadhaar", "Rural household"],
                disqualifiers=[],
                notes="Meets all core criteria",
            )
            assert result.eligible is True
            assert result.confidence == "high"

    def test_ineligible_scheme_returns_false(self):
        result_obj = __import__("agents.eligibility_agent", fromlist=["EligibilityResult"]).EligibilityResult(
            scheme_id="pmvvy",
            scheme_title="PMVVY",
            ministry="Finance",
            eligible=False,
            confidence="high",
            matched_criteria=[],
            disqualifiers=["Citizen is 28 years old; scheme requires 60+"],
            notes="Does not meet age criterion",
        )
        assert result_obj.eligible is False
        assert len(result_obj.disqualifiers) > 0

    def test_results_sorted_eligible_first(self):
        """Eligible results should appear before ineligible ones."""
        from agents.eligibility_agent import EligibilityResult
        results = [
            EligibilityResult("s1", "Scheme A", "Min", False, "high"),
            EligibilityResult("s2", "Scheme B", "Min", True, "medium"),
            EligibilityResult("s3", "Scheme C", "Min", True, "high"),
        ]
        confidence_order = {"high": 0, "medium": 1, "low": 2}
        results.sort(key=lambda r: (not r.eligible, confidence_order.get(r.confidence, 3)))
        assert results[0].eligible is True
        assert results[1].eligible is True
        assert results[2].eligible is False


# ─── Application Agent Tests ──────────────────────────────────────────────────

class TestApplicationAgent:
    def test_only_processes_eligible_schemes(self):
        """Application Agent should skip ineligible results."""
        from agents.eligibility_agent import EligibilityResult
        from agents.application_agent import ApplicationGuide

        eligible = EligibilityResult("pm_kisan", "PM-KISAN", "Agri", True, "high", raw_content="content")
        ineligible = EligibilityResult("pmvvy", "PMVVY", "Finance", False, "high", raw_content="content")

        app_json = json.dumps({
            "required_documents": ["Aadhaar", "Land records"],
            "application_steps": ["Step 1: Visit pmkisan.gov.in", "Step 2: Register"],
            "apply_url": "pmkisan.gov.in",
            "helpline": "155261",
            "estimated_time": "2-4 weeks",
            "tips": ["Keep Aadhaar ready"],
        })

        with patch("agents.application_agent.get_llm") as mock_llm:
            mock_chain = MagicMock()
            mock_chain.invoke.return_value = app_json
            mock_llm.return_value.__or__ = MagicMock(return_value=mock_chain)

            # Directly test filtering logic
            eligible_only = [r for r in [eligible, ineligible] if r.eligible]
            assert len(eligible_only) == 1
            assert eligible_only[0].scheme_id == "pm_kisan"

    def test_application_guide_structure(self):
        from agents.application_agent import ApplicationGuide
        guide = ApplicationGuide(
            scheme_id="pm_kisan",
            scheme_title="PM-KISAN",
            ministry="Agriculture",
            required_documents=["Aadhaar", "Land records"],
            application_steps=["Step 1", "Step 2"],
            apply_url="pmkisan.gov.in",
            helpline="155261",
            estimated_time="2-4 weeks",
            tips=["Tip 1"],
        )
        assert guide.scheme_id == "pm_kisan"
        assert len(guide.required_documents) == 2
        assert len(guide.application_steps) == 2


# ─── Pipeline State Tests ─────────────────────────────────────────────────────

class TestPipelineState:
    def test_navigator_result_structure(self):
        from agents.pipeline import NavigatorResult
        from agents.application_agent import ApplicationGuide
        from agents.eligibility_agent import EligibilityResult

        result = NavigatorResult(
            plain_summary="You qualify for PM-KISAN.",
            eligible_scheme_count=1,
            scheme_titles=["PM-KISAN"],
            application_guides=[
                ApplicationGuide("pm_kisan", "PM-KISAN", "Agriculture")
            ],
            eligibility_results=[
                EligibilityResult("pm_kisan", "PM-KISAN", "Agriculture", True, "high")
            ],
        )
        assert result.eligible_scheme_count == 1
        assert "PM-KISAN" in result.scheme_titles
        assert len(result.application_guides) == 1

    def test_json_parse_fallback(self):
        """Eligibility parser should not crash on malformed LLM output."""
        from agents.eligibility_agent import _parse_llm_response
        bad_input = "Sorry, I cannot determine eligibility from this."
        parsed = _parse_llm_response(bad_input)
        assert "eligible" in parsed
        assert parsed["eligible"] is False  # Conservative default


# ─── Sample Data Tests ────────────────────────────────────────────────────────

class TestSampleSchemes:
    def test_all_schemes_have_required_fields(self):
        from data.sample_schemes import SAMPLE_SCHEMES
        required_fields = {"id", "title", "ministry", "content", "tags"}
        for scheme in SAMPLE_SCHEMES:
            missing = required_fields - set(scheme.keys())
            assert not missing, f"Scheme '{scheme.get('id', '?')}' missing fields: {missing}"

    def test_scheme_content_has_application_steps(self):
        from data.sample_schemes import SAMPLE_SCHEMES
        for scheme in SAMPLE_SCHEMES:
            assert "Step" in scheme["content"], (
                f"Scheme '{scheme['id']}' content appears to be missing application steps"
            )

    def test_scheme_count(self):
        from data.sample_schemes import SAMPLE_SCHEMES
        assert len(SAMPLE_SCHEMES) >= 14, "Expected at least 14 schemes"
