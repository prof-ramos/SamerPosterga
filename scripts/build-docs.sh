#!/bin/bash
# Script para build da documentação (apenas build, sem deploy)

set -e

echo "🏗️  Construindo documentação MkDocs..."

# Verificar se uv está disponível
if ! command -v uv &> /dev/null; then
    echo "❌ UV não encontrado. Instale o UV primeiro."
    exit 1
fi

# Construir documentação
uv run mkdocs build

# Verificar se build foi bem-sucedido
if [ $? -eq 0 ]; then
    echo "✅ Documentação construída com sucesso!"
    echo "📁 Arquivos gerados em: site/"
    echo ""
    echo "Para fazer deploy no GitHub Pages, execute:"
    echo "./scripts/deploy-docs.sh"
else
    echo "❌ Erro na construção da documentação"
    exit 1
fi