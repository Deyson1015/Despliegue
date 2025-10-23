from database.db import db

class Persona:
    
    # Crear una nueva persona
    @staticmethod
    def crear(datos):
        consulta = """
        INSERT INTO personas 
        (primer_nombre, segundo_nombre, primer_apellido, segundo_apellido, 
        numero_documento, genero, correo_electronico, telefono)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        parametros = (
            datos.get('primer_nombre'),
            datos.get('segundo_nombre'),
            datos.get('primer_apellido'),
            datos.get('segundo_apellido'),
            datos.get('numero_documento'),
            datos.get('genero'),
            datos.get('correo_electronico'),
            datos.get('telefono')
        )
        
        try:
            if not db.conectar():
                raise Exception("No se pudo establecer conexión con la base de datos")
            
            db.cursor.execute(consulta, parametros)
            db.connection.commit()
            nuevo_id = db.cursor.lastrowid
            db.cerrar()
            return nuevo_id
        except Exception as e:
            if db.connection:
                db.connection.rollback()
            db.cerrar()
            raise e
    
    # Listar todas las personas
    @staticmethod
    def listar():
        consulta = "SELECT * FROM personas"
        
        try:
            if not db.conectar():
                raise Exception("No se pudo establecer conexión con la base de datos")
            
            db.cursor.execute(consulta)
            resultados = db.cursor.fetchall()
            db.cerrar()
            return resultados
        except Exception as e:
            db.cerrar()
            raise e
    
    # Obtener una persona por ID
    @staticmethod
    def obtener_por_id(id):
        consulta = "SELECT * FROM personas WHERE id = %s"
        
        try:
            if not db.conectar():
                raise Exception("No se pudo establecer conexión con la base de datos")
            
            db.cursor.execute(consulta, (id,))
            resultado = db.cursor.fetchone()
            db.cerrar()
            return resultado
        except Exception as e:
            db.cerrar()
            raise e
    
    # Actualizar una persona existente
    @staticmethod
    def actualizar(id, datos):
        campos = []
        valores = []
        
        if 'primer_nombre' in datos:
            campos.append("primer_nombre = %s")
            valores.append(datos['primer_nombre'])
        if 'segundo_nombre' in datos:
            campos.append("segundo_nombre = %s")
            valores.append(datos['segundo_nombre'])
        if 'primer_apellido' in datos:
            campos.append("primer_apellido = %s")
            valores.append(datos['primer_apellido'])
        if 'segundo_apellido' in datos:
            campos.append("segundo_apellido = %s")
            valores.append(datos['segundo_apellido'])
        if 'numero_documento' in datos:
            campos.append("numero_documento = %s")
            valores.append(datos['numero_documento'])
        if 'genero' in datos:
            campos.append("genero = %s")
            valores.append(datos['genero'])
        if 'correo_electronico' in datos:
            campos.append("correo_electronico = %s")
            valores.append(datos['correo_electronico'])
        if 'telefono' in datos:
            campos.append("telefono = %s")
            valores.append(datos['telefono'])
        
        valores.append(id)
        consulta = f"UPDATE personas SET {', '.join(campos)} WHERE id = %s"
        
        try:
            if not db.conectar():
                raise Exception("No se pudo establecer conexión con la base de datos")
            
            db.cursor.execute(consulta, tuple(valores))
            db.connection.commit()
            filas_afectadas = db.cursor.rowcount
            db.cerrar()
            return filas_afectadas > 0
        except Exception as e:
            if db.connection:
                db.connection.rollback()
            db.cerrar()
            raise e
    
    # Eliminar una persona
    @staticmethod
    def eliminar(id):
        consulta = "DELETE FROM personas WHERE id = %s"
        
        try:
            if not db.conectar():
                raise Exception("No se pudo establecer conexión con la base de datos")
            
            db.cursor.execute(consulta, (id,))
            db.connection.commit()
            filas_afectadas = db.cursor.rowcount
            db.cerrar()
            return filas_afectadas > 0
        except Exception as e:
            if db.connection:
                db.connection.rollback()
            db.cerrar()
            raise e
    
    # Verificar si existe un documento
    @staticmethod
    def existe_documento(numero_documento, excluir_id=None):
        if excluir_id:
            consulta = "SELECT id FROM personas WHERE numero_documento = %s AND id != %s"
            parametros = (numero_documento, excluir_id)
        else:
            consulta = "SELECT id FROM personas WHERE numero_documento = %s"
            parametros = (numero_documento,)
        
        try:
            if not db.conectar():
                raise Exception("No se pudo establecer conexión con la base de datos")
            
            db.cursor.execute(consulta, parametros)
            resultado = db.cursor.fetchone()
            db.cerrar()
            return resultado is not None
        except Exception as e:
            db.cerrar()
            raise e
    
    # Verificar si existe un correo
    @staticmethod
    def existe_correo(correo, excluir_id=None):
        if not correo:
            return False
            
        if excluir_id:
            consulta = "SELECT id FROM personas WHERE correo_electronico = %s AND id != %s"
            parametros = (correo, excluir_id)
        else:
            consulta = "SELECT id FROM personas WHERE correo_electronico = %s"
            parametros = (correo,)

        try:
            if not db.conectar():
                raise Exception("No se pudo establecer conexión con la base de datos")
            
            db.cursor.execute(consulta, parametros)
            resultado = db.cursor.fetchone()
            db.cerrar()
            return resultado is not None
        except Exception as e:
            db.cerrar()
            raise e
    
    # Buscar personas por término
    @staticmethod
    def buscar(termino):
        consulta = """
        SELECT * FROM personas 
        WHERE primer_nombre LIKE %s 
        OR segundo_nombre LIKE %s 
        OR primer_apellido LIKE %s 
        OR segundo_apellido LIKE %s 
        OR numero_documento LIKE %s 
        OR correo_electronico LIKE %s 
        OR telefono LIKE %s
        """
        patron = f"%{termino}%"
        parametros = (patron, patron, patron, patron, patron, patron, patron)
        
        try:
            if not db.conectar():
                raise Exception("No se pudo establecer conexión con la base de datos")
            
            db.cursor.execute(consulta, parametros)
            resultados = db.cursor.fetchall()
            db.cerrar()
            return resultados
        except Exception as e:
            db.cerrar()
            raise e
