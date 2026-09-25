# Conventions

## Observadas (projeto)

- Language: conversation with user in PT-BR; ALL project files in English (code, UI, docs, commits). Decided 2026-09-25, overrides earlier PT requirement for files.
- Backend: FastAPI com routers `documents`, `analyses`, `reviews`, `governance`; schemas Pydantic; nomes de arquivo snake_case.
- Prompts versionados em `prompts/*.md` com front-matter (`version`, `mode`); seleção de versão na UI e registro por execução.
- Frontend: Next.js App Router + TypeScript + Tailwind; páginas PT: dashboard, upload, análise, resultados, histórico, revisão, governança.
- Dados sintéticos apenas em `data/synthetic/` e `backend/seed/`; nunca dados reais.
- Nunca usar o termo "enterprise".
- Commits lógicos em PT ou EN curto; release inicial `v0.1.0`.

## Documentação

- README em PT com problema, arquitetura, fluxo, execução local, config Anthropic, limitações, placeholders de screenshot, e seção de Prompt/Context Engineering, governança e revisão humana + diagrama Mermaid.
- `.ai/` em modo Automático: primário atualiza TASKS/HANDOFF/LEARNINGS; promouvoir aprendizados duráveis.
