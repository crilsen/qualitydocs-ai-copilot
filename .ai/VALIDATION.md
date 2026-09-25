# Validation

## Completion rule

Before completion, run applicable validations and report each as Validated / Partially / Not validated.

## MVP v0.1.0 (+ providers on main)

1. Backend: `cd backend && pip install -r requirements.txt && pytest -q` → expect green (6 tests).
2. Frontend: `cd frontend && npm install && npm run build` (or `npx tsc --noEmit`) → expect no errors (7 routes).
3. Compose: `docker compose config` (and `up --build` when Docker is available) → healthy backend/frontend services.
4. API smoke: `POST /api/documents/upload`, `POST /api/analyses/run`, `GET /api/providers`, `GET /api/history`, finding filters, human review.
5. Evaluation: `python evaluation/run_evaluation.py --output evaluation/report.md` → report with citations, JSON adherence, findings without evidence = 0.

## Known limits

- Without API keys, the backend uses the offline heuristic demo analyzer (same schema, quotes real excerpts). With keys, it uses the selected cloud provider.
- Local SQLite; no multi-user auth in MVP.
- Validation runs via Docker (python:3.12, node:20) because the host Homebrew Python is PEP-668 externally managed.
