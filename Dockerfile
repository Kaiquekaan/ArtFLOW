# Etapa 1: Imagem base com Python
FROM python:3.10-slim

# Diretório de trabalho
WORKDIR /app/backend

# Instalação de dependências do sistema (build-essential e dependências do MySQL)
RUN apt-get update && apt-get install -y \
    build-essential \
    libmariadb-dev-compat \
    libmariadb-dev \
    pkg-config \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Instalar o pip mais recente
RUN pip install --upgrade pip

# Copiar os arquivos do projeto
COPY . /app

# Instalar as dependências do projeto
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Configuração de variáveis de ambiente
ENV PYTHONUNBUFFERED=1 
ENV DJANGO_SETTINGS_MODULE=backend.settings 
ENV REDIS_URL=redis://redis:6379/0 

ENV PYTHONPATH=/app


# Criação de um usuário sem privilégios
RUN adduser --disabled-password --gecos '' myuser
USER myuser

# Expor a porta do servidor
EXPOSE 8000

# Comando para iniciar o servidor com Gunicorn
CMD ["gunicorn", "--workers=4", "--bind=0.0.0.0:8000", "backend.asgi:application", "-k", "uvicorn.workers.UvicornWorker"]
