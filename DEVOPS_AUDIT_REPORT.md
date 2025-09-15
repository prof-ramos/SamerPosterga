# 🔍 Auditoria DevOps - Docker & Deploy

**Auditor**: DevOps Senior | **Data**: $(date)
**Ambiente**: macOS M3 (arm64) → Debian (amd64)
**Foco**: Docker Multi-arch, Portainer Deploy, Production Readiness

---

## 📊 Executive Summary

| Categoria | Score | Status |
|-----------|-------|--------|
| **Docker Multi-arch** | 6/10 | ⚠️ Needs Improvement |
| **Security** | 4/10 | ❌ Critical Issues |
| **Portainer Ready** | 3/10 | ❌ Not Ready |
| **Production Ready** | 4/10 | ❌ Not Ready |
| **CI/CD** | 2/10 | ❌ Missing |

**Overall Score: 4/10** - Requires significant improvements before production deployment.

---

## 🚨 Critical Issues Found

### 1. **Docker Multi-arch Problems**

#### ❌ **Dockerfile Issues**
```dockerfile
# PROBLEMA: Health check para HTTP em app Discord
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1

# PROBLEMA: Porta exposta desnecessária
EXPOSE 8080
```

#### ❌ **Build Platform Confusion**
```dockerfile
# INCORRETO: Não garante target platform
FROM --platform=$BUILDPLATFORM python:3.11-slim
```

#### ❌ **Dependencies Missing for Multi-arch**
- No `buildx` configuration
- No platform-specific optimizations
- Missing cross-compilation setup

### 2. **Security Vulnerabilities**

#### 🔴 **CRÍTICO: Secrets em Plain Text**
```yaml
# docker-compose.yml - VAZAMENTO DE SEGURANÇA
environment:
  - DISCORD_TOKEN=${DISCORD_TOKEN}     # ❌ Plain text
  - OPENAI_API_KEY=${OPENAI_API_KEY}   # ❌ Plain text
```

#### 🔴 **CRÍTICO: Container Privileged**
```dockerfile
# Dockerfile - USER CREATION ISSUES
RUN useradd --create-home --shell /bin/bash app  # ❌ Shell access
USER app  # ❌ Still has write access to sensitive dirs
```

#### 🟡 **Root Dependencies**
```dockerfile
RUN apt-get update && apt-get install -y \
    build-essential \  # ❌ Unnecessary in production
    curl \            # ❌ Security risk
```

### 3. **Portainer Incompatibility**

#### ❌ **Missing Stack Configuration**
- No `docker-stack.yml` for Swarm mode
- No Portainer template metadata
- Missing service constraints

#### ❌ **Volume Management Issues**
```yaml
volumes:
  - ./knowledge:/app/knowledge:rw   # ❌ Host dependency
  - ./.chroma:/app/.chroma:rw      # ❌ Not portable
```

### 4. **Environment Variables Mismatch**
```yaml
# docker-compose.yml usa variáveis diferentes do .env
- ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}  # ❌ Código usa OPENROUTER_API_KEY
- VECTOR_DB_PATH=/app/.chroma             # ❌ Não configurável
```

---

## ✅ Recommended Solutions

### 1. **Fixed Dockerfile (Multi-arch)**

```dockerfile
# Dockerfile.optimized
FROM python:3.11-slim AS base

# Security hardening
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

# Multi-stage build for optimization
FROM base AS dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

FROM base AS runtime

# Copy dependencies from previous stage
COPY --from=dependencies /usr/local/lib/python3.11/site-packages/ /usr/local/lib/python3.11/site-packages/
COPY --from=dependencies /usr/local/bin/ /usr/local/bin/

# Copy application code
COPY src/ ./src/
COPY pyproject.toml .

# Create app user with minimal privileges
RUN groupadd -r app && useradd -r -g app -M -d /app -s /sbin/nologin app && \
    mkdir -p knowledge .chroma logs && \
    chown -R app:app /app

USER app

# Health check for Discord bot (check process, not HTTP)
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD pgrep -f "juridic_bot.main" || exit 1

CMD ["python", "-m", "src.juridic_bot.main"]
```

