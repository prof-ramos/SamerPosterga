# Script de teste para validar a instalação
# Execute: .\test-setup.ps1

Write-Host "🧪 Testando instalação do Bot Jurídico..." -ForegroundColor Cyan

# Testar Python
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ Python: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python não encontrado" -ForegroundColor Red
}

# Testar imports
$modules = @("discord", "openai", "chromadb", "langchain", "dotenv")
foreach ($module in $modules) {
    try {
        $result = python -c "import $module; print('OK')" 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✅ $module importado" -ForegroundColor Green
        } else {
            Write-Host "❌ $module falhou" -ForegroundColor Red
        }
    } catch {
        Write-Host "❌ $module erro" -ForegroundColor Red
    }
}

# Testar configuração
if (Test-Path ".env") {
    Write-Host "✅ Arquivo .env encontrado" -ForegroundColor Green
} else {
    Write-Host "⚠️ Arquivo .env não encontrado" -ForegroundColor Yellow
}

# Testar diretórios
$dirs = @("knowledge", ".chroma", "logs", "src")
foreach ($dir in $dirs) {
    if (Test-Path $dir) {
        Write-Host "✅ Diretório $dir encontrado" -ForegroundColor Green
    } else {
        Write-Host "❌ Diretório $dir não encontrado" -ForegroundColor Red
    }
}

Write-Host "`n🎯 Teste concluído!" -ForegroundColor Cyan