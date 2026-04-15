# TruthLens 🔍
**AI-Powered Misinformation Detector**

🌐 **Live Demo:** https://truthlens-frontend-5bg2.onrender.com

🔧 **API:** https://truthlens-siwz.onrender.com
In a world where fake news spreads faster than the truth, TruthLens helps you verify what you read. Paste any news article URL or raw text and TruthLens will extract the key factual claims, check each one against trusted sources, and return a credibility score with full explanations — not just a black-box verdict.

---

## What Makes TruthLens Different

Most AI fact-checkers simply ask an LLM "is this true?" and trust its memory. TruthLens doesn't do that.

Instead, it uses **Retrieval-Augmented Generation (RAG)** — it first retrieves real evidence from a trusted source database, then asks the LLM to reason on top of that evidence. This prevents hallucination and grounds every verdict in actual sources.

When there isn't enough evidence to make a call, TruthLens explicitly says so — rather than making something up.

---

## How It Works

```
User Input (URL or Text)
        ↓
  Scrape & Clean Article        ← BeautifulSoup
        ↓
  Extract Factual Claims        ← Claude API
        ↓
  Embed & Search ChromaDB       ← sentence-transformers
        ↓
  Retrieve Trusted Evidence     ← Reuters, AP News, Wikipedia
        ↓
  Compare Claim vs Evidence     ← Claude API
        ↓
  Calculate Credibility Score   ← 0 to 100
        ↓
  Display Results in UI         ← Streamlit
```

---

## Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| Language | Python 3.11 | Core development |
| Backend | FastAPI | REST API server |
| LLM | Anthropic Claude API | Claim extraction and verification |
| Vector Database | ChromaDB | Store and search trusted source embeddings |
| Embeddings | sentence-transformers | Convert text to vectors |
| Scraping | BeautifulSoup4 | Extract article text from URLs |
| Frontend | Streamlit | User interface |

---

## Project Structure

```
truthlens/
├── backend/
│   ├── main.py              # FastAPI app — orchestrates the pipeline
│   ├── scraper.py           # Fetches and cleans article text
│   ├── claim_extractor.py   # Extracts factual claims using Claude
│   ├── rag_pipeline.py      # ChromaDB retrieval and verification
│   └── scorer.py            # Calculates final credibility score
├── frontend/
│   └── app.py               # Streamlit UI
├── data/
│   └── trusted_sources/     # Trusted source knowledge base
├── DECISIONS.md             # Architectural decision log
└── requirements.txt
```

---

## Running Locally

**1. Clone the repository**
```bash
git clone git@github.com:SaiTejaAppani16/truthlens.git
cd truthlens
```

**2. Set up virtual environment**
```bash
python3.11 -m venv venv
source venv/bin/activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Configure environment**

Create a `.env` file in the root directory:
```
ANTHROPIC_API_KEY=your_key_here
```

**5. Start the backend**
```bash
uvicorn backend.main:app --reload
```

**6. Start the frontend**
```bash
streamlit run frontend/app.py
```

Open your browser at `http://localhost:8501`

---

## Credibility Scoring

| Score | Verdict | Meaning |
|---|---|---|
| 70 - 100 | ✅ Credible | Most claims supported by evidence |
| 40 - 69 | ⚠️ Suspicious | Mixed or weak evidence |
| 0 - 39 | ❌ Misleading | Claims contradict or lack evidence |

---

## Architectural Decisions

Every technical choice in this project was deliberate. See [DECISIONS.md](DECISIONS.md) for the full reasoning behind each one.

---

*Built by Sai Teja Appani*
*MS Computer Science — University of Florida*
*Herbert Wertheim College of Engineering*