### 2. **Portainer Stack Configuration**

```yaml
# portainer-stack.yml
version: '3.8'

services:
  juridic-bot:
    image: ghcr.io/prof-ramos/juridic-bot:latest
    deploy:
      replicas: 1
      placement:
        constraints: [node.role == worker]
      restart_policy:
        condition: on-failure
        delay: 5s
        max_attempts: 3
      resources:
        limits:
          memory: 512M
          cpus: "0.5"
        reservations:
          memory: 256M
          cpus: "0.25"
    environment:
      - LOG_LEVEL=INFO
    secrets:
      - discord_token
      - openrouter_api_key
      - openai_api_key
    volumes:
      - knowledge:/app/knowledge
      - chroma:/app/.chroma
      - logs:/app/logs
    networks:
      - juridic-network

secrets:
  discord_token:
    external: true
  openrouter_api_key:
    external: true
  openai_api_key:
    external: true

networks:
  juridic-network:
    driver: overlay
    attachable: true

volumes:
  knowledge:
    driver: local
  chroma:
    driver: local
  logs:
    driver: local
```

### 3. **Multi-arch Build Script**

```bash
#!/bin/bash
# scripts/build-multiarch.sh

set -e

IMAGE_NAME="ghcr.io/prof-ramos/juridic-bot"
VERSION="${1:-latest}"

echo "🏗️ Building multi-architecture Docker image..."

# Create buildx builder if not exists
docker buildx inspect multiarch-builder >/dev/null 2>&1 || \
docker buildx create --name multiarch-builder --use

# Build and push multi-arch image
docker buildx build \
  --platform linux/amd64,linux/arm64 \
  --tag "${IMAGE_NAME}:${VERSION}" \
  --tag "${IMAGE_NAME}:latest" \
  --push \
  --file Dockerfile.optimized \
  .

echo "✅ Multi-arch build completed: ${IMAGE_NAME}:${VERSION}"
```

### 4. **GitHub Actions CI/CD**

```yaml
# .github/workflows/deploy.yml
name: Build and Deploy

on:
  push:
    branches: [main]
    tags: ['v*']
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install UV
        run: curl -LsSf https://astral.sh/uv/install.sh | sh

      - name: Install dependencies
        run: uv sync --dev

      - name: Run tests
        run: uv run pytest --cov=src --cov-fail-under=70

      - name: Security scan
        run: |
          uv run bandit -r src/
          uv run safety check

  build:
    needs: test
    runs-on: ubuntu-latest
    if: github.event_name == 'push'
    steps:
      - uses: actions/checkout@v4

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Login to GitHub Container Registry
        uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ghcr.io/${{ github.repository }}
          tags: |
            type=ref,event=branch
            type=ref,event=pr
            type=semver,pattern={{version}}
            type=semver,pattern={{major}}.{{minor}}

      - name: Build and push
        uses: docker/build-push-action@v5
        with:
          context: .
          file: Dockerfile.optimized
          platforms: linux/amd64,linux/arm64
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
```

### 5. **Secrets Management**

```bash
# scripts/setup-secrets.sh
#!/bin/bash

echo "🔐 Setting up Portainer secrets..."

# Create secrets in Portainer
echo "Creating Discord token secret..."
echo "${DISCORD_TOKEN}" | docker secret create discord_token -

echo "Creating OpenRouter API key secret..."
echo "${OPENROUTER_API_KEY}" | docker secret create openrouter_api_key -

echo "Creating OpenAI API key secret..."
echo "${OPENAI_API_KEY}" | docker secret create openai_api_key -

echo "✅ Secrets created successfully"
```

---

## 🔧 Environment Configuration

