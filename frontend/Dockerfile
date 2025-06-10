# Use uma imagem base Node.js para o build
FROM node:18-alpine as builder

# Defina o diretório de trabalho
WORKDIR /app

# Copie os arquivos de package e instale as dependências
COPY package.json package-lock.json ./
RUN npm install

# Copie o código fonte
COPY . .

# Build a aplicação React
RUN npm run build

# Use uma imagem base Nginx para servir os arquivos estáticos
FROM nginx:alpine

# Copie os arquivos de build do estágio anterior para o diretório de serviço do Nginx
COPY --from=builder /app/build /usr/share/nginx/html

# Exponha a porta do Nginx
EXPOSE 80

# Comando para iniciar o Nginx
CMD ["nginx", "-g", "'daemon off;'"]