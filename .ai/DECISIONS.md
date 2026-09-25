# Decision Records

Modo: Simple (inline até ~15–20 registros).

## Index

| ID | Type | Title | Status | Date |
| --- | --- | --- | --- | --- |
| ADR-001 | ADR | Monólito modular FastAPI + Next.js via REST, SQLite local | Accepted | 2026-09-25 |
| TDR-001 | TDR | Provider LLM abstrato com Anthropic primeiro, stub local sem chave | Accepted | 2026-09-25 |
| ADR-002 | ADR | Prompts versionados em arquivos Markdown, não no código | Accepted | 2026-09-25 |
| TDR-002 | TDR | Extração PDF com pypdf e DOCX com python-docx | Accepted | 2026-09-25 |
| ADR-003 | ADR | Revisão humana por finding com status + comentário, nunca auto-aprovação | Accepted | 2026-09-25 |
| TDR-003 | TDR | Multi-provider LLM: Anthropic + OpenAI + Gemini + OpenAI-compat + local, seleção por run | Accepted | 2026-09-25 |

## Records

### ADR-001 — Monólito modular FastAPI + Next.js via REST, SQLite local
Type: ADR | Status: Accepted | Date: 2026-09-25 | Owners: usuário + agente
Context: MVP de portfólio precisa ser executável com `docker compose up`, sem cloud.
Decision: Backend FastAPI modular, frontend Next.js, SQLite via SQLAlchemy, comunicação REST/JSON.
Consequences: Simplicidade e demonstração local; sem multiusuário/auth no MVP.

### TDR-001 — Provider LLM abstrato com Anthropic primeiro, stub local sem chave
Type: TDR | Status: Accepted | Date: 2026-09-25 | Owners: usuário + agente
Context: Chave real não pode ser commitada; demo precisa funcionar sem chave.
Decision: Interface `LLMProvider` + `AnthropicProvider` + `LocalDemoProvider` (heurístico, mesmo schema Pydantic).
Consequences: Demo offline funciona; troca para OpenAI/Gemini futura sem mudar rotas.

### ADR-002 — Prompts versionados em arquivos Markdown
Type: ADR | Status: Proposed | Date: 2026-09-25 | Owners: usuário + agente
Context: Demonstrar Prompt Engineering exige prompts auditáveis e selecionáveis.
Decision: `prompts/*.md` com front-matter de versão; UI seleciona versão; execução registra prompt/modelo/latência.
Consequences: Rastreabilidade total prompt→resposta.

### TDR-002 — Extração PDF/DOCX
Type: TDR | Status: Accepted | Date: 2026-09-25
Context: Upload 2–5 arquivos PDF/DOCX com página/seção.
Decision: `pypdf` para PDF, `python-docx` para DOCX.
Consequences: Sem OCR no MVP (PDF escaneado retorna aviso amigável).

### TDR-003 — Multi-provider LLM com seleção por run
Type: TDR | Status: Accepted | Date: 2026-09-25 | Owners: usuário + agente
Context: Usuário pediu o app adaptado para Codex (OpenAI), OpenCode e Gemini, além do Anthropic inicial.
Decision: Registry `PROVIDERS` em `app/services/llm.py` com ids anthropic/openai/gemini/compat/local; `GET /api/providers` expõe disponibilidade; `RunAnalysisRequest.provider` (default auto, cloud primeiro, local por último); erro 400 amigável com a env var que falta; provider compat cobre OpenCode gateway/OpenRouter/Ollama/vLLM com retry sem JSON estrito. Pydantic elevado a 2.13.5 (exigido por google-genai).
Consequences: Troca de modelo sem mudar rotas; demo offline continua funcionando sem chaves.

### ADR-003 — Revisão humana por finding
Type: ADR | Status: Accepted | Date: 2026-09-25
Context: Governança exige validação humana antes de qualquer decisão.
Decision: Status Pendente/Aceito/Editado/Rejeitado + comentário + edição de título/descrição/ação; resumo agregado.
Consequences: Nenhuma conclusão sem evidência é exibida como validada.
