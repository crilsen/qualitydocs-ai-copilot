# Decision Records

Mode: Simple (inline up to ~15–20 records).

## Index

| ID | Type | Title | Status | Date |
| --- | --- | --- | --- | --- |
| ADR-001 | ADR | Modular FastAPI monolith + Next.js over REST, local SQLite | Accepted | 2026-09-25 |
| TDR-001 | TDR | Abstract LLM provider with Anthropic first, keyless local stub | Accepted | 2026-09-25 |
| ADR-002 | ADR | Versioned prompts in Markdown files, not in code | Accepted | 2026-09-25 |
| TDR-002 | TDR | PDF extraction with pypdf and DOCX with python-docx | Accepted | 2026-09-25 |
| ADR-003 | ADR | Human review per finding with status + comment, never self-approval | Accepted | 2026-09-25 |
| TDR-003 | TDR | Multi-provider LLM: Anthropic + OpenAI + Gemini + OpenAI-compat + local, per-run selection | Accepted | 2026-09-25 |

## Records

### ADR-001 — Modular FastAPI monolith + Next.js over REST, local SQLite
Type: ADR | Status: Accepted | Date: 2026-09-25 | Owners: user + agent
Context: Portfolio MVP must run with `docker compose up`, no cloud.
Decision: Modular FastAPI backend, Next.js frontend, SQLite via SQLAlchemy, REST/JSON communication.
Consequences: Simplicity and local demo; no multi-user/auth in MVP.

### TDR-001 — Abstract LLM provider with Anthropic first, keyless local stub
Type: TDR | Status: Accepted | Date: 2026-09-25 | Owners: user + agent
Context: Real keys cannot be committed; demo must work without a key.
Decision: `LLMProvider` interface + `AnthropicProvider` + `LocalDemoProvider` (heuristic, same Pydantic schema).
Consequences: Offline demo works; switching to OpenAI/Gemini later without changing routes.

### ADR-002 — Versioned prompts in Markdown files
Type: ADR | Status: Proposed | Date: 2026-09-25 | Owners: user + agent
Context: Demonstrating Prompt Engineering requires auditable, selectable prompts.
Decision: `prompts/*.md` with version front-matter; UI selects version; run records prompt/model/latency.
Consequences: Full prompt→response traceability.

### TDR-002 — PDF/DOCX extraction
Type: TDR | Status: Accepted | Date: 2026-09-25
Context: Upload 2–5 PDF/DOCX files with page/section.
Decision: `pypdf` for PDF, `python-docx` for DOCX.
Consequences: No OCR in MVP (scanned PDFs return a friendly warning).

### TDR-003 — Multi-provider LLM with per-run selection
Type: TDR | Status: Accepted | Date: 2026-09-25 | Owners: user + agent
Context: User asked for the app to support Codex (OpenAI), OpenCode, and Gemini beyond the initial Anthropic.
Decision: `PROVIDERS` registry in `app/services/llm.py` with anthropic/openai/gemini/compat/local ids; `GET /api/providers` exposes availability; `RunAnalysisRequest.provider` (auto default, cloud first, local last); friendly 400 error naming the missing env var; compat provider covers OpenCode gateway/OpenRouter/Ollama/vLLM with non-strict-JSON retry. Pydantic raised to 2.13.5 (required by google-genai).
Consequences: Model switching without route changes; offline demo still works keyless.

### ADR-003 — Human review per finding
Type: ADR | Status: Accepted | Date: 2026-09-25
Context: Governance requires human validation before any decision.
Decision: Pending/Accepted/Edited/Rejected status + comment + title/description/action editing; aggregate summary.
Consequences: No conclusion without evidence is shown as validated.
