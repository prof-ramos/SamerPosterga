# Implantação em VPS com Portainer

## Arquitetura Recomendada

### VPS com Portainer
```
VPS (2GB RAM, 2 vCPUs)
├── Portainer CE (Gerenciamento de Containers)
├── Bot Jurídico (Container)
├── Nginx Proxy Manager (Opcional)
└── Watchtower (Atualizações Automáticas)
```

## Pré-requisitos

### Servidor VPS
- Ubuntu 22.04+ ou Debian 12+
- Pelo menos 2GB RAM
- Docker e Docker Compose instalados

### Configuração Inicial
```bash
# Instalar Docker
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker $USER

# Instalar Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

## Instalação do Portainer

### 1. Criar rede Docker
```bash
docker network create portainer-net
```

### 2. Executar Portainer
```bash
docker run -d \
  -p 8000:8000 \
  -p 9443:9443 \
  --name portainer \
  --restart=always \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v portainer_data:/data \
  --network portainer-net \
  portainer/portainer-ce:latest
```

### 3. Acessar Portainer
- **URL**: `https://seu-vps-ip:9443`
- Criar usuário admin na primeira vez

## Implantação do Bot Jurídico

### 1. Preparar Secrets
```bash
# No Portainer, ir para Secrets
# Criar os seguintes secrets:

# discord_token
# openrouter_api_key
# openai_api_key
```

### 2. Criar Stack
```bash
# No Portainer: Stacks > Add Stack
# Nome: juridic-bot
# Método: Upload
# Fazer upload do arquivo: deploy/portainer-stack.yml
```

### 3. Configurar Variáveis de Ambiente
```bash
# Na stack, adicionar variáveis de ambiente:
LOG_LEVEL=INFO
VECTOR_DB_PATH=/data/.chroma
KNOWLEDGE_PATH=/data/knowledge
```

### 4. Implantar a Stack
```bash
# Clicar em "Deploy the stack"
# Aguardar conclusão da implantação
```

## Configuração Avançada

### Volumes Persistentes
```yaml
# No portainer-stack.yml, volumes são automaticamente criados:
volumes:
  knowledge:
    driver: local
  chroma:
    driver: local
  logs:
    driver: local
```

### Health Checks
```yaml
# Health check automático configurado:
healthcheck:
  test: ["CMD", "pgrep", "-f", "juridic_bot.main"]
  interval: 30s
  timeout: 10s
  retries: 3
  start_period: 40s
```

### Limites de Recursos
```yaml
# Limites de recursos:
deploy:
  resources:
    limits:
      memory: 512M
      cpus: "0.5"
    reservations:
      memory: 256M
      cpus: "0.25"
```

## Monitoramento com Portainer

### Dashboard
- **Containers**: Status de todos os containers
- **Images**: Imagens Docker utilizadas
- **Volumes**: Espaço em disco usado
- **Networks**: Conectividade

### Logs
```bash
# No Portainer: Containers > juridic-bot > Logs
# Visualizar logs em tempo real
# Filtrar por nível de severidade
```

### Métricas
```bash
# Containers > juridic-bot > Stats
# CPU, memória, rede, I/O
```

## Atualização Automática

### Configurar Watchtower
```yaml
# Adicionar à stack:
services:
  watchtower:
    image: containrrr/watchtower
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
    command: --interval 3600 --cleanup
    restart: unless-stopped
```

## Backup e Restauração

### Backup Automático
```bash
# Criar script de backup
cat > /opt/backup-juridic.sh << 'EOF'
#!/bin/bash
BACKUP_DIR="/opt/backups"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR

# Backup volumes
docker run --rm -v juridic-bot_knowledge:/data -v $BACKUP_DIR:/backup alpine tar czf /backup/knowledge_$DATE.tar.gz -C / data
docker run --rm -v juridic-bot_chroma:/data -v $BACKUP_DIR:/backup alpine tar czf /backup/chroma_$DATE.tar.gz -C / data

# Limpar backups antigos (manter últimos 7 dias)
find $BACKUP_DIR -name "*.tar.gz" -mtime +7 -delete

echo "Backup concluído: $DATE"
EOF

chmod +x /opt/backup-juridic.sh
```

### Agendar Backup
```bash
# Adicionar ao crontab
crontab -e

# Executar backup diariamente às 2:00
0 2 * * * /opt/backup-juridic.sh
```

## Segurança

### Configurações Essenciais
```bash
# Configurar firewall
sudo ufw allow 9443/tcp  # Portainer HTTPS
sudo ufw allow 8000/tcp  # Portainer HTTP (opcional)
sudo ufw --force enable

# SSL para Portainer (recomendado)
# Portainer > Settings > SSL Certificate
```

### Acesso Seguro
```bash
# Usar HTTPS sempre
# Configurar autenticação 2FA no Portainer
# Limitar acesso IP se possível
```

## Solução de Problemas

### Container não inicia
```bash
# Verificar logs no Portainer
# Containers > juridic-bot > Logs

# Verificar secrets
# Stacks > juridic-bot > Editor
# Confirmar que secrets estão corretos
```

### Problemas de performance
```bash
# Verificar recursos
# Containers > juridic-bot > Stats

# Ajustar limites se necessário
# Stacks > juridic-bot > Editor
# Modificar seção resources
```

### Rede não funciona
```bash
# Verificar conectividade
docker network ls
docker network inspect juridic-bot_juridic-network

# Recriar rede se necessário
docker network rm juridic-bot_juridic-network
# Rede será recriada no próximo deploy
```

## Migração de Implantação Manual

### De Docker Compose para Portainer
1. **Backup**: Fazer backup completo dos dados
2. **Parar**: `docker-compose down`
3. **Secrets**: Criar secrets no Portainer
4. **Stack**: Upload do portainer-stack.yml
5. **Implantar**: Executar stack no Portainer
6. **Testar**: Verificar funcionamento
7. **Cleanup**: Remover containers antigos

### Rollback
```bash
# Se algo der errado, rollback para Docker Compose
cd /opt/SamerPosterga
docker-compose up -d
```

!!! warning "Atenção"
    Sempre faça backup antes de qualquer migração ou atualização crítica.

!!! tip "Dica"
    Use o Portainer para facilitar o gerenciamento diário dos containers e monitoramento do sistema.