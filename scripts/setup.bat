@echo off
:: =============================================================================
:: Bot Jurídico Conversacional - Setup para Windows (Command Prompt)
:: =============================================================================

echo.
echo ========================================
echo   Bot Jurídico Conversacional - Setup
echo ========================================
echo.

:: Verificar se Python está instalado
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python não encontrado!
    echo.
    echo Por favor, instale Python 3.11+ antes de continuar:
    echo https://www.python.org/downloads/
    pause
    exit /b 1
)

echo ✅ Python encontrado
python --version

:: Verificar versão do Python
for /f "tokens=2 delims= " %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo Versão do Python: %PYTHON_VERSION%

:: Verificar se é Python 3.11+
python -c "import sys; exit(0 if sys.version_info >= (3, 11) else 1)" >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python 3.11+ é necessário!
    echo Sua versão: %PYTHON_VERSION%
    pause
    exit /b 1
)

echo.
echo 📦 Verificando gerenciadores de pacote...

:: Tentar usar UV primeiro (recomendado)
uv --version >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ UV encontrado - usando UV para instalação
    goto install_with_uv
)

:: Fallback para pip
echo ℹ️  UV não encontrado, usando pip tradicional
goto install_with_pip

:install_with_uv
echo.
echo 🚀 Instalando dependências com UV...
uv sync
if %errorlevel% neq 0 (
    echo ❌ Erro ao instalar dependências com UV
    pause
    exit /b 1
)

echo.
echo 🧪 Instalando dependências de desenvolvimento...
uv sync --dev
goto setup_env

:install_with_pip
echo.
echo 📦 Criando ambiente virtual...
python -m venv .venv
if %errorlevel% neq 0 (
    echo ❌ Erro ao criar ambiente virtual
    pause
    exit /b 1
)

echo.
echo 🔄 Ativando ambiente virtual...
call .venv\Scripts\activate.bat

echo.
echo 📦 Atualizando pip...
python -m pip install --upgrade pip

echo.
echo 🚀 Instalando dependências...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ❌ Erro ao instalar dependências
    pause
    exit /b 1
)

echo.
echo 🧪 Instalando dependências de desenvolvimento...
pip install -e ".[dev]"

:setup_env
echo.
echo ⚙️  Configurando arquivo de ambiente...

:: Verificar se .env já existe
if exist .env (
    echo ℹ️  Arquivo .env já existe
    set /p overwrite="Deseja sobrescrever? (s/N): "
    if /i not "%overwrite%"=="s" if /i not "%overwrite%"=="sim" (
        echo ✅ Mantendo arquivo .env existente
        goto create_dirs
    )
)

:: Copiar .env.example para .env
if exist .env.example (
    copy .env.example .env >nul
    echo ✅ Arquivo .env criado a partir de .env.example
) else (
    echo.
    echo 📝 Criando arquivo .env básico...
    (
        echo # Discord Configuration
        echo DISCORD_TOKEN=seu_discord_bot_token_aqui
        echo DISCORD_APP_ID=seu_app_id_aqui
        echo DISCORD_GUILD_ID=
        echo DISCORD_OWNER_ID=seu_user_id_para_comandos_admin
        echo.
        echo # OpenRouter Configuration ^(LLM principal^)
        echo OPENROUTER_API_KEY=sua_openrouter_api_key_aqui
        echo OPENROUTER_MODEL=deepseek/deepseek-chat-v3-0324
        echo OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
        echo.
        echo # OpenAI Configuration ^(para embeddings^)
        echo OPENAI_API_KEY=sua_openai_api_key_aqui
        echo EMBEDDING_MODEL=text-embedding-3-small
        echo.
        echo # RAG Configuration
        echo TOP_K=5
        echo CHUNK_SIZE=1500
        echo CHUNK_OVERLAP=200
        echo.
        echo # System Configuration
        echo MAX_TOKENS=2000
        echo TEMPERATURE=0.7
        echo LOG_LEVEL=INFO
    ) > .env
    echo ✅ Arquivo .env criado
)

:create_dirs
echo.
echo 📁 Criando diretórios necessários...
if not exist knowledge mkdir knowledge
if not exist .chroma mkdir .chroma
if not exist logs mkdir logs

echo ✅ Diretórios criados

:test_installation
echo.
echo 🧪 Testando instalação...

:: Verificar se consegue importar módulos principais
python -c "import sys; import discord; import openai; import chromadb; print('✅ Módulos principais importados com sucesso')" 2>nul
if %errorlevel% neq 0 (
    echo ❌ Erro ao importar módulos. Verificando dependências...
    python -c "import discord" 2>nul || echo ❌ discord.py não encontrado
    python -c "import openai" 2>nul || echo ❌ openai não encontrado
    python -c "import chromadb" 2>nul || echo ❌ chromadb não encontrado
    echo.
    echo Tente reinstalar as dependências manualmente.
    pause
    exit /b 1
)

:: Testar se consegue importar o bot
python -c "from src.juridic_bot.config import Config; print('✅ Configuração carregada')" 2>nul
if %errorlevel% neq 0 (
    echo ❌ Erro ao carregar configuração do bot
    echo Verifique se o código fonte está na pasta src/
    pause
    exit /b 1
)

echo.
echo 🎉 ===========================================
echo    INSTALAÇÃO CONCLUÍDA COM SUCESSO!
echo ===========================================
echo.
echo 📋 Próximos passos:
echo.
echo 1. 🔧 Configure suas chaves API no arquivo .env:
echo    - DISCORD_TOKEN (obrigatório)
echo    - OPENROUTER_API_KEY (obrigatório)
echo    - OPENAI_API_KEY (obrigatório)
echo.
echo 2. 📚 Adicione documentos jurídicos na pasta knowledge/
echo.
echo 3. 🚀 Execute o bot:

:: Mostrar comando baseado no método de instalação usado
uv --version >nul 2>&1
if %errorlevel% equ 0 (
    echo    uv run juridic-bot
) else (
    echo    .venv\Scripts\activate.bat
    echo    python -m src.juridic_bot.main
)

echo.
echo 4. 🐳 Ou use Docker (recomendado):
echo    docker-compose up -d
echo.
echo 📖 Documentação completa no README.md
echo.
echo ✨ Bons estudos para seus concursos jurídicos!
echo.

pause