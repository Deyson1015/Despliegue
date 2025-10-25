import os
from dotenv import load_dotenv

# Determinar el entorno
APP_ENV = os.getenv('APP_ENV', 'development')

# Cargar el archivo .env correspondiente PRIMERO
if APP_ENV == 'testing':
    load_dotenv('.env.test', override=True)
elif APP_ENV == 'production':
    load_dotenv('.env.production', override=True)
else:
    load_dotenv('.env', override=True)

# Configuración base (se hereda en los demás entornos)
class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_PORT = int(os.getenv('DB_PORT', '3306'))
    DB_NAME = os.getenv('DB_NAME', 'gestion_personas')
    DB_USER = os.getenv('DB_USER', 'admin')
    DB_PASSWORD = os.getenv('DB_PASSWORD', 'admin123')
    CORS_HEADERS = 'Content-Type'
    DEBUG = False
    TESTING = False

# Configuración para entorno de desarrollo
class DevelopmentConfig(Config):
    DEBUG = True

# Configuración para entorno de producción
class ProductionConfig(Config):
    DEBUG = False

# Configuración para entorno de pruebas (pytest, CI/CD)
class TestConfig(Config):
    TESTING = True
    DEBUG = True

# Diccionario para seleccionar entorno fácilmente
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestConfig
}
