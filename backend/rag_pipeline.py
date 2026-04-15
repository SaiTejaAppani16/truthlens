import os
import chromadb
from chromadb.utils import embedding_functions
from dotenv import load_dotenv
import anthropic
import json

load_dotenv()

client = anthropic.Anthropic()
chroma_client = chromadb.PersistentClient(path="chroma_db")
embedding_fn = embedding_functions.DefaultEmbeddingFunction()
collection = chroma_client.get_or_create_collection(
    name="trusted_sources",
    embedding_function=embedding_fn
)


def load_trusted_sources(filepath: str):
    with open(filepath, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    existing = collection.get()
    if len(existing["ids"]) > 0:
        print("Sources already loaded.")
        return

    for i, line in enumerate(lines):
        collection.add(
            documents=[line],
            ids=[f"doc_{i}"]
        )
    print(f"Loaded {len(lines)} trusted source chunks.")


def fact_check_claim(claim: str) -> dict:
    results = collection.query(
        query_texts=[claim],
        n_results=3
    )

    evidence_chunks = results["documents"][0]
    evidence_text = "\n".join(evidence_chunks)

    prompt = f"""You are a fact-checking assistant.

Claim to verify: {claim}

Evidence from trusted sources:
{evidence_text}

Based ONLY on the evidence provided above, evaluate the claim.
Respond in this exact JSON format:
{{
    "verdict": "SUPPORTED" or "CONTRADICTED" or "INSUFFICIENT EVIDENCE",
    "confidence": a number from 0 to 100,
    "explanation": "one sentence explaining your verdict"
}}

JSON response:"""

    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=512,
        messages=[{"role": "user", "content": prompt}]
    )

    response_text = message.content[0].text.strip()
    result = json.loads(response_text)
    result["evidence"] = evidence_chunks
    return result