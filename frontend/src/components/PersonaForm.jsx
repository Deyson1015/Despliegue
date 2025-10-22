import { useState, useEffect } from 'react';
import './PersonaForm.css';

const PersonaForm = ({ personaEditar, onSubmit, onCancelar }) => {
  const [formData, setFormData] = useState({
    primer_nombre: '',
    segundo_nombre: '',
    primer_apellido: '',
    segundo_apellido: '',
    numero_documento: '',
    genero: '',
    correo_electronico: '',
    telefono: '',
  });

  const [errors, setErrors] = useState({});

  useEffect(() => {
    if (personaEditar) {
      setFormData({
        primer_nombre: personaEditar.primer_nombre || '',
        segundo_nombre: personaEditar.segundo_nombre || '',
        primer_apellido: personaEditar.primer_apellido || '',
        segundo_apellido: personaEditar.segundo_apellido || '',
        numero_documento: personaEditar.numero_documento || '',
        genero: personaEditar.genero || '',
        correo_electronico: personaEditar.correo_electronico || '',
        telefono: personaEditar.telefono || '',
      });
    }
  }, [personaEditar]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value,
    });
    // Limpiar error del campo
    if (errors[name]) {
      setErrors({
        ...errors,
        [name]: '',
      });
    }
  };

  const validarFormulario = () => {
    const newErrors = {};

    if (!formData.primer_nombre.trim()) {
      newErrors.primer_nombre = 'El primer nombre es requerido';
    }

    if (!formData.primer_apellido.trim()) {
      newErrors.primer_apellido = 'El primer apellido es requerido';
    }

    if (!formData.numero_documento.trim()) {
      newErrors.numero_documento = 'El número de documento es requerido';
    }

    if (formData.correo_electronico && !/\S+@\S+\.\S+/.test(formData.correo_electronico)) {
      newErrors.correo_electronico = 'El correo electrónico no es válido';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (validarFormulario()) {
      onSubmit(formData);
    }
  };

  return (
    <div className="persona-form-container">
      <h2>{personaEditar ? 'Editar Persona' : 'Nueva Persona'}</h2>
      <form onSubmit={handleSubmit} className="persona-form">
        <div className="form-row">
          <div className="form-group">
            <label htmlFor="primer_nombre">Primer Nombre *</label>
            <input
              type="text"
              id="primer_nombre"
              name="primer_nombre"
              value={formData.primer_nombre}
              onChange={handleChange}
              className={errors.primer_nombre ? 'error' : ''}
            />
            {errors.primer_nombre && <span className="error-message">{errors.primer_nombre}</span>}
          </div>

          <div className="form-group">
            <label htmlFor="segundo_nombre">Segundo Nombre</label>
            <input
              type="text"
              id="segundo_nombre"
              name="segundo_nombre"
              value={formData.segundo_nombre}
              onChange={handleChange}
            />
          </div>
        </div>

        <div className="form-row">
          <div className="form-group">
            <label htmlFor="primer_apellido">Primer Apellido *</label>
            <input
              type="text"
              id="primer_apellido"
              name="primer_apellido"
              value={formData.primer_apellido}
              onChange={handleChange}
              className={errors.primer_apellido ? 'error' : ''}
            />
            {errors.primer_apellido && <span className="error-message">{errors.primer_apellido}</span>}
          </div>

          <div className="form-group">
            <label htmlFor="segundo_apellido">Segundo Apellido</label>
            <input
              type="text"
              id="segundo_apellido"
              name="segundo_apellido"
              value={formData.segundo_apellido}
              onChange={handleChange}
            />
          </div>
        </div>

        <div className="form-row">
          <div className="form-group">
            <label htmlFor="numero_documento">Número de Documento *</label>
            <input
              type="text"
              id="numero_documento"
              name="numero_documento"
              value={formData.numero_documento}
              onChange={handleChange}
              className={errors.numero_documento ? 'error' : ''}
            />
            {errors.numero_documento && <span className="error-message">{errors.numero_documento}</span>}
          </div>

          <div className="form-group">
            <label htmlFor="genero">Género</label>
            <select
              id="genero"
              name="genero"
              value={formData.genero}
              onChange={handleChange}
            >
              <option value="">Seleccione...</option>
              <option value="M">Masculino</option>
              <option value="F">Femenino</option>
              <option value="O">Otro</option>
            </select>
          </div>
        </div>

        <div className="form-row">
          <div className="form-group">
            <label htmlFor="correo_electronico">Correo Electrónico</label>
            <input
              type="email"
              id="correo_electronico"
              name="correo_electronico"
              value={formData.correo_electronico}
              onChange={handleChange}
              className={errors.correo_electronico ? 'error' : ''}
            />
            {errors.correo_electronico && <span className="error-message">{errors.correo_electronico}</span>}
          </div>

          <div className="form-group">
            <label htmlFor="telefono">Teléfono</label>
            <input
              type="tel"
              id="telefono"
              name="telefono"
              value={formData.telefono}
              onChange={handleChange}
            />
          </div>
        </div>

        <div className="form-actions">
          <button type="submit" className="btn btn-primary">
            {personaEditar ? 'Actualizar' : 'Guardar'}
          </button>
          <button type="button" className="btn btn-secondary" onClick={onCancelar}>
            Cancelar
          </button>
        </div>
      </form>
    </div>
  );
};

export default PersonaForm;
