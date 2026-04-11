import anthropic
import json
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic()


def extract_claims(article_text: str) -> list[str]:
    prompt = f"""You are a fact-checking assistant. Read the following news article and extract the 5-8 most important factual claims that can be verified.

A factual claim is a specific, concrete statement that can be checked against evidence. For example:
- "The unemployment rate rose to 4.2% in March"
- "The president signed the bill into law on Tuesday"

Do NOT include opinions, predictions, or vague statements.

Return your response as a JSON array of strings. Nothing else. No explanation. Just the JSON array.

Article:
{article_text[:3000]}

JSON array of claims:"""

    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    response_text = message.content[0].text.strip()
    claims = json.loads(response_text)
    return claims