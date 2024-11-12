# Etapa 1: Imagem base com Python
FROM python:3.10-slim

# Diretório de trabalho
WORKDIR /app

# Instalação de dependências do sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    libmysqlclient-dev \
    && rm -rf /var/lib/apt/lists/*

# Copia o projeto
COPY . /app

# Instalação das dependências do projeto
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Configura variáveis de ambiente
ENV PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=config.settings.production \
    REDIS_URL=redis://localhost:6379/0

# Criação de um usuário sem privilégios
RUN adduser --disabled-password myuser
USER myuser

# Comando para iniciar o servidor com Daphne
ENTRYPOINT ["daphne", "-b", "0.0.0.0", "-p", "8000", "config.asgi:application"]

# Expondo a porta
EXPOSE 8000
