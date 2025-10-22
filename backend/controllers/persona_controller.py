from flask import Blueprint, request, jsonify
from models.persona import Persona

persona_bp = Blueprint('persona', __name__, url_prefix='/api/personas')

@persona_bp.route('/', methods=['GET'])
def listar():
    try:
        personas = Persona.listar()
        return jsonify({'exito': True, 'datos': personas, 'total': len(personas)}), 200
    except Exception as e:
        return jsonify({'exito': False, 'mensaje': str(e)}), 500

@persona_bp.route('/<int:id>', methods=['GET'])
def obtener(id):
    try:
        persona = Persona.obtener_por_id(id)
        if not persona:
            return jsonify({'exito': False, 'mensaje': 'Persona no encontrada'}), 404
        return jsonify({'exito': True, 'datos': persona}), 200
    except Exception as e:
        return jsonify({'exito': False, 'mensaje': str(e)}), 500

@persona_bp.route('/', methods=['POST'])
def crear():
    try:
        datos = request.get_json()
        
        if not datos.get('primer_nombre') or not datos.get('primer_apellido') or not datos.get('numero_documento'):
            return jsonify({'exito': False, 'mensaje': 'Faltan campos requeridos'}), 400
        
        if Persona.existe_documento(datos['numero_documento']):
            return jsonify({'exito': False, 'mensaje': 'Documento ya existe'}), 400
        
        if datos.get('correo_electronico') and Persona.existe_correo(datos['correo_electronico']):
            return jsonify({'exito': False, 'mensaje': 'Correo ya existe'}), 400
        
        nuevo_id = Persona.crear(datos)
        persona = Persona.obtener_por_id(nuevo_id)
        return jsonify({'exito': True, 'mensaje': 'Persona creada', 'datos': persona}), 201
    except Exception as e:
        return jsonify({'exito': False, 'mensaje': str(e)}), 500

@persona_bp.route('/<int:id>', methods=['PUT'])
def actualizar(id):
    try:
        if not Persona.obtener_por_id(id):
            return jsonify({'exito': False, 'mensaje': 'Persona no encontrada'}), 404
        
        datos = request.get_json()
        
        if datos.get('numero_documento') and Persona.existe_documento(datos['numero_documento'], id):
            return jsonify({'exito': False, 'mensaje': 'Documento ya existe'}), 400
        
        if datos.get('correo_electronico') and Persona.existe_correo(datos['correo_electronico'], id):
            return jsonify({'exito': False, 'mensaje': 'Correo ya existe'}), 400
        
        Persona.actualizar(id, datos)
        persona = Persona.obtener_por_id(id)
        return jsonify({'exito': True, 'mensaje': 'Persona actualizada', 'datos': persona}), 200
    except Exception as e:
        return jsonify({'exito': False, 'mensaje': str(e)}), 500

@persona_bp.route('/<int:id>', methods=['DELETE'])
def eliminar(id):
    try:
        if not Persona.obtener_por_id(id):
            return jsonify({'exito': False, 'mensaje': 'Persona no encontrada'}), 404
        
        Persona.eliminar(id)
        return jsonify({'exito': True, 'mensaje': 'Persona eliminada'}), 200
    except Exception as e:
        return jsonify({'exito': False, 'mensaje': str(e)}), 500

@persona_bp.route('/buscar', methods=['GET'])
def buscar():
    try:
        termino = request.args.get('q', '')
        if not termino:
            return jsonify({'exito': False, 'mensaje': 'Falta término de búsqueda'}), 400
        
        personas = Persona.buscar(termino)
        return jsonify({'exito': True, 'datos': personas, 'total': len(personas)}), 200
    except Exception as e:
        return jsonify({'exito': False, 'mensaje': str(e)}), 500
