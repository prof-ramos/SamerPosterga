# 🤖 Bot Jurídico Conversacional

Assistente jurídico inteligente e amigável para estudantes de concursos públicos no Brasil. Funciona como um chatbot conversacional que responde naturalmente às suas dúvidas sobre direito.

## ✨ Características Principais

- **🤖 Chatbot Conversacional**: Interação natural via @menção ou DM, sem comandos complicados
- **🧠 RAG Inteligente**: Busca contextual em documentos jurídicos usando embeddings OpenAI
- **📚 Especialização Jurídica**: Foco nas principais áreas do Direito brasileiro para concursos
- **🎯 Respostas Didáticas**: Explicações claras e progressivas, como um professor experiente
- **⚡ Resposta Rápida**: Interface fluida sem barreiras técnicas
- **📄 Múltiplos Formatos**: Suporte a PDF, TXT, Markdown e DOCX
- **🔧 OpenRouter + OpenAI**: Modelos avançados (DeepSeek + embeddings) para respostas precisas

## 🚀 Início Rápido

=== "Docker (Recomendado)"
    ```bash
    git clone https://github.com/prof-ramos/SamerPosterga.git
    cd SamerPosterga
    cp .env.example .env
    # Edite o .env com suas chaves API
    docker-compose up -d
    ```

=== "UV Package Manager"
    ```bash
    git clone https://github.com/prof-ramos/SamerPosterga.git
    cd SamerPosterga
    uv sync
    cp .env.example .env
    # Edite o .env com suas chaves API
    uv run juridic-bot
    ```

=== "Pip Tradicional"
    ```bash
    git clone https://github.com/prof-ramos/SamerPosterga.git
    cd SamerPosterga
    pip install -r requirements.txt
    cp .env.example .env
    # Edite o .env com suas chaves API
    python -m src.juridic_bot.main
    ```

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

### 💡 Características das Respostas

- **📖 Explicações Didáticas**: Conceitos explicados passo a passo
- **📚 Baseadas em Documentos**: Respostas fundamentadas em legislação
- **🎯 Foco em Concursos**: Conteúdo relevante para provas
- **😊 Tom Amigável**: Como conversar com um professor experiente
- **⚡ Respostas Rápidas**: Sem complicações técnicas

## 📚 Exemplos de Uso

### 📖 Perguntas Educacionais
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
```

## 📊 Status do Projeto

- ✅ **Modo Conversacional**: Ativo e funcional
- ✅ **RAG System**: ChromaDB + OpenAI embeddings
- ✅ **LLM Integration**: OpenRouter (DeepSeek)
- ✅ **Documentos**: Constituição Federal incluída
- ✅ **Docker**: Multi-arch support (testado e funcionando)
- ✅ **UV Package Manager**: Configurado
- ✅ **Testes**: Testes funcionando com pytest-asyncio
- ✅ **Dependências**: Atualizadas e funcionais

## 🎓 Para Quem é Este Projeto

Este bot foi desenvolvido especialmente para:

- **📚 Estudantes de Direito**: Auxílio nos estudos para concursos públicos
- **⚖️ Candidatos a Concursos**: Preparação para provas da magistratura, ministério público, etc.
- **📖 Profissionais do Direito**: Consulta rápida sobre legislação brasileira
- **🎯 Concursandos**: Foco em questões práticas e conceituais

## 🤝 Contribuição

Contribuições são bem-vindas! Você pode ajudar de várias formas:

- **📄 Adicionando Documentos**: Inclua mais legislação na pasta `knowledge/`
- **🐛 Reportando Bugs**: Abra issues no GitHub
- **💡 Sugestões**: Compartilhe ideias para melhorar o bot
- **📝 Melhorando Documentação**: Ajude a tornar os docs mais claros
- **🔧 Código**: Contribua com melhorias no código

---

**⭐ Dê uma estrela no repositório se está ajudando nos seus estudos!**

**Desenvolvido com ❤️ para estudantes de direito no Brasil** 🇧🇷