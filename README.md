# Juridic Bot - Assistente Jurídico para Concursos

[![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)](https://hub.docker.com/r/gabrielramosprof/juridic-bot)
[![Python](https://img.shields.io/badge/python-3.11+-blue.svg?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Discord](https://img.shields.io/badge/Discord-%235865F2.svg?style=for-the-badge&logo=discord&logoColor=white)](https://discord.com)

Bot Discord conversacional especializado em **direito para concursos públicos brasileiros** com capacidades RAG (Retrieval-Augmented Generation). Funciona como um professor jurídico experiente, respondendo naturalmente a menções e mensagens diretas.

## ✨ Características

- **🤖 Chatbot Conversacional**: Interação natural via @menção ou DM, sem comandos complicados
- **🧠 RAG Inteligente**: Busca contextual em documentos jurídicos usando embeddings OpenAI
- **📚 Especialização Jurídica**: Foco nas principais áreas do Direito brasileiro para concursos
- **🎯 Respostas Didáticas**: Explicações claras e progressivas, como um professor experiente
- **⚡ Resposta Rápida**: Interface fluida sem barreiras técnicas
- **📄 Múltiplos Formatos**: Suporte a PDF, TXT, Markdown e DOCX
- **🔧 OpenRouter + OpenAI**: Modelos avançados (DeepSeek + embeddings) para respostas precisas

## 🚀 Início Rápido

### Docker (Recomendado)

```bash
# 1. Clonar repositório
git clone https://github.com/prof-ramos/SamerPosterga.git
cd SamerPosterga

# 2. Configurar ambiente
cp .env.example .env
# Editar .env com suas credenciais

# 3. Executar
docker-compose up -d

# 4. Ver logs
docker-compose logs -f juridic-bot
```

### Portainer (Produção)

1. Acesse **Portainer → Stacks → Add Stack**
2. Cole o conteúdo de [`deploy/portainer/portainer-stack.yml`](./deploy/portainer/portainer-stack.yml)
3. Configure as variáveis de ambiente obrigatórias
4. Deploy da stack

➡️ **Guia completo**: [Deploy no Portainer](./deploy/portainer/README.md)

## 📋 Pré-requisitos

### Credenciais Obrigatórias

| Serviço | Variável | Onde Obter |
|---------|----------|------------|
| Discord | `DISCORD_TOKEN` | [Discord Developer Portal](https://discord.com/developers/applications) |
| OpenAI | `OPENAI_API_KEY` | [OpenAI API Keys](https://platform.openai.com/api-keys) |
| OpenRouter | `OPENROUTER_API_KEY` | [OpenRouter Keys](https://openrouter.ai/keys) |

### IDs Discord

- `DISCORD_OWNER_ID`: Seu ID de usuário (clique direito → Copiar ID)
- `DISCORD_GUILD_ID`: ID do servidor (opcional)

## 📁 Estrutura do Projeto

```
juridic-bot/
├── src/                    # Código fonte
│   └── juridic_bot/
│       ├── bot/           # Discord bot implementation
│       ├── rag/           # RAG system (retrieval, embeddings)
│       ├── llm/           # LLM client (OpenRouter)
│       └── config.py      # Configuration management
├── tests/                  # Testes automatizados
├── docs/                   # Documentação completa
│   ├── development/       # Guias de desenvolvimento
│   └── deployment/        # Guias de deploy
├── deploy/                 # Arquivos de deployment
│   ├── docker/           # Docker configs
│   └── portainer/        # Portainer stack
├── scripts/               # Scripts auxiliares
├── knowledge/             # Base de conhecimento jurídico
└── README.md              # Este arquivo
```

## 📚 Base de Conhecimento

Organize documentos jurídicos em `knowledge/`:

```
knowledge/
├── direito_constitucional/
├── direito_administrativo/
├── direito_penal/
├── direito_civil/
└── direito_processual/
```

**Formatos suportados**: `.pdf`, `.txt`, `.md`, `.docx`

O bot indexa automaticamente na primeira execução.

## 🐳 Docker

### Imagem Oficial

```bash
# Executar imagem do DockerHub
docker run -d \
  --name juridic-bot \
  -e DISCORD_TOKEN=seu_token \
  -e OPENAI_API_KEY=sua_key \
  -e OPENROUTER_API_KEY=sua_key \
  -v $(pwd)/knowledge:/app/knowledge \
  gabrielramosprof/juridic-bot:latest
```

### Build Local

```bash
# Build otimizado
docker build -f deploy/docker/Dockerfile -t juridic-bot .

# Build multiarch
docker buildx build --platform linux/amd64,linux/arm64 -t juridic-bot .
```

## ⚙️ Configuração Avançada

### System Prompt Personalizado

```bash
# Via variável de ambiente
SYSTEM_PROMPT="Seu prompt personalizado aqui..."
```

### Configurações RAG

```bash
TOP_K=5                    # Documentos por busca
CHUNK_SIZE=1500           # Tamanho dos chunks
CHUNK_OVERLAP=200         # Sobreposição entre chunks
EMBEDDING_MODEL=text-embedding-3-small
```

### Modelos LLM

```bash
# Modelos gratuitos (OpenRouter)
OPENROUTER_MODEL=qwen/qwen3-coder:free
OPENROUTER_MODEL=google/gemma-2-9b-it:free

# Modelos premium
OPENROUTER_MODEL=anthropic/claude-3.5-sonnet
OPENROUTER_MODEL=openai/gpt-4o
```

## 🔧 Desenvolvimento

### Setup Local

```bash
# 1. Instalar UV (recomendado)
curl -LsSf https://astral.sh/uv/install.sh | sh

# 2. Instalar dependências
uv sync --dev

# 3. Configurar ambiente
cp .env.example .env
# Editar .env

# 4. Executar bot
uv run juridic-bot
```

### Comandos Úteis

```bash
# Testes
uv run pytest
uv run pytest --cov=src

# Code Quality
uv run black src/
uv run isort src/
uv run flake8 src/
uv run mypy src/

# Executar tudo
uv run black src/ && uv run isort src/ && uv run flake8 src/ && uv run mypy src/
```

## 📖 Documentação

- **[Guia de Desenvolvimento](./docs/development/)** - Setup, arquitetura e contribuição
- **[Guia de Deploy](./docs/deployment/)** - Produção, Portainer e monitoramento
- **[API Reference](./docs/api/)** - Documentação técnica dos módulos

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch: `git checkout -b feature/nova-funcionalidade`
3. Commit: `git commit -m 'feat: adicionar nova funcionalidade'`
4. Push: `git push origin feature/nova-funcionalidade`
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja [LICENSE](./LICENSE) para detalhes.

## 🆘 Suporte

- **Issues**: [GitHub Issues](https://github.com/prof-ramos/SamerPosterga/issues)
- **Documentação**: [Pasta docs/](./docs/)
- **Docker**: [DockerHub](https://hub.docker.com/r/gabrielramosprof/juridic-bot)

---

**Desenvolvido com ❤️ para a comunidade jurídica brasileira**