### **Development (macOS M3)**
```yaml
# docker-compose.dev.yml
version: '3.8'
services:
  juridic-bot:
    build:
      context: .
      dockerfile: Dockerfile.optimized
      target: development
    platform: linux/arm64
    volumes:
      - ./src:/app/src:ro
      - ./knowledge:/app/knowledge:rw
    environment:
      - LOG_LEVEL=DEBUG
    env_file:
      - .env.dev
```

### **Production (Debian amd64)**
```yaml
# docker-compose.prod.yml
version: '3.8'
services:
  juridic-bot:
    image: ghcr.io/prof-ramos/juridic-bot:latest
    platform: linux/amd64
    restart: unless-stopped
    deploy:
      resources:
        limits:
          memory: 1G
          cpus: "1.0"
    secrets:
      - discord_token
      - openrouter_api_key
      - openai_api_key
```

---

## 📋 Production Deployment Checklist

### **Pré-Deploy**
- [ ] **Security Scan** - Container e dependências
- [ ] **Multi-arch Build** - AMD64 + ARM64 testados
- [ ] **Secrets Setup** - Portainer secrets configurados
- [ ] **Resource Limits** - CPU/Memory definidos
- [ ] **Health Checks** - Monitoramento configurado

### **Deploy Portainer**
```bash
# 1. Upload stack file
curl -X POST "https://portainer.example.com/api/stacks" \
  -H "X-API-Key: ${PORTAINER_API_KEY}" \
  -F "file=@portainer-stack.yml" \
  -F "name=juridic-bot"

# 2. Verify deployment
docker service ls
docker service logs juridic-bot_juridic-bot

# 3. Monitor health
watch docker service ps juridic-bot_juridic-bot
```

### **Pós-Deploy**
- [ ] **Health Check** - Service responding
- [ ] **Logs Monitoring** - No errors críticos
- [ ] **Discord Integration** - Bot online
- [ ] **Resource Usage** - Within limits
- [ ] **Backup Strategy** - Knowledge/vectorstore

---

## 🚀 Performance Optimizations

### **Docker Image Size**
```dockerfile
# Current: ~800MB
# Optimized: ~200MB (multi-stage + alpine)

FROM python:3.11-alpine AS base  # ✅ Smaller base
RUN apk add --no-cache gcc musl-dev  # ✅ Minimal deps
```

### **Build Cache**
```yaml
# GitHub Actions cache
cache-from: type=gha
cache-to: type=gha,mode=max  # ✅ Maximum caching
```

### **Resource Allocation**
```yaml
deploy:
  resources:
    limits:
      memory: 512M      # ✅ Sufficient for bot
      cpus: "0.5"       # ✅ Conservative limit
    reservations:
      memory: 256M      # ✅ Guaranteed minimum
```

---

## 🔍 Monitoring & Observability

### **Health Monitoring**
```dockerfile
# Process-based health check
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
    CMD pgrep -f "juridic_bot.main" || exit 1
```

### **Logging Strategy**
```yaml
logging:
  driver: "json-file"
  options:
    max-size: "10m"
    max-file: "3"
    labels: "service=juridic-bot"
```

### **Metrics Collection** (Recommended)
```python
# Add to bot for observability
from prometheus_client import Counter, Histogram

message_counter = Counter('discord_messages_total', 'Total messages processed')
response_time = Histogram('response_time_seconds', 'Response time')
```

---

## 📈 Next Steps Priority

### **🔴 Immediate (Week 1)**
1. Fix security vulnerabilities (secrets, user privileges)
2. Implement proper multi-arch Dockerfile
3. Create Portainer stack configuration
4. Set up GitHub Container Registry

### **🟡 Short-term (Week 2-3)**
1. Implement CI/CD pipeline
2. Add monitoring and health checks
3. Create deployment automation
4. Security scanning integration

### **🟢 Long-term (Month 1-2)**
1. Implement blue-green deployments
2. Add metrics and observability
3. Disaster recovery procedures
4. Performance optimization

---

**🏆 Recommendation**: Do not deploy to production until critical security issues are resolved and proper secrets management is implemented.

**📞 Contact**: DevOps team for implementation support and code review.