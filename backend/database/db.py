import mysql.connector
from mysql.connector import Error
from config.config import Config
import time

class Database:
    def __init__(self):
        self.host = Config.DB_HOST
        self.port = Config.DB_PORT
        self.database = Config.DB_NAME
        self.user = Config.DB_USER
        self.password = Config.DB_PASSWORD
        self.connection = None
        self.cursor = None

    def conectar(self):
        try:
            print(f"Conectando a MySQL en {self.host}:{self.port}/{self.database}...")
            self.connection = mysql.connector.connect(
                host=self.host,
                port=self.port,
                database=self.database,
                user=self.user,
                password=self.password,
                connect_timeout=10,
                autocommit=False
            )
            if self.connection.is_connected():
                self.cursor = self.connection.cursor(dictionary=True)
                db_info = self.connection.get_server_info()
                print(f" Conexión exitosa a MySQL Server {db_info}")
                return True
        except Error as e:
            print(f" Error al conectar a MySQL: {e}")
            return False
        return False

    def cerrar(self):
        if self.cursor:
            self.cursor.close()
        if self.connection and self.connection.is_connected():
            self.connection.close()

# Instancia global
db = Database()

def init_db():
    """Inicializa la base de datos y crea la tabla si no existe"""
    print("=" * 60)
    print(" Iniciando conexión a MySQL...")
    print("=" * 60)

    # Reintentar conexión hasta 30 veces (aproximadamente 1 minuto)
    max_intentos = 30
    intentos = 0
    
    while intentos < max_intentos:
        intentos += 1
        print(f"Intento {intentos}/{max_intentos} de conexión a MySQL...")
        
        if db.conectar():
            break
        
        if intentos < max_intentos:
            print(" Esperando 2 segundos antes de reintentar...")
            time.sleep(2)
        else:
            print(" No se pudo conectar a la base de datos después de múltiples intentos.")
            return False

    try:
        tabla = """
        CREATE TABLE IF NOT EXISTS personas (
            id INT AUTO_INCREMENT PRIMARY KEY,
            primer_nombre VARCHAR(50) NOT NULL,
            segundo_nombre VARCHAR(50),
            primer_apellido VARCHAR(50) NOT NULL,
            segundo_apellido VARCHAR(50),
            numero_documento VARCHAR(20) UNIQUE NOT NULL,
            genero VARCHAR(20),
            correo_electronico VARCHAR(100) UNIQUE,
            telefono VARCHAR(20)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
        """
        
        db.cursor.execute(tabla)
        db.connection.commit()
        print(" Tabla 'personas' creada o verificada correctamente")
        print("=" * 60)
        print(" Base de datos lista para usar")
        print("=" * 60)
        return True
    except Exception as e:
        print(f" Error al crear tabla: {e}")
        return False
    finally:
        db.cerrar()
