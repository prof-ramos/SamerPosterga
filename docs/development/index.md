# Instalação - Visão Geral

Esta seção guia você através de todas as formas de instalar e executar o Bot Jurídico Conversacional.

## Métodos de Instalação

### 🚀 Instalação Rápida
Para começar rapidamente, recomendamos usar Docker:

```bash
git clone https://github.com/prof-ramos/SamerPosterga.git
cd SamerPosterga
cp .env.example .env
# Edite o .env com suas chaves API
docker-compose up -d
```

### 📋 Pré-requisitos Gerais

Antes de qualquer instalação, você precisará de:

- **Chaves de API**:
  - Discord Bot Token ([Discord Developer Portal](https://discord.com/developers/applications))
  - OpenRouter API Key ([OpenRouter](https://openrouter.ai/))
  - OpenAI API Key ([OpenAI](https://platform.openai.com/api-keys))

- **Sistema operacional** compatível:
  - Linux (Ubuntu 20.04+, Debian 11+)
  - macOS (10.15+)
  - Windows (10/11 com WSL recomendado)

## Escolhendo o Método de Instalação

| Método | Dificuldade | Plataformas | Recomendado para |
|--------|-------------|-------------|------------------|
| **Docker** | ⭐⭐ | Linux/macOS/Windows | Produção, desenvolvimento |
| **UV** | ⭐⭐⭐ | Linux/macOS/Windows | Desenvolvimento rápido |
| **Pip** | ⭐⭐⭐⭐ | Linux/macOS/Windows | Desenvolvimento avançado |
| **Windows** | ⭐⭐⭐ | Windows | Usuários Windows |

## Próximos Passos

Escolha o método que melhor se adapta ao seu ambiente:

- [Instalação Local](local.md) - Para desenvolvimento local
- [Docker](docker.md) - Para produção e desenvolvimento
- [Windows](windows.md) - Setup específico para Windows
- [Ambiente de Desenvolvimento](desenvolvimento.md) - Para contribuidores

!!! tip "Dica"
    Se você é novo no projeto, comece com a [Instalação Local](local.md) para entender como funciona.