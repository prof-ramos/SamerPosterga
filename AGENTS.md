# Repository Guidelines

## Project Structure & Module Organization
- `src/juridic_bot/` contém o código principal (módulos de bot Discord, RAG e configuração).
- `knowledge/` armazena a base jurídica consumida pelo pipeline de ingestão; `./.chroma/` guarda o índice vetorial persistido.
- `tests/` cobre unidades e integrações; `docs/` reúne guias de desenvolvimento e deploy.
- `deploy/` oferece manifests Docker/Portainer; `scripts/` agrega utilitários de setup.

## Build, Test, and Development Commands
- `uv run juridic-bot` inicia o bot localmente após configurar `.env`.
- `uv run rag-reindex` reprocessa documentos e recria a ChromaDB usando `DocumentProcessor`.
- `uv run pytest` ou `uv run pytest --cov=src` executa a suíte de testes com cobertura.
- `docker-compose up -d` sobe a stack containerizada; `docker-compose logs -f juridic-bot` acompanha a execução.

## Coding Style & Naming Conventions
- Python 3.11 com Black (linha máxima 120) e isort perfil black garantem formatação consistente.
- Execute `uv run black src/ && uv run isort src/` antes de abrir PRs.
- PEP 8 para nomes: módulos `snake_case`, classes `PascalCase`, constantes `UPPER_SNAKE_CASE`.
- Flake8 e mypy (`uv run flake8 src/`, `uv run mypy src/`) evitam lint e tipos quebrados.

## Testing Guidelines
- Pytest dirige testes unitários/integrados; use marcadores `@pytest.mark.unit`, `integration`, `slow`, `asyncio` quando aplicável.
- Nomeie arquivos `test_*.py` e funções `test_*` conforme `pyproject.toml`.
- Busque manter ou melhorar cobertura reportada via `--cov`; valide caminhos críticos como `rag/` e `bot/`.

## Commit & Pull Request Guidelines
- Mensagens seguem o estilo convencional (`feat:`, `fix:`, `chore:`). Agrupe mudanças correlatas em commits focados.
- PRs devem incluir: descrição clara, passos de teste manual (ex.: `uv run rag-reindex`), issues relacionadas e evidências relevantes (logs, capturas do Discord, etc.).
- Certifique-se de que linters e testes passam localmente antes do push.

## Security & Configuration Tips
- Nunca faça commit de `.env` ou chaves; use `cp .env.example .env` e configure tokens manualmente.
- Volumes Docker precisam mapear `knowledge/`, `.chroma/` e `logs/` para persistência.
- Limpe dados sensíveis de logs antes de compartilhá-los em issues ou PRs.
