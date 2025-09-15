# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Projeto Overview

Este é um **Bot Discord conversacional especializado em direito para concursos públicos** com capacidades RAG (Retrieval-Augmented Generation). O bot opera em **modo conversacional** - responde naturalmente a menções e DMs sem comandos complexos, funcionando como um professor jurídico amigável.

## Comandos de Desenvolvimento

### UV Package Manager (Recomendado)
```bash
# Instalar dependências principais
uv sync

# Instalar com dependências de desenvolvimento
uv sync --dev

# Executar o bot
uv run juridic-bot

# Executar testes
uv run pytest

# Code quality
uv run black src/
uv run isort src/
uv run flake8 src/
uv run mypy src/
```

### Dependências Tradicionais (pip)
```bash
# Instalar dependências principais
pip install -r requirements.txt

# Instalar dependências de desenvolvimento
pip install -e ".[dev]"

# Executar o bot
python -m src.juridic_bot.main
```

### Testes
```bash
# Executar todos os testes
pytest

# Executar testes com cobertura
pytest --cov=src

# Executar apenas testes unitários
pytest -m unit

# Executar apenas testes de integração
pytest -m integration
```

### Code Quality
```bash
# Formatação de código
black src/
isort src/

# Linting
flake8 src/

# Type checking
mypy src/

# Executar todas as verificações
black src/ && isort src/ && flake8 src/ && mypy src/
```

### Docker
```bash
# Build da imagem
docker build -t juridic-bot .

# Executar com docker-compose
docker-compose up -d

# Ver logs
docker-compose logs -f juridic-bot
```

## Arquitetura do Sistema

### Estrutura Principal
```
src/juridic_bot/
├── main.py              # Ponto de entrada, inicialização do bot
├── config.py            # Configuração centralizada (env vars, paths)
├── bot/
│   └── bot.py          # Implementação Discord Bot com comandos slash
├── rag/
│   ├── embeddings.py   # Serviço OpenAI embeddings
│   ├── ingest.py       # Processamento e indexação de documentos
│   └── retriever.py    # Busca vetorial e formatação de contexto
└── llm/
    └── client.py       # Cliente OpenRouter/LLM para geração de respostas
```

### Fluxo RAG Conversacional
1. **Ingestão**: `DocumentProcessor` processa PDFs/TXTs/DOCX da pasta `knowledge/`
2. **Indexação**: ChromaDB armazena embeddings via OpenAI `text-embedding-3-small`
3. **Escuta**: Bot monitora menções (@bot) e DMs automaticamente
4. **Busca**: `RAGRetriever` faz busca vetorial por similaridade (TOP_K=5)
5. **Geração**: `LLMClient` usa OpenRouter (DeepSeek) para respostas conversacionais
6. **Resposta**: Mensagens amigáveis sem disclaimers, como professor experiente

### Sistema de Configuração
- **Config centralizada**: `src/juridic_bot/config.py` usa variáveis de ambiente
- **Validação obrigatória**: `Config.validate()` verifica keys essenciais
- **Paths automáticos**: Diretórios baseados em `BASE_DIR` (knowledge/, .chroma/, logs/)

## Configuração Essencial

### Variáveis de Ambiente (.env)
```bash
# Obrigatórias
DISCORD_TOKEN=your_token
OPENROUTER_API_KEY=your_key
OPENAI_API_KEY=your_key

# Bot Discord
DISCORD_GUILD_ID=optional_guild
DISCORD_OWNER_ID=your_user_id

# Modelos
OPENROUTER_MODEL=deepseek/deepseek-chat-v3-0324
EMBEDDING_MODEL=text-embedding-3-small

# RAG Settings
TOP_K=5
CHUNK_SIZE=1500
CHUNK_OVERLAP=200
```

### Estrutura de Documentos
```
knowledge/
├── direito_constitucional/
├── direito_administrativo/
├── direito_penal/
├── direito_civil/
└── direito_processual/
```
Formatos suportados: `.pdf`, `.txt`, `.md`, `.docx`

**Organização recomendada**: Separar documentos por área jurídica para facilitar a busca contextual.

## Sistema de Interação

### Modo Conversacional (Principal)
- **Menção no servidor**: `@SamerPosterga qual a diferença entre habeas corpus e habeas data?`
- **DM direta**: `Oi! Me explica o que é improbidade administrativa?`
- **Respostas naturais**: Tom de professor amigável, sem disclaimers
- **Tratamento de erro**: Mensagens variadas e contextualizadas

### Comandos Técnicos (Administrativos)
- `/ping` - Verifica se o bot está respondendo
- `/status` - Status do sistema (CPU, RAM, uptime)
- `/reindex` - Reindexa documentos (apenas owner)
- Comandos slash tradicionais são opcionais e para usuários avançados

## Padrões de Código

### Logging
- Configurado em `bot.py` com níveis INFO/DEBUG/ERROR
- Logs salvos em `logs/bot.log`
- Logger por módulo: `logger = logging.getLogger(__name__)`

### Error Handling
- Try/catch em todas as operações Discord/LLM
- Respostas de erro amigáveis para usuários
- Logs detalhados para debugging

### Type Safety
- mypy habilitado com strict mode
- Type hints obrigatórios em funções públicas
- Overrides para libs sem tipos (chromadb, langchain)

### Code Style
- **Black**: linha 120 chars, Python 3.11+
- **isort**: profile black, trailing commas
- **flake8**: linting padrão
- **pytest**: testes com markers (unit/integration/slow)

## Debugging e Desenvolvimento

### Logs Importantes
```bash
# Ver logs em tempo real
tail -f logs/bot.log

# Logs do Docker
docker-compose logs -f juridic-bot
```

### Reindexação de Documentos
```bash
# Via comando Discord (owner only)
/reindex

# Via código
python -c "from src.juridic_bot.rag.ingest import DocumentProcessor; DocumentProcessor().create_vectorstore()"
```

### Testing RAG Pipeline
```bash
# Testar busca vetorial
python -c "
from src.juridic_bot.rag.retriever import RAGRetriever
r = RAGRetriever()
docs = r.search('constituição federal', k=3)
print([d.page_content[:100] for d in docs])
"
```

## Deployment

### Docker Production
- Multi-arch support (linux/amd64, linux/arm64)
- Volumes para persistência: `knowledge/`, `.chroma/`, `logs/`
- Health checks configurados
- Restart policy: unless-stopped

### Environment Setup
1. Copiar `.env.example` para `.env`
2. Configurar tokens/APIs obrigatórias (Discord, OpenRouter, OpenAI)
3. Adicionar documentos jurídicos em `knowledge/` organizados por área
4. Executar indexação inicial automática no primeiro run
5. Iniciar bot e testar com menções conversacionais

### Características Conversacionais Importantes
- **Sem comandos slash por padrão**: Usuários simplesmente mencionam o bot
- **Respostas didáticas**: Explicações como professor, não chatbot formal
- **Contextualização jurídica**: Foco em concursos públicos brasileiros
- **Erro handling inteligente**: Mensagens variadas para situações diferentes
- **Performance**: Modo conversacional otimizado para fluidez