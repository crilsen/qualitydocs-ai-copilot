# Session Handoff

## Resume block (read first)

- Repo state: branch `main`, 3 commits, HEAD at docs commit, working tree clean, pushed to origin + tag v0.1.0 + GitHub release
- Source of truth: `AGENTS.md` → `.ai/`
- Budget / usage observed: unknown
- Checkpoint updated: 2026-09-25
- Last goal: Build MVP v0.1.0 and publish first public release — DONE
- Exact next action: None pending. Next session: pick a follow-up (providers, OCR, auth) or demo via `cp .env.example .env && docker compose up --build`
- Blocked by: None.
- Contexto durável: Automático (não perguntar de novo)
- Resume prompt: `Read AGENTS.md and .ai/HANDOFF.md. Continue from the Resume block. Do not rediscover context.`

## Goal

MVP v0.1.0 released at https://github.com/crilsen/qualitydocs-ai-copilot/releases/tag/v0.1.0

## Current State

Public repo `crilsen/qualitydocs-ai-copilot` with topics, 3 logical commits, release v0.1.0.

## What Was Done

- Full MVP: backend, 6 versioned prompts, frontend 7 screens, evaluation, README (all in English; conversation in PT-BR per user).
- Validated: pytest 4/4, evaluation 5/5, Next build 7 routes, compose build + backend smoke (health + governance OK).

## Files Changed

- All project files (see 3 commits). Local-only (untracked): `.env` (from example), no secrets committed.

## Decisions Made

- Conversation PT-BR / files EN (user, 2026-09-25).
- `db.query().get()` → `db.get()` (SQLAlchemy 2.0).
- Backend Dockerfile drops prompts copy; prompts mounted ro via compose + embedded defaults fallback.
- `next-env.d.ts` + `package-lock.json` kept in repo.

## Problems / Risks

- Homebrew Python 3.14 is PEP-668 externally managed → validation done via Docker (python:3.12, node:20). Documented here for next sessions.

## Validation Performed

- Validated: backend tests, evaluation, frontend build, compose config/build, container smoke test.
- Not validated: full `docker compose up` with frontend (images built, backend smoke OK).

## Next Actions

- Demo: `cp .env.example .env && docker compose up --build` (UI :3000, API :8000).
