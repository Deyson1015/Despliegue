# Imagen de python ligera
FROM python:3.11-slim

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

# Exponer el puerto 5000
EXPOSE 5000

# Iniciar directamente Gunicorn (sin wait-for-db.sh)
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "--timeout", "120", "app:app"]
