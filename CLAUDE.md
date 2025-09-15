# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Projeto Overview

Este é um **Bot Discord especializado em direito para concursos públicos** com capacidades RAG (Retrieval-Augmented Generation). O bot utiliza embeddings e LLMs para responder perguntas jurídicas baseadas em documentos indexados.

## Comandos de Desenvolvimento

### Dependências e Ambiente
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

### Fluxo RAG
1. **Ingestão**: `DocumentProcessor` processa PDFs/TXTs da pasta `knowledge/`
2. **Indexação**: ChromaDB armazena embeddings via OpenAI `text-embedding-3-small`
3. **Busca**: `RAGRetriever` faz busca vetorial por similaridade
4. **Geração**: `LLMClient` usa OpenRouter (Claude/GPT) para gerar respostas

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
OPENROUTER_MODEL=anthropic/claude-3.5-sonnet
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
└── direito_civil/
```
Formatos suportados: `.pdf`, `.txt`, `.md`, `.docx`

## Comandos Discord

### Comandos Slash
- `/ping` - Latência do bot
- `/status` - Status do sistema (CPU, RAM, uptime)
- `/pergunta <texto>` - Pergunta jurídica com contexto RAG
- `/buscar_lei <numero> [ano]` - Busca lei específica
- `/reindex` - Reindexa documentos (apenas owner)
- `/ajuda` - Menu de ajuda

### Interação Natural
- **Menção**: `@Bot qual a legislação sobre...`
- **DM**: Mensagem direta ao bot
- **Respostas conversacionais** com disclaimer legal

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
2. Configurar tokens/APIs
3. Adicionar documentos em `knowledge/`
4. Executar indexação inicial
5. Iniciar bot