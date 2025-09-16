#!/bin/bash
# Script para servir documentação localmente

set -e

echo "🚀 Servindo documentação MkDocs localmente..."

# Verificar se mkdocs está instalado
if ! command -v mkdocs &> /dev/null; then
    echo "❌ MkDocs não encontrado. Instale com: uv sync --group docs"
    exit 1
fi

# Servir documentação
mkdocs serve --dev-addr 127.0.0.1:8001