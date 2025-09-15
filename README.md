# 🤖 Bot Jurídico Conversacional para Concursos

Assistente jurídico inteligente e amigável para estudantes de concursos públicos no Brasil. Funciona como um chatbot conversacional que responde naturalmente às suas dúvidas sobre direito.

## ✨ Características

- **🤖 Chatbot Conversacional**: Interação natural via @menção ou DM, sem comandos complicados
- **🧠 RAG Inteligente**: Busca contextual em documentos jurídicos usando embeddings OpenAI
- **📚 Especialização Jurídica**: Foco nas principais áreas do Direito brasileiro para concursos
- **🎯 Respostas Didáticas**: Explicações claras e progressivas, como um professor experiente
- **⚡ Resposta Rápida**: Interface fluida sem barreiras técnicas
- **📄 Múltiplos Formatos**: Suporte a PDF, TXT, Markdown e DOCX
- **🔧 OpenRouter + OpenAI**: Modelos avançados (DeepSeek + embeddings) para respostas precisas

## 🚀 Instalação

### Pré-requisitos

- Python 3.11+
- Discord Bot Token
- OpenRouter API Key
- OpenAI API Key

### 🚀 Instalação Rápida com UV

```bash
# Clone o repositório
git clone https://github.com/prof-ramos/SamerPosterga.git
cd SamerPosterga

# Instale as dependências com UV (recomendado)
uv sync

# Configure as variáveis de ambiente
cp .env.example .env
# Edite o .env com suas chaves API

# Execute o bot
uv run juridic-bot
```

### 🐳 Usando Docker

```bash
# Build da imagem multi-arch
docker build -t juridic-bot .

# Execute com docker-compose
docker-compose up -d

# Ou execute diretamente
docker run -d --env-file .env juridic-bot
```

### 📦 Instalação Tradicional (pip)

```bash
# Instale as dependências
pip install -r requirements.txt

# Execute o bot
python -m src.juridic_bot.main
```

## ⚙️ Configuração

### 📝 Arquivo .env

```env
# Discord Config
DISCORD_TOKEN=seu_token_aqui
DISCORD_APP_ID=seu_app_id_aqui
DISCORD_GUILD_ID=  # Deixe vazio para modo global
DISCORD_OWNER_ID=seu_user_id_para_comandos_admin

# OpenRouter Config (LLM principal)
OPENROUTER_API_KEY=seu_openrouter_key
OPENROUTER_MODEL=deepseek/deepseek-chat-v3-0324
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

### 🎯 Modo Conversacional

O bot está configurado para **modo conversacional**:
- ✅ **Sem comandos slash** - interação natural
- ✅ **Respostas amigáveis** - tom de professor
- ✅ **Sem disclaimers** - conversa fluida
- ✅ **Tratamento de erros** inteligente

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

## 🎯 Como Usar

### 🤖 Modo Conversacional

O bot funciona como um **chatbot amigável** - apenas mencione-o ou envie DM!

#### 📱 Via Menção no Servidor
```
@SamerPosterga Qual é a diferença entre habeas corpus e habeas data?
```

#### 💬 Via Mensagem Direta (DM)
```
Oi! Me explica o que é improbidade administrativa?
```

#### 🎓 Exemplos de Perguntas
- "O que é devido processo legal?"
- "Como funciona a prescrição penal?"
- "Qual a diferença entre mandado de segurança e ação popular?"
- "Me explica sobre responsabilidade civil do Estado"

### 💡 Características das Respostas

- **📖 Explicações Didáticas**: Conceitos explicados passo a passo
- **📚 Baseadas em Documentos**: Respostas fundamentadas em legislação
- **🎯 Foco em Concursos**: Conteúdo relevante para provas
- **😊 Tom Amigável**: Como conversar com um professor experiente
- **⚡ Respostas Rápidas**: Sem complicações técnicas

### 🔧 Comandos Técnicos (Opcional)

Para usuários avançados, alguns comandos ainda estão disponíveis:
- `/ping` - Verifica se o bot está respondendo
- `/status` - Mostra informações do sistema
- `/reindex` - Reindexa documentos (apenas admin)

## 🏗️ Arquitetura

```
src/juridic_bot/
├── config.py          # ⚙️ Configurações centralizadas
├── main.py           # 🚀 Ponto de entrada
├── bot/              # 🤖 Módulo Discord (modo conversacional)
│   ├── __init__.py
│   └── bot.py        # 💬 Lógica de chat e menções
├── rag/              # 🧠 Sistema RAG inteligente
│   ├── __init__.py
│   ├── embeddings.py # 🔍 Serviço de embeddings OpenAI
│   ├── ingest.py     # 📄 Processamento de documentos
│   └── retriever.py  # 🎯 Busca e recuperação contextual
└── llm/              # 🤖 Cliente LLM conversacional
    ├── __init__.py
    └── client.py     # 💭 Respostas naturais via OpenRouter

