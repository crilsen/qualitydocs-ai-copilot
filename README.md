# Document Quality AI Copilot

Web app to consolidate, compare, and validate quality documents with generative AI. Portfolio MVP using **synthetic demo data only** — no real or confidential data.

> AI-generated results must be reviewed before any decision.

## Problem

Quality teams juggle procedures, specifications, and nonconformity reports across versions. Manual cross-checking is slow and misses divergences, missing items, and overdue actions. This MVP shows how Prompt Engineering, Context Engineering, structured output, traceability, human review, and basic AI governance fit together in one demonstrable flow.

## Architecture

```mermaid
flowchart LR
    UI[Next.js UI] -->|REST JSON| API[FastAPI]
    API --> DB[(SQLite)]
    API --> EXT[PDF/DOCX extractor]
    API --> PR[Versioned prompts\nprompts/*.md]
    API --> GUARD[Injection guard\ndata-only wrapping]
    API --> LLM{LLM provider}
    LLM -->|key present| CLAUDE[Anthropic Claude]
    LLM -->|no key| LOCAL[Local demo analyzer]
    LLM --> OUT[Pydantic JSON:\nsummary + findings + evidence]
    OUT --> REV[Human review\nAccept/Edit/Reject]
```

## Flow

1. Upload 2–5 PDF/DOCX → text extraction (name, page/section, date) → list.
2. Pick analysis mode + prompt version → system prompt + documents-as-data → provider.
3. Validated JSON (Pydantic): `executive_summary`, `findings[]` (each with evidence), `limitations`. Findings without evidence are withheld.
4. Results table with severity/category filters; evidence excerpt per finding.
5. Human review per finding (Pending/Accepted/Edited/Rejected + comment) with summary counts.
6. History of runs (prompt, model, latency, date) + Governance page.

## Quickstart

```bash
cp .env.example .env            # add ANTHROPIC_API_KEY to use Claude; without it, offline demo runs
docker compose up --build
# UI: http://localhost:3000  API: http://localhost:8000  Health: http://localhost:8000/api/health
```

Local dev:

```bash
cd backend && pip install -r requirements.txt && python -m app.seed && uvicorn app.main:app --reload
cd frontend && npm install && npm run dev
```

## Anthropic API setup

1. Get a key at console.anthropic.com (never commit it).
2. Put `ANTHROPIC_API_KEY=...` in `.env`, optionally set `ANTHROPIC_MODEL` and `LLM_PROVIDER=anthropic`.
3. Restart the backend. Runs record model + latency; without a key the offline demo provider is used automatically.

## Analysis modes

Executive Summary · Document/Version Comparison · Missing Items · Divergences & Inconsistencies · Risks & Nonconformities · Suggested Action Plan

## How this demonstrates the skills

- **Prompt Engineering:** versioned system prompts in `prompts/*.md` (answer-only-from-documents, cite source/page, declare uncertainty, never invent, strict JSON, injection resistance); prompt version selectable in UI and stored per run.
- **Context Engineering:** documents wrapped as delimited DATA with section labels; clipping limits; injection scan with flag + log note; system prompt immune to document text.
- **Governance:** Governance page (human validation required, allowed/prohibited data, AI limits) + persistent banner + `/api/governance`.
- **Human review:** per-finding status, reviewer comment, field edits, aggregate counts.

## Evaluation

```bash
cd backend && pip install -r requirements.txt
python evaluation/run_evaluation.py --output evaluation/report.md
```

Scores: citation presence, JSON adherence, findings without evidence (must be 0), latency, cost estimate (local = $0). See `evaluation/questions.json`.

## Tests

```bash
cd backend && pip install -r requirements.txt && pytest -q
```

## Screenshots

- `docs/screenshots/dashboard.png` — placeholder
- `docs/screenshots/results.png` — placeholder
- `docs/screenshots/review.png` — placeholder

## Known limitations

- No OCR (scanned PDFs return a friendly error); 15 MB / PDF-DOCX-only validation.
- SQLite local; no multi-user auth in MVP.
- Offline demo provider is heuristic; real depth requires an Anthropic key.
- Full document content is never logged; API keys never exposed to the frontend.

## Project layout

```
prompts/          versioned system prompts (6 modes)
backend/          FastAPI + SQLAlchemy + Pydantic + providers + tests
frontend/         Next.js + TypeScript + Tailwind (7 screens)
evaluation/       questions + runner + report
```

## License

MIT — synthetic demo data only.
