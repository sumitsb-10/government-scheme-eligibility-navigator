"""
debug_pipeline.py - run pipeline in-process to get the real result
"""
import os
os.environ["PYTHONUTF8"] = "1"
os.environ["GEMINI_MODEL"] = "gemini-3.5-flash-lite"  # override .env for testing
import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

from agents.pipeline import run_pipeline

try:
    result = run_pipeline("I am a 28-year-old woman from a rural village in Rajasthan. I belong to SC community. My husband is a daily wage labourer and we earn about Rs. 6000 per month. We have no LPG connection. I have Aadhaar card.")
    print("SUCCESS")
    print("Eligible schemes:", result.eligible_scheme_count)
    print("Titles:", result.scheme_titles)
    print("Summary preview:", result.plain_summary[:300])
    if result.application_guides:
        g = result.application_guides[0]
        print(f"\nFirst guide: {g.scheme_title}")
        print(f"  Docs: {g.required_documents[:2]}")
        print(f"  Steps: {g.application_steps[:2]}")
except Exception as e:
    import traceback
    traceback.print_exc()
