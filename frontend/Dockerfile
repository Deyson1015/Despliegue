# Dockerfile para Frontend React + Vite 

# Usar Node.js 20 
FROM node:20-alpine

# Establecer directorio de trabajo
WORKDIR /app

# Copiar archivos de dependencias
COPY package*.json ./

# Instalar dependencias con reintentos (3 intentos)
RUN npm install --network-timeout=300000 || \
    npm install --network-timeout=300000 || \
    npm install --network-timeout=300000

# Copiar todo el código fuente
COPY . .

# Exponer el puerto de Vite (5173)
EXPOSE 5173

# Iniciar el servidor de desarrollo de Vite
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
