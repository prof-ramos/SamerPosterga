# 🚀 Guia de Deploy - Bot Jurídico para Concursos

Este guia explica como fazer o deploy do bot usando Docker em diferentes ambientes.

## 📋 Pré-requisitos

- Docker e Docker Compose instalados
- Arquivo `.env` configurado com as chaves necessárias
- Pelo menos 2GB de espaço em disco disponível

## ⚡ Deploy Rápido

### 1. Configurar ambiente

```bash
# Copiar arquivo de exemplo
cp .env.example .env

# Editar com suas chaves
nano .env
```

### 2. Build e execução

```bash
# Build da imagem
docker-compose build

# Executar o bot
docker-compose up -d

# Ver logs
docker-compose logs -f juridic-bot
```

### 3. Parar o bot

```bash
# Parar execução
docker-compose down

# Parar e remover volumes
docker-compose down -v
```

## 🏗️ Build Multi-Arquitetura

Para build em múltiplas plataformas (útil para deploy em diferentes servidores):

```bash
# Build para múltiplas plataformas
docker buildx build --platform linux/amd64,linux/arm64 -t juridic-bot:latest .

# Push para registry
docker buildx build --platform linux/amd64,linux/arm64 -t your-registry/juridic-bot:latest --push .
```

## 📁 Estrutura de Volumes

O Docker Compose configura volumes persistentes:

- `knowledge/` - Base de conhecimento jurídica
- `.chroma/` - Banco de dados vetorial
- `logs/` - Arquivos de log

## 🔧 Configuração Avançada

### Variáveis de Ambiente

| Variável | Descrição | Padrão |
|----------|-----------|---------|
| `DISCORD_TOKEN` | Token do bot Discord | *obrigatório* |
| `OPENAI_API_KEY` | Chave da OpenAI | *obrigatório* |
| `VECTOR_DB_PATH` | Caminho do banco vetorial | `.chroma` |
| `KNOWLEDGE_PATH` | Caminho da base de conhecimento | `knowledge` |
| `LOG_LEVEL` | Nível de log | `INFO` |

### Health Check

O container inclui health check automático:

```bash
# Verificar status
docker-compose ps

# Health check manual
docker-compose exec juridic-bot python -c "print('Bot is healthy')"
```

## 🌐 Deploy em Produção

### Usando Docker Swarm

```bash
# Inicializar swarm
docker swarm init

# Deploy como stack
docker stack deploy -c docker-compose.yml juridic-stack

# Ver serviços
docker stack services juridic-stack
```

### Usando Kubernetes

```yaml
# Exemplo de deployment
apiVersion: apps/v1
kind: Deployment
metadata:
  name: juridic-bot
spec:
  replicas: 1
  selector:
    matchLabels:
      app: juridic-bot
  template:
    metadata:
      labels:
        app: juridic-bot
    spec:
      containers:
      - name: juridic-bot
        image: juridic-bot:latest
        envFrom:
        - secretRef:
            name: juridic-bot-secrets
        volumeMounts:
        - name: knowledge
          mountPath: /app/knowledge
        - name: chroma
          mountPath: /app/.chroma
      volumes:
      - name: knowledge
        persistentVolumeClaim:
          claimName: knowledge-pvc
      - name: chroma
        persistentVolumeClaim:
          claimName: chroma-pvc
```

## 📊 Monitoramento

### Logs

```bash
# Ver logs em tempo real
docker-compose logs -f

# Filtrar logs por nível
docker-compose logs | grep ERROR

# Salvar logs
docker-compose logs > bot_logs.txt
```

### Recursos

```bash
# Ver uso de recursos
docker stats

# Inspecionar container
docker inspect juridic-bot
```

## 🔒 Segurança

### Recomendações

1. **Nunca commite o arquivo `.env`** - Use `.env.example` como template
2. **Use secrets no Docker Swarm/K8s** - Não passe chaves como variáveis de ambiente
3. **Configure firewall** - Limite acesso às portas necessárias
4. **Monitore logs** - Configure rotação de logs automática

### Secrets no Docker

```bash
# Criar secrets
echo "your_discord_token" | docker secret create discord_token -
echo "your_openai_key" | docker secret create openai_key -

# Usar no compose
version: '3.8'
services:
  juridic-bot:
    secrets:
      - discord_token
      - openai_key
secrets:
  discord_token:
    external: true
  openai_key:
    external: true
```

## 🐛 Troubleshooting

### Problemas Comuns

**Erro: "No module named 'config'"**
```bash
# Verificar se está no diretório correto
pwd
# Deve estar em: /path/to/SamerPosterga

# Verificar estrutura
ls -la src/
```

**Erro: "Permission denied"**
```bash
# Ajustar permissões
sudo chown -R $USER:$USER .
chmod +x docker-compose.yml
```

**Erro: "Port already in use"**
```bash
# Verificar portas em uso
docker ps
docker-compose down

# Ou mudar porta no compose
ports:
  - "8081:8080"
```

**Bot não responde no Discord**
```bash
# Verificar logs
docker-compose logs juridic-bot

# Verificar token
docker-compose exec juridic-bot env | grep DISCORD
```

## 📞 Suporte

Para problemas específicos:

1. Verifique os logs do container
2. Confirme se todas as variáveis estão configuradas
3. Teste localmente antes do deploy
4. Verifique conectividade de rede

---

**🎯 Dica**: Sempre teste em ambiente de desenvolvimento antes do deploy em produção!