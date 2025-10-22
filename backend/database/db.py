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
    
    def conectar(self, max_intentos=5, tiempo_espera=3):
        """Intenta conectar a MySQL con reintentos"""
        for intento in range(max_intentos):
            try:
                print(f"Intento {intento + 1} de conexión a MySQL...")
                self.connection = mysql.connector.connect(
                    host=self.host,
                    port=self.port,
                    database=self.database,
                    user=self.user,
                    password=self.password
                )
                if self.connection.is_connected():
                    self.cursor = self.connection.cursor(dictionary=True)
                    print("Conexión exitosa a MySQL")
                    return True
            except Error as e:
                print(f"Error al conectar a MySQL (intento {intento + 1}/{max_intentos}): {e}")
                if intento < max_intentos - 1:
                    print(f"Esperando {tiempo_espera} segundos antes de reintentar...")
                    time.sleep(tiempo_espera)
                else:
                    print("No se pudo conectar a MySQL después de varios intentos")
                    return False
        return False
    
    def cerrar(self):
        if self.cursor:
            self.cursor.close()
        if self.connection and self.connection.is_connected():
            self.connection.close()

# Instancia global de la base de datos
db = Database()

def init_db():
    """Inicializa la base de datos y crea las tablas necesarias"""
    if not db.conectar():
        print("✗ No se pudo inicializar la base de datos")
        return False
    
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
    
    try:
        db.cursor.execute(tabla)
        db.connection.commit()
        print("Tabla 'personas' creada o verificada correctamente")
        return True
    except Error as e:
        print(f"Error al crear tabla: {e}")
        return False
