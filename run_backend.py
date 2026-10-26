"""
run_backend.py — Launch the FastAPI backend with UTF-8 forced for Windows.
Usage: python run_backend.py
"""
import os
import sys
import subprocess

# Force UTF-8 and set sensible model default if user's .env still has old model
env = {
    **os.environ,
    "PYTHONUTF8": "1",
}
# Only override GEMINI_MODEL if user hasn't changed it away from the broken default
if env.get("GEMINI_MODEL") in ("gemini-1.5-flash", "gemini-3.5-flash", ""):
    env["GEMINI_MODEL"] = "gemini-3.5-flash-lite"

if __name__ == "__main__":
    # Re-launch self with PYTHONUTF8=1 if not already set
    if os.environ.get("PYTHONUTF8") != "1":
        result = subprocess.run(
            [sys.executable, __file__],
            env=env,
        )
        sys.exit(result.returncode)

    # At this point PYTHONUTF8=1 is guaranteed
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")

    import uvicorn
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=False)
