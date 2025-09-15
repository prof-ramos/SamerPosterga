FROM python:3.11-slim

WORKDIR /app

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements e instalar dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código fonte
COPY src/ ./src/
COPY pyproject.toml .

# Criar diretórios necessários
RUN mkdir -p data/RRAG data/chroma logs

# Comando para executar
CMD ["python", "-m", "src.asof_bot.main"]