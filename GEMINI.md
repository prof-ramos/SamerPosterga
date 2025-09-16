# Gemini Project: Juridic Bot

## Project Overview

This project is a Discord bot named "Juridic Bot" designed to assist Brazilian law students preparing for public exams. It functions as a conversational AI, leveraging a Retrieval-Augmented Generation (RAG) system to answer legal questions. The bot is built with Python and utilizes several key technologies:

*   **Discord.py:** For interacting with the Discord API.
*   **OpenAI:** For generating text embeddings for the RAG system.
*   **OpenRouter:** To use various large language models for generating responses.
*   **ChromaDB:** As a vector store for the RAG system.
*   **LangChain:** To orchestrate the RAG pipeline.
*   **Docker:** For containerization and deployment.
*   **UV:** For python environment and package management.
*   **MkDocs:** For documentation.

The bot's knowledge base is sourced from `.docx` files located in the `knowledge` directory, which are indexed into the ChromaDB vector store. The RAG database is included in the Docker image.

## Building and Running

### Development Environment

1.  **Install UV:**
    ```bash
    curl -LsSf https://astral.sh/uv/install.sh | sh
    ```
2.  **Install Dependencies:**
    ```bash
    uv sync --dev
    ```
3.  **Configure Environment:**
    *   Copy `.env.example` to `.env`.
    *   Fill in the required environment variables in the `.env` file, including API keys for Discord, OpenAI, and OpenRouter.
4.  **Run the Bot:**
    ```bash
    uv run juridic-bot
    ```

### Docker

1.  **Build the Docker Image:**
    ```bash
    docker build -t juridic-bot .
    ```
2.  **Run with Docker Compose:**
    ```bash
    docker-compose up -d
    ```

### Testing

*   Run tests with `pytest`:
    ```bash
    uv run pytest
    ```
*   Run tests with coverage:
    ```bash
    uv run pytest --cov=src
    ```

### Code Quality

*   **Formatting:**
    ```bash
    uv run black src/
    ```
*   **Import Sorting:**
    ```bash
    uv run isort src/
    ```
*   **Linting:**
    ```bash
    uv run flake8 src/
    ```
*   **Type Checking:**
    ```bash
    uv run mypy src/
    ```

## Development Conventions

*   **Code Style:** The project uses `black` for code formatting and `isort` for import sorting.
*   **Linting:** `flake8` is used for linting.
*   **Type Hinting:** The project uses type hints, and `mypy` is used for static type checking.
*   **Testing:** Tests are written using `pytest` and are located in the `tests` directory.
*   **Documentation:** The documentation is written in Markdown and built with `MkDocs`. The source files are in the `docs` directory.
