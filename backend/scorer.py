from backend.rag_pipeline import fact_check_claim


def score_article(claims: list[str]) -> dict:
    results = []

    for claim in claims:
        result = fact_check_claim(claim)
        results.append({
            "claim": claim,
            "verdict": result["verdict"],
            "confidence": result["confidence"],
            "explanation": result["explanation"],
            "evidence": result["evidence"]
        })

    supported = [r for r in results if r["verdict"] == "SUPPORTED"]
    contradicted = [r for r in results if r["verdict"] == "CONTRADICTED"]
    insufficient = [r for r in results if r["verdict"] == "INSUFFICIENT EVIDENCE"]

    total = len(results)
    score = round((len(supported) / total) * 100) if total > 0 else 0

    if score >= 70:
        verdict = "CREDIBLE"
    elif score >= 40:
        verdict = "SUSPICIOUS"
    else:
        verdict = "MISLEADING"

    return {
        "overall_score": score,
        "overall_verdict": verdict,
        "total_claims": total,
        "supported": len(supported),
        "contradicted": len(contradicted),
        "insufficient": len(insufficient),
        "claim_results": results
    }