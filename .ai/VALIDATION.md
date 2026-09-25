# Validation

## Completion rule

Antes de concluir, rodar validações aplicáveis e reportar como Validated / Partially / Not validated.

## MVP v0.1.0

1. Backend: `cd backend && pip install -r requirements.txt && pytest -q` → esperado verde.
2. Frontend: `cd frontend && npm install && npm run build` (ou `npx tsc --noEmit`) → esperado sem erro.
3. Compose: `docker compose config` (e `up --build` quando Docker disponível) → serviços backend/frontend saudáveis.
4. Smoke API: `POST /api/documents/upload`, `POST /api/analyses/run`, `GET /api/history`, filtros de findings, revisão humana.
5. Evaluation: `python evaluation/run_evaluation.py --output evaluation/report.md` → relatório gerado com citações, aderência JSON, findings sem evidência = 0.

## Limites conhecidos

- Sem chave Anthropic, o backend usa analisador heurístico local de demonstração (mesmo schema, cita trechos reais). Com chave, usa Claude via API.
- SQLite local; sem autenticação multiusuário no MVP.
