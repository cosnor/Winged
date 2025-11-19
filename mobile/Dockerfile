# Dockerfile para desarrollo con Expo + Hot Reload + QR
FROM node:20-alpine

# Instalar dependencias del sistema
RUN apk add --no-cache git bash

# Crear directorio de trabajo
WORKDIR /app

# Evitar problemas de permisos con node_modules
RUN mkdir -p /app/node_modules && chmod -R 777 /app/node_modules

# Instalar Expo CLI globalmente
RUN npm install -g expo-cli @expo/cli

# Copiar package.json y package-lock.json
COPY package*.json ./

# Instalar dependencias del proyecto
RUN npm install

# Copiar el resto del código
COPY . .

# Puertos para Expo
EXPOSE 19000 19001 19002 8081

# Comando para iniciar Expo (MUESTRA QR)
CMD ["npx", "expo", "start", "--tunnel"]
