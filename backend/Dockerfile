# Use uma imagem base Python
FROM python:3.10-slim

# Defina o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copie o arquivo de requisitos e instale as dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie o restante do código da aplicação
COPY . .

# Exponha a porta que a aplicação usa
EXPOSE 8000

# Comando para rodar a aplicação (ajuste conforme seu ponto de entrada)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]