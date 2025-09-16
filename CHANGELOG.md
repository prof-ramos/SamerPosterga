# Changelog

Todas as mudanças notáveis do projeto serão documentadas neste arquivo.

## [Atualização Docker] - 2025-09-16

### ✅ Corrigido
- **Docker Build Context**: Corrigido problema onde docker-compose precisava ser executado do diretório raiz (onde está `src/`) ao invés de `deploy/docker/`
- **Dependências**: Adicionado `langchain-chroma>=0.1.0` ao `requirements.txt` para corrigir `ModuleNotFoundError`
- **Rate Limiting**: Implementado sistema de modelos alternativos para lidar com rate limiting de APIs gratuitas

### 🔄 Alterado
- **Modelo Padrão**: DeepSeek Chat v3 (`deepseek/deepseek-chat-v3-0324`) como modelo principal recomendado
- **Estrutura Docker**: Dockerfile principal movido para raiz do projeto, mantendo compatibilidade com docker-compose

### 📚 Documentação
- **README.md**: Atualizado com instruções corretas de Docker, troubleshooting e modelos recomendados
- **CLAUDE.md**: Adicionada seção completa de troubleshooting e debug
- **Modelos OpenRouter**: Documentados modelos gratuitos e pagos com preços

### 🆕 Adicionado
- **Troubleshooting Guide**: Seção completa com soluções para problemas comuns:
  - Rate limiting (HTTP 429)
  - Dependências em falta
  - Container não inicia
  - Dockerfile context errors
  - Variáveis de ambiente
- **Comandos de Debug**: Lista de comandos úteis para desenvolvimento
- **Modelos Alternativos**: Lista de modelos OpenRouter como backup

### 📊 Modelos OpenRouter Recomendados

#### 🆓 Gratuitos (Ordem de Preferência)
1. `deepseek/deepseek-chat-v3-0324` - ✅ Principal
2. `meta-llama/llama-3.2-3b-instruct:free` - Backup estável
3. `google/gemini-2.0-flash-exp:free` - Alternativa

#### 💰 Pagos Baratos (<$1/1M tokens)
1. `deepseek/deepseek-chat` - ~$0.14/1M tokens
2. `qwen/qwen-2.5-7b-instruct` - ~$0.18/1M tokens
3. `mistralai/mistral-7b-instruct` - ~$0.25/1M tokens

### 🔧 Estrutura de Execução

```bash
# Estrutura correta para Docker
SamerPosterga/              # ← Executar docker-compose AQUI
├── src/                    # Código fonte
├── docker-compose.yml      # Configuração principal
├── Dockerfile             # Build do container
├── .env                   # Variáveis de ambiente
└── deploy/docker/         # Configurações adicionais
    ├── docker-compose.yml  # Backup/alternativo
    └── .env               # Configurações específicas
```

### 🐛 Bugs Conhecidos Resolvidos
- ❌ `ModuleNotFoundError: No module named 'langchain_chroma'`
- ❌ `COPY src/ ./src/: "/src": not found`
- ❌ Rate limiting constante em modelos gratuitos
- ❌ Container não carrega variáveis de ambiente

### 📈 Melhorias de Performance
- Modelo DeepSeek mais eficiente para textos jurídicos
- Sistema de fallback automático entre modelos
- Otimização de dependências Docker

---

## Como Usar Este Changelog

- **Desenvolvedores**: Consulte para entender mudanças na estrutura
- **Deploy**: Verifique antes de atualizar em produção
- **Troubleshooting**: Use a seção de bugs resolvidos para debug