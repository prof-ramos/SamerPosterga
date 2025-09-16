# AGENTS.md - Juridic Concursos Bot

## Commands
- **Run**: `uv run juridic-bot` or `python -m src.juridic_bot.main`
- **Install**: `uv sync --dev` or `pip install -e ".[dev]"`
- **Test single**: `uv run pytest tests/test_<module>.py::<TestClass>::<test_method> -v`
- **Test all**: `uv run pytest` or `pytest --cov=src`
- **Lint**: `uv run flake8 src/` or `flake8 src/ --max-line-length=120`
- **Type check**: `uv run mypy src/` or `mypy src/ --ignore-missing-imports`
- **Format**: `uv run black src/ && uv run isort src/`

## Code Style
- **Imports**: stdlib, third-party, local with blank lines; `isort` (profile black)
- **Naming**: snake_case functions/variables, PascalCase classes, UPPER_CASE constants
- **Types**: Type hints required for public functions; strict mypy enabled
- **Docstrings**: Triple quotes for classes and public methods
- **Error handling**: Specific exceptions with context logging; graceful user errors
- **Logging**: `logging.getLogger(__name__)` with levels; logs to `logs/bot.log`
- **Async**: async/await for Discord/LLM ops; pytest-asyncio for tests

## Conventions
- **Structure**: Modular src/juridic_bot/ with bot/, rag/, llm/ submodules
- **Config**: Environment variables via python-dotenv; validate in Config class
- **Security**: Never log API keys/tokens; use .env for secrets; validate inputs
- **Testing**: pytest with markers (unit/integration); coverage enabled
- **Deps**: Pin versions in pyproject.toml; prefer stable releases