# 💻 Guia Específico para Windows

Este guia aborda questões específicas e soluções para usuários Windows.

## 🚀 Setup Rápido

### 1. Pré-requisitos

**Python 3.11+**
1. Baixe de: https://www.python.org/downloads/
2. ⚠️ **IMPORTANTE**: Marque "Add Python to PATH" durante a instalação
3. Reinicie o terminal após a instalação

**Git (opcional)**
- Baixe de: https://git-scm.com/download/win
- Ou use GitHub Desktop: https://desktop.github.com/

### 2. Scripts de Setup

**Opção A: Command Prompt (Recomendado para iniciantes)**
```cmd
setup.bat
```

**Opção B: PowerShell (Mais recursos)**
```powershell
# Setup básico
.\setup.ps1

# Setup com dependências de desenvolvimento
.\setup.ps1 -DevMode

# Setup apenas para Docker
.\setup.ps1 -UseDocker
```

## 🔧 Soluções para Problemas Comuns

### Erro: "python não é reconhecido"

**Solução 1: Verificar PATH**
```cmd
echo %PATH%
```
Se Python não estiver no PATH, adicione manualmente:
1. Abra "Variáveis de Ambiente" (Windows + R → sysdm.cpl → Avançado)
2. Adicione: `C:\Python311\` e `C:\Python311\Scripts\`

**Solução 2: Usar py launcher**
```cmd
py --version
py -m pip install --upgrade pip
```

### Erro: "Execution Policy" no PowerShell

```powershell
# Verificar política atual
Get-ExecutionPolicy

# Permitir scripts locais (como administrador)
Set-ExecutionPolicy RemoteSigned

# Ou apenas para sessão atual
Set-ExecutionPolicy Bypass -Scope Process
```

### Erro: "uv não é reconhecido"

**Instalar UV:**
```powershell
# Via pip
pip install uv

# Ou via PowerShell (Scoop)
iwr -useb get.scoop.sh | iex
scoop install uv
```

### Erro: Permissões de arquivo

**Se tiver problemas com permissões:**
```cmd
# Executar como administrador
# Ou dar permissões à pasta:
icacls "C:\caminho\para\SamerPosterga" /grant %USERNAME%:F /T
```

### Erro: "ModuleNotFoundError" após instalação

**Verificar ambiente virtual:**
```cmd
# Verificar se está ativo
where python
# Deve mostrar caminho dentro de .venv

# Ativar manualmente
.venv\Scripts\activate.bat
```

### Problemas com Docker

**Docker Desktop não iniciando:**
1. Habilitar virtualização na BIOS
2. Ativar WSL2: `wsl --install`
3. Reiniciar o sistema

**Docker build lento:**
- Fechar antivírus temporariamente
- Mover projeto para SSD se possível
- Usar WSL2 backend

## 🎯 Comandos Úteis para Windows

### Verificação de Sistema
```cmd
# Verificar versão do Windows
ver

# Verificar Python
python --version
py --version

# Verificar pip
python -m pip --version

# Verificar Docker
docker --version
docker-compose --version
```

### Limpeza e Reset
```cmd
# Limpar cache pip
pip cache purge

# Remover ambiente virtual
rmdir /s .venv

# Recriar ambiente
python -m venv .venv
```

### Logs e Debug
```cmd
# Ver logs do bot (se rodando)
type logs\bot.log

# Executar com debug
set LOG_LEVEL=DEBUG
python -m src.juridic_bot.main

# Docker logs
docker-compose logs -f juridic-bot
```

## 🐳 Docker no Windows

### Configuração Recomendada

**Docker Desktop Settings:**
- WSL2 backend habilitado
- File sharing configurado para drive do projeto
- Memory limit: pelo menos 4GB

### Comandos Docker Windows

```powershell
# Build (PowerShell)
docker-compose build

# Run em background
docker-compose up -d

# Logs em tempo real
docker-compose logs -f juridic-bot

# Parar
docker-compose down

# Reset completo
docker-compose down -v --rmi all
docker system prune -f
```

## ⚡ Dicas de Performance

### 1. Antivírus
- Adicione a pasta do projeto às exceções
- Exclua: `node_modules`, `.venv`, `.git`

### 2. Windows Defender
```powershell
# Adicionar exceção (como admin)
Add-MpPreference -ExclusionPath "C:\caminho\para\SamerPosterga"
```

### 3. WSL2 (Recomendado para desenvolvedores)
```bash
# Instalar WSL2
wsl --install

# Usar dentro do WSL2
cd /mnt/c/caminho/para/projeto
python -m venv .venv
source .venv/bin/activate
```

## 📁 Estrutura de Pastas Windows

```
SamerPosterga/
├── setup.bat              # ← Execute este
├── setup.ps1              # ← Ou este
├── .env                   # Suas chaves API
├── .venv/                 # Ambiente virtual Python
├── knowledge/             # Seus documentos PDF/TXT
├── .chroma/               # Base vetorial (automática)
├── logs/                  # Logs do bot
└── src/juridic_bot/       # Código do bot
```

## 🆘 Suporte

### Se nada funcionar:

1. **Desinstale e reinstale Python** com "Add to PATH"
2. **Use WSL2** (ambiente Linux no Windows)
3. **Use Docker** (mais isolado e confiável)
4. **Abra uma Issue** no GitHub com:
   - Versão do Windows (`ver`)
   - Versão do Python (`python --version`)
   - Mensagem de erro completa
   - Saída do comando que falhou

### Links Úteis

- **Python Windows**: https://docs.python.org/3/using/windows.html
- **Docker Desktop**: https://docs.docker.com/desktop/windows/
- **WSL2**: https://docs.microsoft.com/pt-br/windows/wsl/
- **PowerShell**: https://docs.microsoft.com/pt-br/powershell/

---

💡 **Dica**: Se estiver com muitos problemas no Windows, recomendamos usar o **Docker** que isola completamente o ambiente e evita conflitos de dependências!