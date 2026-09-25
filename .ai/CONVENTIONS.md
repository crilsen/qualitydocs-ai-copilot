# Conventions

## Observed (project)

- Language: conversation with user in PT-BR; ALL project files in English (code, UI, docs, commits, .ai/). Decided 2026-09-25, overrides earlier PT requirement for files.
- Backend: FastAPI with `documents`, `analyses`, `reviews`, `governance` routers; Pydantic schemas; snake_case filenames.
- Versioned prompts in `prompts/*.md` with front-matter (`version`, `mode`); version selected in UI and recorded per run.
- Frontend: Next.js App Router + TypeScript + Tailwind; English pages: dashboard, upload, analysis, results, history, review, governance.
- Synthetic data only via `backend/app/seed.py`; never real data.
- Never use the term "enterprise".
- Short logical commits in English; initial release `v0.1.0`.

## Documentation

- English README with problem, architecture, flow, local run, provider setup, limitations, screenshot placeholders, and Prompt/Context Engineering, governance, and human-review sections + Mermaid diagram.
- `.ai/` in Automatic mode: primary agent updates TASKS/HANDOFF/LEARNINGS; promote durable learnings.
