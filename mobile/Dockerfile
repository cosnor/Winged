# Dockerfile para desarrollo con hot reload
FROM node:20-alpine

# Instalar dependencias del sistema
RUN apk add --no-cache git

# Crear directorio de trabajo
WORKDIR /app

# Instalar Expo CLI globalmente
RUN npm install -g @expo/cli

# Copiar package.json y package-lock.json para aprovechar cache de Docker
COPY package*.json ./

# Instalar dependencias de Node
RUN npm install

# Copiar el resto de los archivos del proyecto
COPY . .

# Exponer puertos necesarios para Expo
EXPOSE 8081 19000 19001 19002

# Comando para iniciar Expo con hot reload habilitado
CMD ["npx", "expo", "start", "--web", "--host", "lan", "--port", "8081"]
