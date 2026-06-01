import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from backend.scraper import scrape_article
from backend.claim_extractor import extract_claims
from backend.rag_pipeline import load_trusted_sources, fact_check_claim
from backend.scorer import score_article
from backend.news_search import search_news
import anthropic

app = FastAPI(title="TruthLens API")

load_trusted_sources("data/trusted_sources/sample.txt")

client = anthropic.Anthropic()


class AnalyzeRequest(BaseModel):
    url: str = None
    text: str = None


class QuestionRequest(BaseModel):
    question: str


def clean_input(text: str) -> str:
    """Fix spelling mistakes and grammar errors in user input using Claude."""
    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=256,
        messages=[{
            "role": "user",
            "content": f"""Fix any spelling mistakes and grammar errors in this text.
Return ONLY the corrected text with no explanation, no quotes, nothing else.
If the text is already correct, return it as-is.

Text: {text}"""
        }]
    )
    return message.content[0].text.strip()


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
        cleaned_text = clean_input(request.text)
        article_text = cleaned_text

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

    cleaned_question = clean_input(request.question)
    texts = search_news(cleaned_question)

    if not texts:
        raise HTTPException(
            status_code=404,
            detail="No relevant news articles found"
        )

    combined_text = " ".join(texts)
    claims = extract_claims(combined_text)
    result = score_article(claims)
    result["question"] = cleaned_question

    return result


if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("backend.main:app", host="0.0.0.0", port=port)