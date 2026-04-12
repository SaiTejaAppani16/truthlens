from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from backend.scraper import scrape_article
from backend.claim_extractor import extract_claims
from backend.rag_pipeline import load_trusted_sources, fact_check_claim
from backend.scorer import score_article

app = FastAPI(title="TruthLens API")

load_trusted_sources("data/trusted_sources/sample.txt")


class AnalyzeRequest(BaseModel):
    url: str = None
    text: str = None


@app.get("/")
def root():
    return {"message": "TruthLens API is running"}


@app.post("/analyze")
def analyze(request: AnalyzeRequest):
    if not request.url and not request.text:
        raise HTTPException(
            status_code=400,
            detail="Provide either a URL or text"
        )

    if request.url:
        article_text = scrape_article(request.url)
    else:
        article_text = request.text

    claims = extract_claims(article_text)
    result = score_article(claims)

    return result