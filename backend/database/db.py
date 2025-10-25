import mysql.connector
from mysql.connector import Error
from flask import current_app

class Database:
    
    def __init__(self):
        self.host = None
        self.port = None
        self.database = None
        self.user = None
        self.password = None
        self.connection = None
        self.cursor = None

    def init_app(self, config):
        """Carga la configuración de la base de datos desde la app Flask."""
        self.host = config['DB_HOST']
        self.port = config['DB_PORT']
        self.database = config['DB_NAME']
        self.user = config['DB_USER']
        self.password = config['DB_PASSWORD']

    def conectar(self):
        """Conecta a MySQL. Retorna True si éxito, False si falla."""
        try:
            # Asegurarse de que la configuración ha sido inicializada
            if not self.host:
                self.init_app(current_app.config)

            print(f" Conectando a MySQL en {self.host}:{self.port}/{self.database}...")
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
        """Cierra el cursor y la conexión de forma segura."""
        try:
            if self.cursor:
                self.cursor.close()
            if self.connection and self.connection.is_connected():
                self.connection.close()
                print("Conexión a MySQL cerrada")
        except Exception as e:
            print(f" Error al cerrar conexión: {e}")

# Instancia global
db = Database()

def init_db():
    """Inicializa la base de datos y crea la tabla si no existe"""
    db.init_app(current_app.config)
    
    print("=" * 60)
    print(" Iniciando conexión a MySQL...")
    print("=" * 60)

    # Conectar (el healthcheck ya garantiza que MySQL está listo)
    if not db.conectar():
        print("❌ No se pudo conectar a la base de datos")
        return False

    try:
        # Crear tabla (sin DROP - mantiene datos entre reinicios)
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
        if db.connection:
            db.connection.rollback()
        return False
