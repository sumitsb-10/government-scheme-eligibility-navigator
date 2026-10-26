# 🏛️ Government Scheme Eligibility Navigator

> A citizen-facing multi-agent AI assistant that helps people discover and apply for Indian government welfare schemes — in plain language.

---

## 📐 Architecture

```
User Description (plain text)
        │
        ▼
┌───────────────────┐
│  Retrieval Agent  │  RAG over ChromaDB — finds relevant scheme docs
└────────┬──────────┘
         │  top-k scheme chunks
         ▼
┌───────────────────┐
│ Eligibility Agent │  LLM evaluates user vs each scheme's criteria
└────────┬──────────┘
         │  eligible/ineligible + reasons
         ▼
┌───────────────────┐
│ Application Agent │  Extracts required docs + step-by-step guide
└────────┬──────────┘
         │  structured application guides
         ▼
┌───────────────────┐
│  Explainer Agent  │  Produces plain-language citizen summary
└────────┬──────────┘
         │
         ▼
   Streamlit UI / FastAPI
```

Orchestrated by **LangGraph** — each agent is a node in a directed acyclic graph.

---

## 🛠️ Technology Stack

| Layer | Technology |
|---|---|
| Frontend | Streamlit |
| Backend API | FastAPI + Uvicorn |
| LLM | Google Gemini 3.5 Flash (free tier) / Groq LLaMA 3 |
| Embeddings | Google `embedding-001` / Sentence Transformers |
| Vector DB | ChromaDB (local persistence) |
| Orchestration | LangGraph + LangChain |
| Data | 15 real Indian government scheme documents |

---

## 📁 Project Structure

```
Government Scheme Eligibility Navigator/
├── config.py                  # Central config (reads .env)
├── requirements.txt
├── .env.example               # Copy to .env and fill your keys
│
├── data/
│   ├── sample_schemes.py      # 14 pre-loaded scheme documents
│   └── scheme_docs/           # Drop real PDFs/DOCXs here
│
├── ingestion/
│   └── ingest.py              # Load docs → split → embed → ChromaDB
│
├── agents/
│   ├── llm_factory.py         # LLM provider abstraction (Gemini / Groq)
│   ├── vector_store.py        # ChromaDB singleton + retriever
│   ├── retrieval_agent.py     # Agent 1: RAG retrieval
│   ├── eligibility_agent.py   # Agent 2: Eligibility evaluation
│   ├── application_agent.py   # Agent 3: Application guides
│   ├── explainer_agent.py     # Agent 4: Plain-language summary
│   └── pipeline.py            # LangGraph orchestration
│
├── backend/
│   ├── main.py                # FastAPI app
│   └── models.py              # Pydantic request/response models
│
├── frontend/
│   └── app.py                 # Streamlit citizen UI
│
└── tests/
    └── test_pipeline.py       # Unit tests (pytest)
```

---

## 🚀 Quick Start

### 1. Clone & create virtual environment

```bash
git clone <your-repo>
cd "Government Scheme Eligibility Navigator"
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

> For Groq users, also install: `pip install sentence-transformers`

### 3. Configure your API key

```bash
copy .env.example .env       # Windows
# cp .env.example .env       # macOS/Linux
```

Edit `.env`:

```env
LLM_PROVIDER=gemini
GEMINI_MODEL=gemini-3.5-flash
GOOGLE_API_KEY=your_key_here   # Get free key at aistudio.google.com
```

**Or use Groq (also free):**

```env
LLM_PROVIDER=groq
GROQ_API_KEY=your_key_here     # Get free key at console.groq.com
```

### 4. Ingest scheme documents into ChromaDB

```bash
python ingestion/ingest.py
```

This embeds all 15 sample schemes into ChromaDB. Re-run whenever you add new PDFs.

### 5. Start the FastAPI backend

```bash
uvicorn backend.main:app --reload --port 8000
```

API docs available at: http://localhost:8000/docs

### 6. Start the Streamlit frontend

```bash
streamlit run frontend/app.py
```

Open: http://localhost:8501

---

## 🧪 Running Tests

```bash
pytest tests/ -v
```

---

## 📋 Covered Schemes (15)

| Scheme | Category |
|---|---|
| PM-KISAN | Farmer income support |
| Ayushman Bharat PM-JAY | Health insurance |
| PMAY-Gramin | Rural housing |
| National Scholarship Portal | Education |
| PM MUDRA Yojana | Business loans |
| Ujjwala Yojana 2.0 | Free LPG connection |
| MGNREGS | Rural employment (100 days) |
| Sukanya Samriddhi Yojana | Girl child savings |
| Stand-Up India | SC/ST & women entrepreneurs |
| Atal Pension Yojana | Unorganised sector pension |
| PM Fasal Bima Yojana | Crop insurance |
| PM Gram Sadak Yojana | Rural road connectivity |
| e-Shram Portal | Unorganised worker registration |
| PM Vaya Vandana Yojana | Senior citizen pension |
| Beti Bachao Beti Padhao | Girl child welfare |

---

## ➕ Adding More Schemes

**Option A — Add to sample_schemes.py:**
Add a new dict entry to `SAMPLE_SCHEMES` in `data/sample_schemes.py` and re-run `python ingestion/ingest.py`.

**Option B — Drop PDF/DOCX files:**
Place any government scheme PDF or Word document in `data/scheme_docs/` and re-run `python ingestion/ingest.py`.

---

## 📡 API Reference

### `POST /query`
Run the full pipeline.

```json
{
  "description": "I am a 30-year-old woman from rural Rajasthan, SC category, BPL family, no LPG connection..."
}
```

**Response:** eligible schemes + documents + steps + plain summary.

### `GET /health`
Liveness check + indexed chunk count.

### `GET /schemes`
List all indexed schemes.

### `POST /ingest`
Trigger background re-ingestion.

---

## 🧠 Learning Objectives

This project teaches:
- **RAG (Retrieval-Augmented Generation):** ChromaDB + LangChain retrievers
- **LLM Chaining:** LangChain prompts, parsers, chains
- **Multi-Agent Systems:** LangGraph StateGraph with typed state
- **Embeddings & Vector Search:** Semantic similarity over documents
- **FastAPI:** REST API design with Pydantic models
- **Streamlit:** Rapid prototyping of AI-powered UIs

---

## ⚠️ Disclaimer

This tool provides AI-assisted guidance only. Always verify eligibility at official government portals or your nearest Common Service Centre (CSC / Jan Seva Kendra).