knowledge/            # 📚 Base de conhecimento jurídica
├── direito_constitucional/
├── direito_administrativo/
├── direito_penal/
├── direito_civil/
└── direito_processual/
```

### 🎭 Modo Conversacional

O bot opera em **modo conversacional inteligente**:

1. **👂 Escuta**: Monitora menções (@bot) e DMs
2. **🧠 Processa**: Usa RAG para buscar contexto relevante
3. **💭 Responde**: Gera respostas naturais e didáticas
4. **😊 Interage**: Mantém conversa fluida e amigável

**Vantagens:**
- ✅ Interação natural como conversar com um professor
- ✅ Sem barreiras técnicas (comandos, sintaxes)
- ✅ Respostas contextualizadas com a legislação
- ✅ Tratamento inteligente de dúvidas fora do escopo

## 💬 Exemplos de Uso

### 📚 Perguntas Educacionais
```
Usuário: @SamerPosterga O que é devido processo legal?

Bot: Olá! O devido processo legal é um princípio fundamental do direito constitucional brasileiro. Ele está previsto no art. 5º, LIV, da Constituição Federal:

"ninguém será privado da liberdade ou de seus bens sem o devido processo legal"

Na prática, isso significa que qualquer atuação do Estado que afete direitos individuais deve seguir um procedimento adequado, com contraditório e ampla defesa. É uma garantia contra arbitrariedades do poder público!

Quer que eu explique algum aspecto específico sobre isso? 🤔
```

### ⚖️ Consultas Jurídicas
```
Usuário: Me explica a diferença entre mandado de segurança e habeas corpus

Bot: Claro! Vamos lá:

**Habeas Corpus** (art. 5º, LXVIII, CF):
- Protege a liberdade de locomoção
- Usado contra prisão ou ameaça de prisão ilegal
- Prazo: 24 horas para impetração

**Mandado de Segurança** (art. 5º, LXIX, CF):
- Protege qualquer direito líquido e certo
- Mais amplo: pode ser contra atos de autoridade em geral
- Prazo: 120 dias para impetração

O HC é específico para liberdade, enquanto o MS vale para outros direitos. Ambos são ações constitucionais de proteção individual! 📖
```

## 🧪 Desenvolvimento

### 🛠️ Configuração com UV (Recomendado)

```bash
# Instale dependências incluindo dev
uv sync --dev

# Execute os testes
uv run pytest

# Verifique qualidade do código
uv run flake8 src/
uv run mypy src/
uv run black src/
uv run isort src/

# Execute o bot em modo desenvolvimento
uv run juridic-bot
```

### 📦 Desenvolvimento Tradicional

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

## 📞 Suporte e Comunidade

### 🆘 Precisa de Ajuda?
- 📧 **Email**: suporte@juridic-bot.com
- 🐛 **Issues**: [GitHub Issues](https://github.com/prof-ramos/SamerPosterga/issues)
- 📖 **Documentação**: [Wiki do Projeto](https://github.com/prof-ramos/SamerPosterga/wiki)
- 💬 **Discord**: Junte-se ao nosso servidor para discussões sobre direito e concursos

### 🤝 Como Contribuir

1. **Fork** o projeto
2. **Adicione documentos** na pasta `knowledge/`
3. **Teste** com suas dúvidas de concurso
4. **Abra uma Issue** com sugestões ou problemas
5. **Envie um PR** com melhorias

### 📊 Status do Projeto

- ✅ **Modo Conversacional**: Ativo e funcional
- ✅ **RAG System**: ChromaDB + OpenAI embeddings
- ✅ **LLM Integration**: OpenRouter (DeepSeek)
- ✅ **Documentos**: Constituição Federal incluída
- ✅ **Docker**: Multi-arch support
- ✅ **UV Package Manager**: Configurado

### 🎯 Roadmap

- [ ] Adicionar mais documentos jurídicos
- [ ] Implementar sistema de feedback das respostas
- [ ] Suporte a múltiplos idiomas
- [ ] Interface web para administração
- [ ] Integração com bases de jurisprudência

---

**⭐ Star este repositório** se está ajudando nos seus estudos para concursos! 📚✨

**Desenvolvido com ❤️ para estudantes de direito no Brasil** 🇧🇷