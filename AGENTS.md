# AGENTS.md - Juridic Concursos Bot

## Build/Test Commands
- **Run bot**: `uv run juridic-bot` or `python -m src.juridic_bot.main`
- **Install deps**: `uv sync --dev` or `pip install -e ".[dev]"`
- **Test single function**: `uv run pytest tests/test_<module>.py::<TestClass>::<test_method> -v`
- **Run all tests**: `uv run pytest` or `pytest --cov=src`
- **Lint code**: `uv run flake8 src/` or `flake8 src/ --max-line-length=120`
- **Type check**: `uv run mypy src/` or `mypy src/ --ignore-missing-imports`
- **Format code**: `uv run black src/ && uv run isort src/`

## Code Style Guidelines
- **Imports**: Group stdlib, third-party, local with blank lines; use `isort` (profile black)
- **Naming**: snake_case functions/variables, PascalCase classes, UPPER_CASE constants
- **Types**: Type hints required for all public functions; strict mypy mode enabled
- **Docstrings**: Triple quotes with brief description for classes and public methods
- **Error handling**: Specific exceptions with context logging; graceful user-facing errors
- **Logging**: `logging.getLogger(__name__)` with appropriate levels; logs to `logs/bot.log`
- **Async**: Use async/await consistently for Discord/LLM operations; pytest-asyncio for tests

## Project Conventions
- **Structure**: Modular src/juridic_bot/ with bot/, rag/, llm/ submodules
- **Configuration**: Environment variables via python-dotenv; validate in Config class
- **Security**: Never log API keys/tokens; use .env for secrets; validate inputs
- **Testing**: pytest with markers (unit/integration); coverage reporting enabled
- **Dependencies**: Pin versions in pyproject.toml; prefer stable releases