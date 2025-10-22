#!/bin/sh
# wait-for-db.sh - Espera a que MySQL esté disponible

echo "Esperando a que MySQL esté disponible..."

# Usar variables de entorno del .env.docker
HOST="${DB_HOST:-db}"
PORT="${DB_PORT:-3306}"
MAX_TRIES=60
TRIES=0

while [ $TRIES -lt $MAX_TRIES ]; do
    if nc -z $HOST $PORT 2>/dev/null; then
        echo "✓ MySQL está disponible en $HOST:$PORT"
        sleep 5  # Esperar 5 segundos más para asegurar que esté completamente listo
        exit 0
    fi
    
    TRIES=$((TRIES + 1))
    echo "Intento $TRIES/$MAX_TRIES - Esperando MySQL..."
    sleep 2
done

echo "✗ ERROR: MySQL no respondió después de $MAX_TRIES intentos"
exit 1
