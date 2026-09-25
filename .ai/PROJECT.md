# Project

## Identity

- **Name:** Document Quality AI Copilot (qualitydocs-ai-copilot)
- **Objective:** Aplicação web para consolidar, comparar e validar documentos de qualidade com IA generativa, demonstrando Prompt Engineering, Context Engineering, rastreabilidade, revisão humana e governança básica.
- **Status:** MVP v0.1.0 em construção (primeira release, portfólio, apenas dados sintéticos).
- **Idioma:** Interface e documentação em português.

## Stack (observado do escopo aprovado)

- Backend: Python 3.12 + FastAPI + SQLAlchemy (SQLite local) + Pydantic
- Frontend: Next.js + TypeScript + Tailwind CSS
- Processamento: PDF (pypdf) e DOCX (python-docx)
- LLM: camada de provider abstrata; suporte inicial Anthropic Claude via API; preparado para OpenAI/Gemini
- Containers: Docker Compose
- Config: `.env.example`, sem credenciais reais

## Modos de análise

resumo executivo, comparação entre documentos/versões, itens ausentes, divergências e inconsistências, riscos e não conformidades, plano de ação sugerido.

## Princípios

- Apenas dados sintéticos de exemplo; nenhum dado real/confidencial.
- MVP demonstrável, sem funcionalidades excessivas.
- Nunca usar o termo "enterprise" no projeto.
- Contexto durável: modo Automático (atualizar .ai/ conforme o trabalho avança, sem perguntar de novo). Registrado em HANDOFF.
