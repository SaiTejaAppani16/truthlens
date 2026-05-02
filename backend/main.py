import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from backend.scraper import scrape_article
from backend.claim_extractor import extract_claims
from backend.rag_pipeline import load_trusted_sources, fact_check_claim
from backend.scorer import score_article
from backend.news_search import search_news

app = FastAPI(title="TruthLens API")

load_trusted_sources("data/trusted_sources/sample.txt")


class AnalyzeRequest(BaseModel):
    url: str = None
    text: str = None


class QuestionRequest(BaseModel):
    question: str


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


@app.post("/question")
def question(request: QuestionRequest):
    if not request.question:
        raise HTTPException(
            status_code=400,
            detail="Provide a question"
        )

    texts = search_news(request.question)

    if not texts:
        raise HTTPException(
            status_code=404,
            detail="No relevant news articles found"
        )

    combined_text = " ".join(texts)
    claims = extract_claims(combined_text)
    result = score_article(claims)
    result["question"] = request.question

    return result


if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("backend.main:app", host="0.0.0.0", port=port)