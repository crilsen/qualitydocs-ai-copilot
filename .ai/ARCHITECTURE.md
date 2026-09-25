# Architecture

## Components (MVP)

```text
[Next.js Frontend] ──REST/JSON──> [FastAPI Backend] ──> [SQLite via SQLAlchemy]
                                         │
                          ┌──────────────┼──────────────┐
                          │              │              │
                   [Extractor       [Prompt          [LLM Provider
                    PDF/DOCX]        Registry]        registry: anthropic
                    pypdf/           prompts/*.md     openai (GPT/Codex)
                    python-docx      versioned        gemini
                                     + Pydantic       compat (OpenCode/
                                     output schema   OpenRouter/Ollama)
                                                     local demo (no key)]
```

## Flow

1. Upload 2–5 docs (PDF/DOCX) → extraction (text, name, page/section, date) → list.
2. Select analysis mode + prompt version + provider.
3. Backend builds context (documents as DATA, never instructions) + system prompt → LLM provider (or local demo heuristic when no key).
4. Pydantic-validated JSON output (`executive_summary`, `findings[]` with evidence, `limitations`).
5. Human review (Pending/Accepted/Edited/Rejected + comment) → status summary.
6. Run history (prompt, model, latency, date).

## Security

- File type/size validation; no full-content logging; no exposed keys; friendly errors; basic prompt-injection defense (content as data, immutable system prompt, suspicious-text detection and logging).

## Local deploy

- `docker compose up --build` (backend :8000, frontend :3000). No cloud IaC; terraform/kubernetes/cloud-port workflows do not apply.
