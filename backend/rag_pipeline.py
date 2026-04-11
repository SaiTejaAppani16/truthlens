import os
import chromadb
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
import anthropic

load_dotenv()

client = anthropic.Anthropic()
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
chroma_client = chromadb.PersistentClient(path="chroma_db")
collection = chroma_client.get_or_create_collection(name="trusted_sources")


def load_trusted_sources(filepath: str):
    with open(filepath, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    existing = collection.get()
    if len(existing["ids"]) > 0:
        print("Sources already loaded.")
        return

    for i, line in enumerate(lines):
        embedding = embedding_model.encode(line).tolist()
        collection.add(
            documents=[line],
            embeddings=[embedding],
            ids=[f"doc_{i}"]
        )
    print(f"Loaded {len(lines)} trusted source chunks.")


def fact_check_claim(claim: str) -> dict:
    claim_embedding = embedding_model.encode(claim).tolist()

    results = collection.query(
        query_embeddings=[claim_embedding],
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

    import json
    response_text = message.content[0].text.strip()
    result = json.loads(response_text)
    result["evidence"] = evidence_chunks
    return result