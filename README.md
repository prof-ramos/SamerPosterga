# 🤖 Bot Jurídico para Concursos

Bot Discord com capacidades RAG (Retrieval-Augmented Generation) especializado em auxiliar estudantes de concursos públicos no Brasil com questões jurídicas.

## ✨ Características

- **RAG Avançado**: Busca inteligente em documentos jurídicos usando embeddings
- **Especialização Jurídica**: Conhecimento abrangente das principais áreas do Direito para concursos públicos
- **Integração Discord**: Interface intuitiva via comandos slash e menções
- **Múltiplos Formatos**: Suporte a PDF, TXT, Markdown e DOCX
- **OpenRouter + OpenAI**: Modelos de linguagem avançados para respostas precisas

## 🚀 Instalação

### Pré-requisitos

- Python 3.11+
- Discord Bot Token
- OpenRouter API Key
- OpenAI API Key

### Instalação Rápida

```bash
# Clone o repositório
git clone <repository-url>
cd juridic-concursos-bot

# Instale as dependências
pip install -r requirements.txt

# Configure as variáveis de ambiente
cp .env.example .env
# Edite o .env com suas chaves API
```

### Usando Docker

```bash
# Build da imagem
docker build -t juridic-bot .

# Execute o container
docker-compose up -d
```

## ⚙️ Configuração

### Arquivo .env

```env
# Discord Config
DISCORD_TOKEN=seu_token_aqui
DISCORD_APP_ID=seu_app_id_aqui
DISCORD_GUILD_ID=opcional_guild_id
DISCORD_OWNER_ID=seu_user_id_para_comandos_admin

# OpenRouter Config
OPENROUTER_API_KEY=seu_openrouter_key
OPENROUTER_MODEL=anthropic/claude-3.5-sonnet
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1

# OpenAI Config (para embeddings)
OPENAI_API_KEY=sua_openai_key
EMBEDDING_MODEL=text-embedding-3-small

# RAG Config
TOP_K=5
CHUNK_SIZE=1500
CHUNK_OVERLAP=200

# System Config
MAX_TOKENS=2000
TEMPERATURE=0.7
LOG_LEVEL=INFO
```

### Documentos

Coloque seus documentos na pasta `knowledge/`:
- `knowledge/` - Documentos para indexação RAG
- Organize em subpastas por área do direito:
  - `knowledge/direito_constitucional/`
  - `knowledge/direito_administrativo/`
  - `knowledge/direito_penal/`
  - `knowledge/direito_civil/`
  - etc.
- Suportados: `.pdf`, `.txt`, `.md`, `.docx`

## 🎯 Uso

### Comandos Disponíveis

| Comando | Descrição |
|---------|-----------|
| `/ping` | Verifica latência do bot |
| `/status` | Mostra status do sistema |
| `/reindex` | Reindexa documentos (apenas owner) |
| `/buscar_lei` | Busca lei específica |
| `/ajuda` | Menu de ajuda |

### Interação por Menção

Mencione o bot (@Bot) seguido de sua pergunta:

```
@Bot Qual é a legislação sobre férias de oficiais de chancelaria?
```

### Respostas Estruturadas

O bot fornece:
- Respostas baseadas em documentos indexados
- Citação de fontes consultadas
- Disclaimer legal
- Contexto jurídico específico do Serviço Exterior

## 🏗️ Arquitetura

```
src/juridic_bot/
├── config.py          # Configurações centralizadas
├── main.py           # Ponto de entrada
├── bot/              # Módulo Discord
│   ├── __init__.py
│   └── bot.py
├── rag/              # Sistema RAG
│   ├── __init__.py
│   ├── embeddings.py # Serviço de embeddings
│   ├── ingest.py     # Processamento de documentos
│   └── retriever.py  # Busca e recuperação
└── llm/              # Cliente LLM
    ├── __init__.py
    └── client.py
```

## 🧪 Desenvolvimento

### Configuração do Ambiente de Desenvolvimento

```bash
# Instale dependências de desenvolvimento
pip install -e ".[dev]"

# Execute os testes
pytest

# Verifique qualidade do código
flake8 src/
mypy src/
black src/
isort src/
```

### Estrutura de Testes

```bash
tests/
├── __init__.py
├── test_config.py     # Testes de configuração
└── test_rag.py       # Testes do sistema RAG
```

## 📊 Monitoramento

### Logs

Os logs são salvos em `logs/bot.log` com diferentes níveis:
- DEBUG: Informações detalhadas para desenvolvimento
- INFO: Operações normais
- WARNING: Avisos não críticos
- ERROR: Erros que precisam atenção

### Métricas

- Uso de tokens por consulta
- Tempo de resposta
- Taxa de sucesso de buscas
- Status do sistema (CPU, RAM, uptime)

## 🔒 Segurança

- **Nunca commite chaves API** no repositório
- Use sempre variáveis de ambiente para secrets
- Logs não incluem informações sensíveis
- Validação rigorosa de entrada de usuários

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

### Padrões de Código

- **Black**: Formatação automática
- **isort**: Organização de imports
- **flake8**: Linting
- **mypy**: Type checking
- **pytest**: Testes

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 📞 Suporte

Para suporte técnico ou dúvidas sobre o projeto:

- 📧 Email: suporte@juridic-bot.com
- 🐛 Issues: [GitHub Issues](https://github.com/juridic-bot/concursos-bot/issues)
- 📖 Documentação: [Wiki](https://github.com/juridic-bot/concursos-bot/wiki)

---

⭐ **Star este repositório** se o projeto foi útil para você!