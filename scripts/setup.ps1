# =============================================================================
# Bot Jurídico Conversacional - Setup para Windows (PowerShell)
# =============================================================================

param(
    [switch]$SkipPythonCheck,
    [switch]$UseDocker,
    [switch]$DevMode
)

# Configurar cores para output
$Host.UI.RawUI.WindowTitle = "Bot Jurídico - Setup"

function Write-ColorOutput {
    param(
        [string]$Message,
        [string]$Color = "White"
    )
    Write-Host $Message -ForegroundColor $Color
}

function Write-Header {
    param([string]$Title)
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host "   $Title" -ForegroundColor Cyan
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host ""
}

function Write-Success {
    param([string]$Message)
    Write-Host "✅ $Message" -ForegroundColor Green
}

function Write-Error {
    param([string]$Message)
    Write-Host "❌ $Message" -ForegroundColor Red
}

function Write-Info {
    param([string]$Message)
    Write-Host "ℹ️  $Message" -ForegroundColor Yellow
}

function Write-Step {
    param([string]$Message)
    Write-Host "🔄 $Message" -ForegroundColor Blue
}

# Verificar se está executando como administrador
function Test-IsAdmin {
    $currentPrincipal = New-Object Security.Principal.WindowsPrincipal([Security.Principal.WindowsIdentity]::GetCurrent())
    return $currentPrincipal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
}

