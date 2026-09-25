# Project

## Identity

- **Name:** Document Quality AI Copilot (qualitydocs-ai-copilot)
- **Objective:** Web app to consolidate, compare, and validate quality documents with generative AI, demonstrating Prompt Engineering, Context Engineering, traceability, human review, and basic governance.
- **Status:** MVP v0.1.0 released; multi-provider LLM support on main (unreleased). Portfolio project, synthetic data only.
- **Language:** All project files in English; conversation with user in PT-BR.

## Stack (observed from approved scope)

- Backend: Python 3.12 + FastAPI + SQLAlchemy (local SQLite) + Pydantic
- Frontend: Next.js + TypeScript + Tailwind CSS
- Processing: PDF (pypdf) and DOCX (python-docx)
- LLM: abstract provider layer — Anthropic Claude, OpenAI (GPT/Codex), Google Gemini, OpenAI-compatible endpoints, offline local demo
- Containers: Docker Compose
- Config: `.env.example`, no real credentials

## Analysis modes

executive summary, document/version comparison, missing items, divergences and inconsistencies, risks and nonconformities, suggested action plan.

## Principles

- Synthetic example data only; no real/confidential data.
- Demonstrable MVP, no excessive features.
- Never use the term "enterprise" in the project.
- Durable context: Automatic mode (keep .ai/ current as work happens, no need to ask again). Recorded in HANDOFF.
