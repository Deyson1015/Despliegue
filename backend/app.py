from flask import Flask, jsonify
from flask_cors import CORS
from config.config import Config
from database.db import init_db
from controllers.persona_controller import persona_bp
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = Config.SECRET_KEY

# Configurar CORS para producción
CORS(app)

# Inicializar base de datos
init_db()

# Registrar rutas
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

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
