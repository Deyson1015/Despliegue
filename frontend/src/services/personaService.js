import api from '../config/api';

const personaService = {
  // Obtener todas las personas
  listar: async () => {
    const response = await api.get('/api/personas/');
    return response.data;
  },

  // Obtener una persona por ID
  obtenerPorId: async (id) => {
    const response = await api.get(`/api/personas/${id}`);
    return response.data;
  },

  // Crear una nueva persona
  crear: async (datos) => {
    const response = await api.post('/api/personas/', datos);
    return response.data;
  },

  // Actualizar una persona
  actualizar: async (id, datos) => {
    const response = await api.put(`/api/personas/${id}`, datos);
    return response.data;
  },

  // Eliminar una persona
  eliminar: async (id) => {
    const response = await api.delete(`/api/personas/${id}`);
    return response.data;
  },

  // Buscar personas
  buscar: async (termino) => {
    const response = await api.get(`/api/personas/buscar?q=${termino}`);
    return response.data;
  },
};

export default personaService;
