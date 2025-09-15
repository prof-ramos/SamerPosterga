# AGENTS.md - Discord RAG Bot Project

## Build/Test Commands
- **Run bot**: `python discord-rag-bot-complete.py`
- **Install deps**: `pip install -r requirements.txt` (embedded in main file lines 10-23)
- **Test single function**: `python -m pytest tests/test_<module>.py::<TestClass>::<test_method> -v`
- **Lint code**: `python -m flake8 discord-rag-bot-complete.py --max-line-length=120`
- **Type check**: `python -m mypy discord-rag-bot-complete.py --ignore-missing-imports`

## Code Style Guidelines
- **Imports**: Group by stdlib, third-party, local modules with blank lines between groups
- **Naming**: snake_case for functions/variables, PascalCase for classes, UPPER_CASE for constants
- **Types**: Use type hints for all function parameters and return values
- **Docstrings**: Use triple quotes with brief description for all classes and public methods
- **Error handling**: Use try/except with specific exceptions, log errors with context
- **Logging**: Use logging module with appropriate levels (DEBUG, INFO, WARNING, ERROR)
- **Async**: Use async/await consistently for Discord interactions and I/O operations

## Project Conventions
- **File structure**: Keep all code in single file with clear section separators (===)
- **Configuration**: Use environment variables via python-dotenv, validate in Config class
- **Security**: Never log API keys or sensitive data, use .env for secrets
- **Documentation**: Include usage examples in comments, maintain requirements.txt inline
- **Testing**: Write unit tests for core functions (embeddings, retrieval, LLM client)
- **Dependencies**: Pin versions in requirements.txt, prefer stable releases

## Development Workflow
1. Set up .env file with required API keys before running
2. Test locally with minimal documents in RRAG/ directory
3. Use logging levels appropriately for debugging
4. Validate configuration before deployment
5. Monitor token usage and API rate limits in production