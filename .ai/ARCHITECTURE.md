# Architecture

## Componentes (MVP)

```text
[Next.js Frontend] ──REST/JSON──> [FastAPI Backend] ──> [SQLite via SQLAlchemy]
                                         │
                          ┌──────────────┼──────────────┐
                          │              │              │
                   [Extrator        [Prompt          [LLM Provider
                    PDF/DOCX]        Registry]        registry: anthropic
                    pypdf/           prompts/*.md     openai (GPT/Codex)
                    python-docx      versionados      gemini
                                     + Pydantic       compat (OpenCode/
                                     output schema   OpenRouter/Ollama)
                                                     local demo (sem chave)]
```

## Fluxo

1. Upload 2–5 docs (PDF/DOCX) → extração (texto, nome, página/seção, data) → lista.
2. Seleção modo de análise + versão do prompt.
3. Backend monta contexto (documentos como DADO, nunca instrução) + system prompt → provider LLM (ou heurística local de demonstração quando sem chave).
4. Saída JSON validada por Pydantic (`executive_summary`, `findings[]` com evidence, `limitations`).
5. Revisão humana (Pendente/Aceito/Editado/Rejeitado + comentário) → resumo de status.
6. Histórico de execuções (prompt, modelo, latência, data).

## Segurança

- Validação tipo/tamanho; sem log de conteúdo completo; sem expor chaves; erros amigáveis; defesa básica contra prompt injection (conteúdo = dado, system prompt imutável, detecção e registro de texto suspeito).

## Deploy local

- `docker compose up --build` (backend :8000, frontend :3000). Sem IaC cloud; workflows terraform/kubernetes/cloud-port não se aplicam.
