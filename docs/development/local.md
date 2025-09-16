# Instalação Local

## Pré-requisitos

### Python 3.11+
- **Linux/macOS**: `python3 --version`
- **Windows**: Verificar se Python está no PATH durante a instalação

### UV Package Manager (Recomendado)
```bash
# Linux/macOS
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -ExecutionPolicy RemoteSigned -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### Chaves de API Necessárias
- **Discord Bot Token** ([Discord Developer Portal](https://discord.com/developers/applications))
- **OpenRouter API Key** ([OpenRouter](https://openrouter.ai/))
- **OpenAI API Key** ([OpenAI](https://platform.openai.com/api-keys))

## Instalação Rápida com UV

### 1. Clonar e configurar
```bash
git clone https://github.com/prof-ramos/SamerPosterga.git
cd SamerPosterga

# Instalar dependências
uv sync

# Configurar ambiente
cp .env.example .env
# Edite o .env com suas chaves API
```

### 2. Executar o bot
```bash
uv run juridic-bot
```

## Instalação Tradicional (pip)

### 1. Instalar Python e pip
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3.11 python3.11-venv

# macOS
brew install python@3.11

# Windows - usar setup.bat
```

### 2. Configurar ambiente virtual
```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
# venv\Scripts\activate   # Windows

pip install -r requirements.txt
```

### 3. Configurar e executar
```bash
cp .env.example .env
# Edite o .env com suas chaves API

python -m src.juridic_bot.main
```

## Verificação da Instalação

### Testar conectividade
```bash
# Verificar se bot responde
curl -s http://localhost:8080/health || echo "Bot não está respondendo"
```

### Verificar logs
```bash
tail -f logs/bot.log
```

## Próximos Passos

1. ✅ Instalação completa
2. [ ] Configurar bot no Discord
3. [ ] Adicionar documentos jurídicos
4. [ ] Testar funcionalidades

## Solução de Problemas

### Python não encontrado
```bash
# Verificar instalação
python --version
python3 --version

# Windows: verificar PATH
where python
```

### Erro de dependências
```bash
# Limpar cache e reinstalar
uv cache clean
uv sync --reinstall

# Ou com pip
pip uninstall -r requirements.txt -y
pip install -r requirements.txt
```

### Problemas de permissão
```bash
# Linux/macOS
chmod +x scripts/*
sudo chown -R $USER:$USER .

# Windows: executar como administrador
```

!!! tip "Dica"
    Se encontrar problemas na instalação, consulte a seção [Solução de Problemas](../solucao-problemas/comuns.md) para soluções específicas.