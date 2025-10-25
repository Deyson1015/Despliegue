# app.py
from flask import Flask, jsonify
from flask_cors import CORS
from config.config import Config, config
from database.db import init_db
from controllers.persona_controller import persona_bp
import os

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = Config.SECRET_KEY
    
    # Obtener entorno actual (por defecto: development)
    env = os.getenv('APP_ENV', 'development')
    app.config.from_object(config[env])

    # CORS
    CORS(app)

    # Inicializar base de datos dentro del contexto de la app
    with app.app_context():
        init_db()

    # Rutas
    app.register_blueprint(persona_bp)

    @app.route('/')
    def inicio():
        return jsonify({
            'mensaje': 'API de Gestión de Personas',
            'version': '1.0',
            'endpoints': {
                'listar': 'GET /api/personas',
                'obtener': 'GET /api/personas/<id>',
                'crear': 'POST /api/personas',
                'actualizar': 'PUT /api/personas/<id>',
                'eliminar': 'DELETE /api/personas/<id>',
                'buscar': 'GET /api/personas/buscar?q=termino'
            }
        })

    @app.route('/health')
    def health():
        return jsonify({'status': 'ok'}), 200

    return app

if __name__ == '__main__':
    app = create_app()
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
