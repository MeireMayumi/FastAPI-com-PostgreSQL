# Usar a imagem base do Python
FROM python:3.12-alpine

# Criar um novo usuário
RUN adduser -D fastapi

# Criar area de trabalho dentro do container /app
WORKDIR /app

#Copiar o arquivo de requisitos
COPY requirements.txt requirements.txt

# Instalar dependências
RUN apk add --no-cache bash curl gcc musl-dev netcat-openbsd postgresql-dev \
&& pip install --no-cache-dir -r requirements.txt     

# Copiar todos o arquivos da aplicação
COPY . /app 

# Dar permissão de execução ao script wait-for-it.sh
RUN chmod +x /app/wait-for-it.sh

# Trocar para o novo usuário
USER fastapi

# Adicionar um health check
HEALTHCHECK CMD ["curl", "--fail", "http://localhost:8000/"]

# Comando para executar a aplicação
CMD ["/app/wait-for-it.sh", "db", "--", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]