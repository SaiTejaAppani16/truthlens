# Architectural Decision Log — TruthLens

When I built TruthLens, every technical choice was deliberate. This
document explains what I chose, what I considered, and the reasoning
behind each decision. I wrote this because I believe good engineers
don't just build things — they understand why they built them that way.

---

## 1. Why RAG instead of just asking the LLM?

This was the most important decision in the entire project.

The naive approach would be to take a news claim and ask Claude
"is this true?" It's simple, fast, and completely unreliable.
LLMs hallucinate. They predict patterns from training data and
sometimes confidently state things that are wrong. For a
misinformation detector, that's unacceptable.

RAG solves this by separating retrieval from reasoning. Instead
of trusting the LLM's memory, I first retrieve real evidence from
a trusted source database, then give that evidence to the LLM and
ask it to reason on top of it. The LLM becomes an analyst, not
a memory bank.

There's also a critical edge case I wanted to handle correctly:
what happens when there's not enough evidence? A naive LLM will
make something up. TruthLens explicitly returns "INSUFFICIENT
EVIDENCE" instead of guessing. That's a production-grade behavior
that most student projects ignore.

---

## 2. Why Anthropic Claude instead of OpenAI GPT?

I evaluated both. Claude and GPT-4o-mini are both strong at
reasoning and instruction following — the two things TruthLens
needs most for claim extraction and evidence comparison.

The deciding factor was practical. As an international student
building a portfolio project, I needed to manage costs carefully.
Anthropic provided free credits that covered the entire development
and testing phase. Beyond cost, Claude's responses to structured
prompts — especially JSON output — were clean and consistent,
which made parsing the responses straightforward.

---

## 3. Why ChromaDB instead of Pinecone?

Pinecone is excellent. It's a managed cloud vector database with
a polished API and great documentation. I seriously considered it.

The problem is cost. Pinecone requires a paid plan for anything
beyond a small hobby tier, and it introduces a network dependency
— my app would break if Pinecone had downtime.

ChromaDB runs locally. It's open source, has zero cost, persists
data to disk, and integrates with Python in a few lines. For a
portfolio project that needs to be deployable, demonstrable, and
cost-free to run, ChromaDB was the right call. If TruthLens were
scaling to millions of documents, I would revisit Pinecone.

---

## 4. Why sentence-transformers instead of OpenAI Embeddings?

Every claim and every trusted source chunk needs to be converted
into a vector embedding. If I used OpenAI's embedding API, every
single analysis would make paid API calls just for embeddings —
on top of the Claude API calls already happening.

The sentence-transformers library runs entirely locally. The
all-MiniLM-L6-v2 model is fast, lightweight, and produces
high quality semantic embeddings. It costs nothing per call
and has no external dependency. For a system where embeddings
happen on every request, local inference was the clear choice.

---

## 5. Why FastAPI instead of Flask?

Flask is simple and I could have used it. But FastAPI offers
something Flask doesn't out of the box — automatic interactive
API documentation at /docs. The moment you run the server,
you get a fully functional interface to test every endpoint
without writing a single line of extra code.

FastAPI also enforces type hints through Pydantic. This means
if the frontend sends a malformed request, FastAPI catches it
immediately and returns a clear error — rather than letting
bad data flow into the pipeline and cause a confusing crash
somewhere downstream. For a production-minded project, that
kind of input validation matters.

---

## 6. Why Streamlit instead of React?

I want to be honest here. I could have built a React frontend.
But that would have been the wrong decision for this project.

TruthLens is an AI engineering project. Its value is in the
RAG pipeline, the LLM integration, and the system design — not
in the frontend. Spending three weeks building a React UI would
have pulled focus away from the parts that actually demonstrate
AI/ML engineering skills.

Streamlit let me build a clean, functional, and professional
UI in pure Python in a single day. That freed me to spend the
remaining time deepening the AI pipeline, improving the scoring
logic, and documenting my decisions properly. For this project,
that was the right tradeoff.

---

## 7. Why build RAG from scratch instead of using LangChain?

This is the decision I'm most proud of.

LangChain is a popular framework that wraps RAG into a few
lines of code. I could have used it and shipped faster. But
I would not have understood what my own project was doing —
and that matters enormously in interviews.

By building RAG manually — chunking text, generating embeddings,
storing vectors in ChromaDB, querying by similarity, formatting
prompts, parsing responses — I understand every single step.
When an interviewer asks me "how does your RAG pipeline work?"
I can explain it precisely, down to why I chose cosine similarity
and what happens when the top-k results are all low confidence.

LangChain is a tool. Understanding the problem it solves is
the skill. I chose to learn the skill first.

---

*Sai Teja Appani*
*MS Computer Science — University of Florida*
*Herbert Wertheim College of Engineering*
