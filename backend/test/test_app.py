import json

# Datos de prueba
persona_valida = {
    "primer_nombre": "Juan",
    "segundo_nombre": "Carlos",
    "primer_apellido": "Perez",
    "segundo_apellido": "Gomez",
    "numero_documento": "123456789",
    "genero": "Masculino",
    "correo_electronico": "juan.perez@example.com",
    "telefono": "3001234567",
}

def test_health_check(client):
    """Prueba el endpoint de health check."""
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json == {'status': 'ok'}

def test_listar_personas_vacio(client):
    """Prueba que se obtiene una lista vacía si no hay personas."""
    response = client.get('/api/personas/')
    assert response.status_code == 200
    data = response.json
    assert data['exito'] is True
    assert data['datos'] == []
    assert data['total'] == 0

def test_crear_persona(client):
    """Prueba la creación exitosa de una persona."""
    response = client.post('/api/personas/', data=json.dumps(persona_valida), content_type='application/json')
    assert response.status_code == 201
    data = response.json
    assert data['exito'] is True
    assert data['mensaje'] == 'Persona creada'
    assert data['datos']['primer_nombre'] == persona_valida['primer_nombre']
    assert data['datos']['numero_documento'] == persona_valida['numero_documento']

def test_crear_persona_campos_faltantes(client):
    """Prueba que la creación falla si faltan campos requeridos."""
    persona_invalida = persona_valida.copy()
    del persona_invalida['primer_nombre']
    response = client.post('/api/personas/', data=json.dumps(persona_invalida), content_type='application/json')
    assert response.status_code == 400
    data = response.json
    assert data['exito'] is False
    assert data['mensaje'] == 'Faltan campos requeridos'

def test_crear_persona_documento_duplicado(client):
    """Prueba que no se puede crear una persona con un documento que ya existe."""
    # La persona ya fue creada en `test_crear_persona`
    response = client.post('/api/personas/', data=json.dumps(persona_valida), content_type='application/json')
    assert response.status_code == 400
    data = response.json
    assert data['exito'] is False
    assert data['mensaje'] == 'Documento ya existe'

def test_listar_personas(client):
    """Prueba que se puede listar las personas existentes."""
    response = client.get('/api/personas/')
    assert response.status_code == 200
    data = response.json
    assert data['exito'] is True
    assert len(data['datos']) == 1
    assert data['total'] == 1
    assert data['datos'][0]['numero_documento'] == persona_valida['numero_documento']

def test_obtener_persona_por_id(client):
    """Prueba que se puede obtener una persona por su ID."""
    response = client.get('/api/personas/1')
    assert response.status_code == 200
    data = response.json
    assert data['exito'] is True
    assert data['datos']['id'] == 1
    assert data['datos']['primer_nombre'] == persona_valida['primer_nombre']

def test_obtener_persona_no_existente(client):
    """Prueba que se obtiene un 404 para una persona que no existe."""
    response = client.get('/api/personas/999')
    assert response.status_code == 404
    data = response.json
    assert data['exito'] is False
    assert data['mensaje'] == 'Persona no encontrada'

def test_actualizar_persona(client):
    """Prueba la actualización de los datos de una persona."""
    datos_actualizados = {
        "primer_nombre": "Juanito",
        "telefono": "3109876543"
    }
    response = client.put('/api/personas/1', data=json.dumps(datos_actualizados), content_type='application/json')
    assert response.status_code == 200
    data = response.json
    assert data['exito'] is True
    assert data['mensaje'] == 'Persona actualizada'
    assert data['datos']['id'] == 1
    assert data['datos']['primer_nombre'] == "Juanito"
    assert data['datos']['telefono'] == "3109876543"

def test_actualizar_persona_no_existente(client):
    """Prueba que no se puede actualizar una persona que no existe."""
    response = client.put('/api/personas/999', data=json.dumps({}), content_type='application/json')
    assert response.status_code == 404
    data = response.json
    assert data['exito'] is False
    assert data['mensaje'] == 'Persona no encontrada'

def test_buscar_persona(client):
    """Prueba la funcionalidad de búsqueda de personas."""
    # Busca por nombre "Juanito"
    response = client.get('/api/personas/buscar?q=Juanito')
    assert response.status_code == 200
    data = response.json
    assert data['exito'] is True
    assert len(data['datos']) == 1
    assert data['datos'][0]['primer_nombre'] == 'Juanito'

    # Busca por documento
    response = client.get(f"/api/personas/buscar?q={persona_valida['numero_documento']}")
    assert response.status_code == 200
    data = response.json
    assert data['exito'] is True
    assert len(data['datos']) == 1

def test_buscar_persona_sin_termino(client):
    """Prueba que la búsqueda falla si no se proporciona un término."""
    response = client.get('/api/personas/buscar')
    assert response.status_code == 400
    data = response.json
    assert data['exito'] is False
    assert data['mensaje'] == 'Falta término de búsqueda'

def test_eliminar_persona(client):
    """Prueba que se puede eliminar una persona."""
    response = client.delete('/api/personas/1')
    assert response.status_code == 200
    data = response.json
    assert data['exito'] is True
    assert data['mensaje'] == 'Persona eliminada'

    # Verifica que la persona ya no existe
    response_get = client.get('/api/personas/1')
    assert response_get.status_code == 404

def test_eliminar_persona_no_existente(client):
    """Prueba que no se puede eliminar una persona que no existe."""
    response = client.delete('/api/personas/999')
    assert response.status_code == 404
    data = response.json
    assert data['exito'] is False
    assert data['mensaje'] == 'Persona no encontrada'
