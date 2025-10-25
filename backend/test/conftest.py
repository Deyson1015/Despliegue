import os
import pytest
import sys
from dotenv import load_dotenv

# Agregamos el path del backend al sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# IMPORTANTE: Cargar .env.test ANTES de importar app
os.environ["APP_ENV"] = "testing"
load_dotenv('.env.test', override=True)

from app import create_app
from database.db import init_db, db


@pytest.fixture(scope="session")
def test_app():
    app = create_app()  # Ya llama a init_db() internamente

    yield app

    # Limpieza final
    with app.app_context():
        if db.conectar():
            db.cursor.execute("DROP TABLE IF EXISTS personas;")
            db.connection.commit()
            db.cerrar()


@pytest.fixture(scope="function")
def client(test_app):
    return test_app.test_client()
