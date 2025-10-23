# Imagen de python ligera
FROM python:3.11-slim

# Instalar netcat para verificar conexión a MySQL
RUN apt-get update && apt-get install -y netcat-traditional && rm -rf /var/lib/apt/lists/*

# Establecer el directorio de trabajo
WORKDIR /app

# Instalar dependencias
COPY requirements.txt .

# Instalar Gunicorn y otras dependencias con reintentos (3 intentos)
RUN pip install --default-timeout=300 --no-cache-dir -r requirements.txt || \
    pip install --default-timeout=300 --no-cache-dir -r requirements.txt || \
    pip install --default-timeout=300 --no-cache-dir -r requirements.txt

# Copiar el código de la aplicación
COPY . .

# Dar permisos de ejecución al script de espera
RUN chmod +x wait-for-db.sh

# Exponer el puerto 5000
EXPOSE 5000

# Para producción (Render/Railway), iniciar directamente Gunicorn
# El script wait-for-db.sh es opcional, solo para Docker local
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "--timeout", "120", "app:app"]
