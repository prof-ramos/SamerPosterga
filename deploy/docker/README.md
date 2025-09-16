# Deploy com Docker

Este diretório contém os arquivos para deploy usando Docker diretamente.

## Arquivos

- `Dockerfile` - Dockerfile otimizado para produção
- `docker-compose.yml` - Configuração para desenvolvimento local

## Uso

### Docker Compose (Desenvolvimento)

```bash
# Copiar e configurar variáveis
cp ../../.env.example .env
# Editar .env com suas credenciais

# Executar
docker-compose up -d

# Ver logs
docker-compose logs -f juridic-bot
```

### Docker Build Manual

```bash
# Build da imagem
docker build -f Dockerfile -t juridic-bot .

# Executar com variáveis
docker run -d \
  --name juridic-bot \
  -e DISCORD_TOKEN=seu_token \
  -e OPENAI_API_KEY=sua_key \
  -e OPENROUTER_API_KEY=sua_key \
  -v $(pwd)/knowledge:/app/knowledge \
  -v $(pwd)/.chroma:/app/.chroma \
  juridic-bot
```

### Imagem do DockerHub

```bash
# Usar imagem pré-construída
docker run -d \
  --name juridic-bot \
  -e DISCORD_TOKEN=seu_token \
  -e OPENAI_API_KEY=sua_key \
  -e OPENROUTER_API_KEY=sua_key \
  -v $(pwd)/knowledge:/app/knowledge \
  -v $(pwd)/.chroma:/app/.chroma \
  gabrielramosprof/juridic-bot:latest
```

## Características da Imagem

- **Multiarch**: Suporta AMD64 e ARM64
- **Otimizada**: Build multi-stage com UV package manager
- **Segura**: Usuario não-root, mínimas dependências
- **Pequena**: ~1.25GB comprimida
- **Health Check**: Monitoramento automático