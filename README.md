# TruthLens 🔍
**AI-Powered Misinformation Detector**

🌐 **Live Demo:** https://truthlens-frontend-5bg2.onrender.com

🔧 **API:** https://truthlens-siwz.onrender.com

---

In a world where fake news spreads faster than the truth, TruthLens helps you verify what you read. Paste any news article URL, raw text, or simply ask a question about current events — TruthLens extracts the key factual claims, checks each one against trusted sources using RAG, and returns a credibility score with full explanations.

---

## How It Works

**Mode 1 — Analyze an Article**

1. **Scrape** — BeautifulSoup extracts clean text from any news URL
2. **Extract** — Claude API identifies 5-8 key factual claims
3. **Retrieve** — Each claim is embedded and searched against ChromaDB trusted sources
4. **Verify** — Claude compares each claim against retrieved evidence
5. **Score** — A credibility score (0-100) is calculated and displayed

**Mode 2 — Ask a Question**

1. **Search** — NewsAPI finds the 3 most relevant current articles
2. **Scrape** — Each article is scraped and cleaned automatically
3. **Extract** — Claude API identifies key factual claims from the articles
4. **Retrieve** — Claims checked against ChromaDB trusted sources
5. **Verify** — Claude compares claims against evidence
6. **Score** — Credibility score returned with full claim-by-claim breakdown

---

## Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| Language | Python 3.11 | Core development |
| Backend API | FastAPI | REST API server |
| LLM | Anthropic Claude API | Claim extraction and verification |
| Vector Database | ChromaDB | Store and search trusted source embeddings |
| News Search | NewsAPI | Find relevant current articles by question |
| Web Scraping | BeautifulSoup4 | Extract article text from URLs |
| Frontend | Streamlit | User interface |
| Deployment | Render | Live public hosting |

---

## Project Structure

```
truthlens/
├── backend/
│   ├── main.py              # FastAPI app — orchestrates the pipeline
│   ├── scraper.py           # Fetches and cleans article text
│   ├── claim_extractor.py   # Extracts factual claims using Claude
│   ├── rag_pipeline.py      # ChromaDB retrieval and verification
│   ├── scorer.py            # Calculates final credibility score
│   └── news_search.py       # NewsAPI integration for question mode
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
ANTHROPIC_API_KEY=your_anthropic_key
NEWS_API_KEY=your_newsapi_key
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

## Key Design Decisions

Every technical choice in this project was deliberate. See [DECISIONS.md](DECISIONS.md) for the full reasoning behind each one.

---

*Built by Sai Teja Appani*
*MS Computer Science — University of Florida*
*Herbert Wertheim College of Engineering*