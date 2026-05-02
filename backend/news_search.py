import requests
import os
from dotenv import load_dotenv
from backend.scraper import scrape_article

load_dotenv()

NEWS_API_KEY = os.getenv("NEWS_API_KEY")


def search_news(query: str) -> list[str]:
    url = "https://newsapi.org/v2/everything"
    params = {
        "q": query,
        "apiKey": NEWS_API_KEY,
        "language": "en",
        "sortBy": "relevancy",
        "pageSize": 3
    }

    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()

    articles = data.get("articles", [])
    texts = []

    for article in articles:
        url = article.get("url")
        if not url:
            continue
        try:
            text = scrape_article(url)
            texts.append(text[:3000])
        except Exception as e:
            print(f"Failed to scrape {url}: {e}")
            continue

    return texts