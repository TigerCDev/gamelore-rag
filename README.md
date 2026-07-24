```markdown
# gamelore-rag

> A RAG system for deep narrative analysis of story-driven games — hybrid structured + vector retrieval, built on Django, DRF, pgvector, and LangChain.

## Stack

- Django + DRF
- PostgreSQL + pgvector
- LangChain + OpenAI (embeddings) + Groq (LLM)
- Celery + Redis (async ingestion)
- Docker → Fly.io (deploy in progress)

## Status

🚧 In active development — core RAG loop complete, deploy prep underway

## What this is

A hybrid retrieval system that answers two kinds of questions about story-driven games:

- **Factual questions** ("Who developed Expedition 33?") → routed to PostgreSQL via Django ORM
- **Narrative questions** ("What does the Maelle ending represent?") → routed to pgvector semantic search → LLM synthesis with citations

A keyword router classifies incoming questions and sends them down the correct path — no wasted LLM calls on questions the database can already answer.

## Corpus

Full multi-source ingestion (Wikipedia + developer interview transcripts):

- Clair Obscur: Expedition 33
- The Last of Us
- God of War (2018) / God of War Ragnarok

12 games loaded structurally via IGDB; corpus expansion (Red Dead Redemption 2, Uncharted, Beyond: Two Souls) is a documented next step.

## Eval Harness

20 hand-written domain-expert questions with known-good answers, measuring retrieval precision via keyword overlap. Used to tune retrieval parameters before deploying.

**Top-k tuning results:**

| top-k | retrieval score | gain vs previous |
|---|---|---|
| 3 | 0.38 | — |
| 5 | 0.45 | +0.07 |
| 8 | 0.50 | +0.05 |
| 12 | 0.55 | +0.05 |
| 15 | 0.56 | +0.01 |

**Decision:** k=8 selected for production. Captures the majority of retrieval gain while avoiding the token cost and context dilution of retrieving 12-15 chunks per query for marginal improvement.

## Architecture

```
User question
    → /ask endpoint (Django DRF)
    → Query router (classify: factual vs narrative)
    → [Factual path]   Django ORM → structured result
    → [Narrative path] Embed question → pgvector cosine similarity → top-8 chunks
                       → Prompt construction (context + question)
                       → LLM call (Groq, llama-3.1-8b-instant)
                       → Response with citations
```

Async ingestion runs through Celery + Redis, decoupled from the query API — fetching, chunking, and embedding new sources never blocks `/ask`.

## Tests

14 pytest tests covering the router, retrieval, `/ask` endpoint (LLM and embeddings mocked), and edge cases.

## Run locally

```
git clone https://github.com/TigerCDev/gamelore-rag.git
cd gamelore-rag
docker compose up --build
```

## What's next

- Streaming responses via `StreamingHttpResponse`
- JWT auth + rate limiting
- Fly.io deployment
- Corpus expansion to remaining catalog
```