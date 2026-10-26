"""
frontend/app.py
Streamlit citizen-facing UI for the Government Scheme Eligibility Navigator.

Run with:
    streamlit run frontend/app.py
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import streamlit as st
import httpx
import time

import config

# ─── Page Config ──────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="Government Scheme Eligibility Navigator",
    page_icon="🇮🇳",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Custom CSS ───────────────────────────────────────────────────────────────

st.markdown("""
<style>
    .main-title {
        font-size: 2rem;
        font-weight: 700;
        color: #1a3c6e;
        margin-bottom: 0.2rem;
    }
    .subtitle {
        font-size: 1rem;
        color: #555;
        margin-bottom: 1.5rem;
    }
    .scheme-card {
        background: #f0f7ff;
        border-left: 4px solid #1a3c6e;
        border-radius: 6px;
        padding: 1rem 1.2rem;
        margin-bottom: 1rem;
    }
    .scheme-title {
        font-size: 1.15rem;
        font-weight: 700;
        color: #1a3c6e;
    }
    .ministry-tag {
        font-size: 0.78rem;
        color: #666;
        margin-bottom: 0.5rem;
    }
    .badge-eligible {
        background: #d4edda;
        color: #155724;
        padding: 2px 10px;
        border-radius: 12px;
        font-size: 0.78rem;
        font-weight: 600;
    }
    .badge-ineligible {
        background: #f8d7da;
        color: #721c24;
        padding: 2px 10px;
        border-radius: 12px;
        font-size: 0.78rem;
    }
    .summary-box {
        background: #fffbea;
        border: 1px solid #f0c040;
        border-radius: 8px;
        padding: 1.2rem;
        margin-bottom: 1.5rem;
    }
    .step-item {
        margin-bottom: 0.3rem;
    }
    .tip-box {
        background: #e8f4fd;
        border-radius: 6px;
        padding: 0.6rem 1rem;
        margin-top: 0.5rem;
        font-size: 0.9rem;
    }
    .helpline-badge {
        display: inline-block;
        background: #fff3cd;
        color: #856404;
        padding: 2px 10px;
        border-radius: 12px;
        font-size: 0.82rem;
        font-weight: 600;
        margin-top: 0.4rem;
    }
</style>
""", unsafe_allow_html=True)

# ─── Sidebar ──────────────────────────────────────────────────────────────────

with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/5/55/Emblem_of_India.svg", width=60)
    st.markdown("### 🇮🇳 Scheme Navigator")
    st.markdown("---")

    st.markdown("**How to use:**")
    st.markdown("""
1. Describe your situation in the box
2. Include details like:
   - Age & gender
   - Occupation / work type
   - Monthly/annual income
   - Location (rural/urban)
   - Caste category (General/OBC/SC/ST)
   - Family details
