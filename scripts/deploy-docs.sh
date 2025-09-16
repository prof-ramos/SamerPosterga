#!/bin/bash
# Script para deploy da documentação no GitHub Pages (pasta docs/)

set -e

echo "🚀 Fazendo deploy da documentação para GitHub Pages..."

# Verificar se uv está disponível
if ! command -v uv &> /dev/null; then
    echo "❌ UV não encontrado. Instale o UV primeiro."
    exit 1
fi

# Construir documentação
echo "📦 Construindo documentação..."
uv run mkdocs build

# Fazer backup dos arquivos fonte .md
echo "💾 Fazendo backup dos arquivos fonte..."
mkdir -p .docs_backup
find docs -name "*.md" -exec cp {} .docs_backup/ \;

# Copiar arquivos gerados para docs/
echo "📋 Copiando arquivos para pasta docs/..."
cp -r site/* docs/

# Restaurar arquivos fonte .md
echo "🔄 Restaurando arquivos fonte..."
cp .docs_backup/*.md docs/

# Limpar backup
rm -rf .docs_backup site/

echo "✅ Deploy concluído!"
echo "📁 Arquivos prontos na pasta docs/ para GitHub Pages"
echo ""
echo "Para ativar o GitHub Pages:"
echo "1. Vá para Settings > Pages no repositório"
echo "2. Selecione 'Deploy from a branch'"
echo "3. Escolha branch 'main' e folder '/docs'"
echo "4. Clique em Save"