try {
    Write-Header "Bot Jurídico Conversacional - Setup"

    # Verificar Python
    if (-not $SkipPythonCheck) {
        Write-Step "Verificando Python..."

        try {
            $pythonVersion = python --version 2>&1
            if ($LASTEXITCODE -ne 0) {
                throw "Python não encontrado"
            }

            Write-Success "Python encontrado: $pythonVersion"

            # Verificar versão Python 3.11+
            $versionCheck = python -c "import sys; exit(0 if sys.version_info >= (3, 11) else 1)" 2>&1
            if ($LASTEXITCODE -ne 0) {
                throw "Python 3.11+ é necessário. Versão atual: $pythonVersion"
            }

        } catch {
            Write-Error "Python não encontrado ou versão incompatível!"
            Write-Info "Instale Python 3.11+ de: https://www.python.org/downloads/"
            Write-Info "Certifique-se de marcar 'Add Python to PATH' durante a instalação"
            Read-Host "Pressione Enter para sair"
            exit 1
        }
    }

    # Verificar se deve usar Docker
    if ($UseDocker) {
        Write-Step "Configurando para uso com Docker..."

        # Verificar se Docker está instalado
        try {
            $dockerVersion = docker --version 2>&1
            if ($LASTEXITCODE -ne 0) {
                throw "Docker não encontrado"
            }
            Write-Success "Docker encontrado: $dockerVersion"
        } catch {
            Write-Error "Docker não encontrado!"
            Write-Info "Instale Docker Desktop de: https://www.docker.com/products/docker-desktop/"
            Read-Host "Pressione Enter para sair"
            exit 1
        }

        # Verificar docker-compose
        try {
            $composeVersion = docker-compose --version 2>&1
            if ($LASTEXITCODE -ne 0) {
                throw "docker-compose não encontrado"
            }
            Write-Success "Docker Compose encontrado: $composeVersion"
        } catch {
            Write-Error "Docker Compose não encontrado!"
            Write-Info "Docker Compose está incluído no Docker Desktop"
            Read-Host "Pressione Enter para sair"
            exit 1
        }
    }

    # Verificar gerenciadores de pacote
    Write-Step "Verificando gerenciadores de pacote..."

    $useUV = $false
    try {
        $uvVersion = uv --version 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Success "UV encontrado: $uvVersion"
            $useUV = $true
        }
    } catch {
        Write-Info "UV não encontrado, usando pip tradicional"
    }

    # Instalação com UV
    if ($useUV -and -not $UseDocker) {
        Write-Step "Instalando dependências com UV..."

        uv sync
        if ($LASTEXITCODE -ne 0) {
            throw "Erro ao instalar dependências com UV"
        }

        if ($DevMode) {
            Write-Step "Instalando dependências de desenvolvimento..."
            uv sync --dev
        }
    }

    # Instalação com pip
    if (-not $useUV -and -not $UseDocker) {
        Write-Step "Configurando ambiente virtual..."

        # Criar ambiente virtual
        python -m venv .venv
        if ($LASTEXITCODE -ne 0) {
            throw "Erro ao criar ambiente virtual"
        }

        # Ativar ambiente virtual
        Write-Step "Ativando ambiente virtual..."
        & ".\.venv\Scripts\Activate.ps1"

        # Atualizar pip
        Write-Step "Atualizando pip..."
        python -m pip install --upgrade pip

        # Instalar dependências
        Write-Step "Instalando dependências..."
        if (Test-Path "requirements.txt") {
            pip install -r requirements.txt
        } else {
            pip install -e .
        }

        if ($LASTEXITCODE -ne 0) {
            throw "Erro ao instalar dependências"
        }

        if ($DevMode) {
            Write-Step "Instalando dependências de desenvolvimento..."
            pip install -e ".[dev]"
        }
    }

    # Configurar arquivo de ambiente
    Write-Step "Configurando arquivo de ambiente..."

    if (Test-Path ".env") {
        Write-Info "Arquivo .env já existe"
        $overwrite = Read-Host "Deseja sobrescrever? (s/N)"
        if ($overwrite -ne "s" -and $overwrite -ne "sim") {
            Write-Success "Mantendo arquivo .env existente"
        } else {
            Copy-Item ".env.example" ".env" -Force
            Write-Success "Arquivo .env atualizado"
        }
    } else {
        if (Test-Path ".env.example") {
            Copy-Item ".env.example" ".env"
            Write-Success "Arquivo .env criado a partir de .env.example"
        } else {
            # Criar .env básico
            $envContent = @"
# Discord Configuration
DISCORD_TOKEN=seu_discord_bot_token_aqui
DISCORD_APP_ID=seu_app_id_aqui
DISCORD_GUILD_ID=
DISCORD_OWNER_ID=seu_user_id_para_comandos_admin

# OpenRouter Configuration (LLM principal)
OPENROUTER_API_KEY=sua_openrouter_api_key_aqui
OPENROUTER_MODEL=deepseek/deepseek-chat-v3-0324
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1

# OpenAI Configuration (para embeddings)
OPENAI_API_KEY=sua_openai_api_key_aqui
EMBEDDING_MODEL=text-embedding-3-small

# RAG Configuration
TOP_K=5
CHUNK_SIZE=1500
CHUNK_OVERLAP=200

# System Configuration
MAX_TOKENS=2000
TEMPERATURE=0.7
LOG_LEVEL=INFO
"@
            $envContent | Out-File -FilePath ".env" -Encoding UTF8
            Write-Success "Arquivo .env criado"
        }
    }

    # Criar diretórios necessários
    Write-Step "Criando diretórios necessários..."

    $directories = @("knowledge", ".chroma", "logs")
    foreach ($dir in $directories) {
        if (-not (Test-Path $dir)) {
            New-Item -ItemType Directory -Path $dir | Out-Null
        }
    }
    Write-Success "Diretórios criados"

    # Testes de instalação (apenas se não for Docker)
    if (-not $UseDocker) {
        Write-Step "Testando instalação..."

        # Testar imports principais
        $testResult = python -c "import discord, openai, chromadb; print('Módulos OK')" 2>&1
        if ($LASTEXITCODE -ne 0) {
            Write-Error "Erro ao importar módulos principais"
            Write-Info "Teste individual:"
            python -c "import discord" 2>&1; if ($LASTEXITCODE -ne 0) { Write-Error "discord.py não encontrado" }
            python -c "import openai" 2>&1; if ($LASTEXITCODE -ne 0) { Write-Error "openai não encontrado" }
            python -c "import chromadb" 2>&1; if ($LASTEXITCODE -ne 0) { Write-Error "chromadb não encontrado" }
            throw "Falha nos testes de módulos"
        }

        # Testar configuração do bot
        $configTest = python -c "from src.juridic_bot.config import Config; print('Config OK')" 2>&1
        if ($LASTEXITCODE -ne 0) {
            Write-Error "Erro ao carregar configuração do bot"
            throw "Falha no teste de configuração"
        }

        Write-Success "Todos os testes passaram!"
    }

    # Sucesso!
    Write-Host ""
    Write-Host "🎉 ===========================================" -ForegroundColor Green
    Write-Host "    INSTALAÇÃO CONCLUÍDA COM SUCESSO!" -ForegroundColor Green
    Write-Host "===========================================" -ForegroundColor Green
    Write-Host ""

    Write-Host "📋 Próximos passos:" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "1. 🔧 Configure suas chaves API no arquivo .env:" -ForegroundColor White
    Write-Host "   - DISCORD_TOKEN (obrigatório)" -ForegroundColor Gray
    Write-Host "   - OPENROUTER_API_KEY (obrigatório)" -ForegroundColor Gray
    Write-Host "   - OPENAI_API_KEY (obrigatório)" -ForegroundColor Gray
    Write-Host ""
    Write-Host "2. 📚 Adicione documentos jurídicos na pasta knowledge/" -ForegroundColor White
    Write-Host ""
    Write-Host "3. 🚀 Execute o bot:" -ForegroundColor White

    if ($UseDocker) {
        Write-Host "   docker-compose up -d" -ForegroundColor Green
    } elseif ($useUV) {
        Write-Host "   uv run juridic-bot" -ForegroundColor Green
    } else {
        Write-Host "   .\.venv\Scripts\Activate.ps1" -ForegroundColor Green
        Write-Host "   python -m src.juridic_bot.main" -ForegroundColor Green
    }

    Write-Host ""
    Write-Host "📖 Documentação completa no README.md" -ForegroundColor White
    Write-Host ""
    Write-Host "✨ Bons estudos para seus concursos jurídicos!" -ForegroundColor Yellow
    Write-Host ""

} catch {
    Write-Host ""
    Write-Error "Erro durante a instalação: $($_.Exception.Message)"
    Write-Host ""
    Write-Info "Verifique os pré-requisitos e tente novamente"
    Write-Host ""
} finally {
    if (-not $env:CI) {
        Read-Host "Pressione Enter para sair"
    }
}