3. Click **Find My Schemes**
""")
    st.markdown("---")

    backend_url = st.text_input(
        "Backend URL",
        value=config.BACKEND_URL,
        help="FastAPI backend URL",
    )

    st.markdown("---")
    st.caption("Powered by LangChain · LangGraph · ChromaDB · Gemini/Groq")

    # Backend health check
    if st.button("🔍 Check Backend Status"):
        try:
            r = httpx.get(f"{backend_url}/health", timeout=5)
            data = r.json()
            st.success(f"✅ Backend online — {data.get('indexed_schemes', '?')} chunks indexed")
        except Exception as e:
            st.error(f"❌ Backend offline: {e}")

    if st.button("🔄 Re-ingest Schemes"):
        try:
            r = httpx.post(f"{backend_url}/ingest", timeout=5)
            st.info(r.json().get("message", "Ingestion triggered"))
        except Exception as e:
            st.error(f"Error: {e}")


# ─── Main Title ───────────────────────────────────────────────────────────────

st.markdown('<div class="main-title">🏛️ Government Scheme Eligibility Navigator</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Tell us about yourself — we\'ll find the government schemes you qualify for and show you exactly how to apply.</div>', unsafe_allow_html=True)

# ─── Prompt Examples ─────────────────────────────────────────────────────────

EXAMPLES = [
    "I am a 28-year-old woman from a rural village in Rajasthan. I belong to an SC community. My husband is a daily wage labourer and we earn about Rs. 6,000 per month. We live in a small kutcha house. We have no LPG connection. I have an Aadhaar card.",
    "I am a 45-year-old farmer from rural Maharashtra. I own 3 acres of land. My annual family income is about Rs. 80,000. I have Aadhaar and a bank account. I grow wheat and soybean.",
    "I am a 20-year-old student from Bihar. I just passed Class 12 with 78% marks in the science stream and have taken admission in B.Sc. My father is a daily wage worker and our total family income is around Rs. 2.5 lakh per year. I belong to the OBC category.",
    "I am a 32-year-old man living in a city slum in Mumbai. I work as a plumber and earn about Rs. 12,000 per month. I am not registered anywhere formally. I have Aadhaar but no other documents.",
    "I am a 19-year-old woman from an ST tribe in Jharkhand. I want to start a small tailoring business. I have completed Class 10. My family is BPL. I have Aadhaar and a bank account.",
]

st.markdown("**Try an example:**")
cols = st.columns(len(EXAMPLES))
selected_example = None
for i, (col, ex) in enumerate(zip(cols, EXAMPLES)):
    with col:
        if st.button(f"Example {i+1}", key=f"ex_{i}"):
            selected_example = ex

# ─── Input Area ───────────────────────────────────────────────────────────────

default_text = selected_example if selected_example else st.session_state.get("last_input", "")
user_description = st.text_area(
    "Describe your situation in your own words:",
    value=default_text,
    height=130,
    placeholder="E.g. I am a 30-year-old woman from rural Uttar Pradesh. I belong to SC community. My husband is a farmer and we have 2 acres of land. Our annual income is Rs. 60,000. We cook on firewood and have no gas connection...",
    key="user_input",
)

col_btn, col_info = st.columns([1, 5])
with col_btn:
    run_button = st.button("🔍 Find My Schemes", type="primary", use_container_width=True)
with col_info:
    st.caption("Your description is processed by AI and not stored permanently.")

# ─── Pipeline Execution ───────────────────────────────────────────────────────

if run_button:
    if not user_description or len(user_description.strip()) < 10:
        st.warning("Please describe your situation in at least a few words.")
        st.stop()

    st.session_state["last_input"] = user_description

    # Progress display
    progress_placeholder = st.empty()
    status_placeholder = st.empty()

    steps = [
        ("🔍", "Retrieval Agent", "Searching scheme documents..."),
        ("⚖️", "Eligibility Agent", "Checking your eligibility against each scheme..."),
        ("📋", "Application Agent", "Preparing application guides..."),
        ("💬", "Explainer Agent", "Generating your personalised summary..."),
    ]

    with progress_placeholder.container():
        progress_bar = st.progress(0)
        for i, (icon, name, msg) in enumerate(steps):
            status_placeholder.info(f"{icon} **{name}:** {msg}")
            progress_bar.progress((i + 1) * 25)
            time.sleep(0.3)

    status_placeholder.info("⏳ Running the full pipeline — this may take 15–30 seconds...")

    try:
        response = httpx.post(
            f"{backend_url}/query",
            json={"description": user_description.strip()},
            timeout=120,
        )
        response.raise_for_status()
        data = response.json()
    except httpx.TimeoutException:
        progress_placeholder.empty()
        status_placeholder.empty()
        st.error("⏱️ The request timed out. Please try again or check if the backend is running.")
        st.stop()
    except Exception as e:
        progress_placeholder.empty()
        status_placeholder.empty()
        st.error(f"❌ Error contacting backend: {e}")
        st.stop()

    progress_placeholder.empty()
    status_placeholder.empty()

    # ─── Results ─────────────────────────────────────────────────────────────

    eligible_count = data.get("eligible_scheme_count", 0)

    if eligible_count > 0:
        st.success(f"✅ Found **{eligible_count} scheme(s)** you are likely eligible for!")
    else:
        st.warning("No clearly matching schemes found. See the summary below for next steps.")

    # ── Plain language summary ────────────────────────────────────────────────
    st.markdown("### 💬 Your Personalised Summary")
    st.markdown(
        f'<div class="summary-box">{data["plain_summary"].replace(chr(10), "<br>")}</div>',
        unsafe_allow_html=True,
    )

    # ── Eligible schemes with guides ─────────────────────────────────────────
    if data.get("application_guides"):
        st.markdown("### 📋 Eligible Schemes & How to Apply")

        for guide in data["application_guides"]:
            with st.expander(f"🟢 {guide['scheme_title']}", expanded=True):

                col1, col2 = st.columns([3, 1])
                with col1:
                    st.markdown(f'<div class="ministry-tag">📌 {guide["ministry"]}</div>', unsafe_allow_html=True)
                    if guide.get("notes"):
                        st.markdown(f"*{guide['notes']}*")
                with col2:
                    if guide.get("helpline"):
                        st.markdown(f'<div class="helpline-badge">📞 {guide["helpline"]}</div>', unsafe_allow_html=True)
                    if guide.get("estimated_time"):
                        st.caption(f"⏱️ Processing: {guide['estimated_time']}")

                tab_docs, tab_steps, tab_tips = st.tabs(
                    ["📄 Required Documents", "🪜 Application Steps", "💡 Tips for You"]
                )

                with tab_docs:
                    for doc in guide.get("required_documents", []):
                        st.markdown(f"- {doc}")

                with tab_steps:
                    for step in guide.get("application_steps", []):
                        st.markdown(f'<div class="step-item">▶ {step}</div>', unsafe_allow_html=True)
                    if guide.get("apply_url"):
                        st.markdown(f"🌐 **Apply at:** [{guide['apply_url']}]({guide['apply_url']})")

                with tab_tips:
                    if guide.get("tips"):
                        for tip in guide["tips"]:
                            st.markdown(f'<div class="tip-box">💡 {tip}</div>', unsafe_allow_html=True)
                    else:
                        st.info("No specific tips generated. Follow the application steps above.")

    # ── All eligibility results (expandable) ────────────────────────────────
    with st.expander("🔍 Full Eligibility Check Results (all evaluated schemes)"):
        for r in data.get("eligibility_results", []):
            badge = '<span class="badge-eligible">✅ Eligible</span>' if r["eligible"] else '<span class="badge-ineligible">❌ Not eligible</span>'
            st.markdown(
                f'**{r["scheme_title"]}** — {badge} &nbsp; *Confidence: {r["confidence"]}*',
                unsafe_allow_html=True,
            )
            if r.get("matched_criteria"):
                st.caption("Matched: " + "; ".join(r["matched_criteria"][:2]))
            if r.get("disqualifiers"):
                st.caption("Reason: " + "; ".join(r["disqualifiers"][:1]))
            st.markdown("---")

# ─── Footer ───────────────────────────────────────────────────────────────────

st.markdown("---")
st.caption(
    "⚠️ This tool provides AI-assisted guidance only. "
    "Always verify eligibility with the official scheme portal or your nearest CSC/Jan Seva Kendra. "
    "| Built with LangChain · LangGraph · ChromaDB · Streamlit"
)
