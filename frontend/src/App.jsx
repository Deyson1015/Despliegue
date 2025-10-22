import { useState, useEffect } from 'react';
import './App.css';
import PersonaForm from './components/PersonaForm';
import PersonaLista from './components/PersonaLista';
import SearchBar from './components/SearchBar';
import personaService from './services/personaService';
import Swal from 'sweetalert2';

function App() {
  const [personas, setPersonas] = useState([]);
  const [personaEditar, setPersonaEditar] = useState(null);
  const [mostrarFormulario, setMostrarFormulario] = useState(false);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    cargarPersonas();
  }, []);

  const cargarPersonas = async () => {
    try {
      setLoading(true);
      const response = await personaService.listar();
      if (response.exito) {
        setPersonas(response.datos);
      }
    } catch (error) {
      Swal.fire({
        icon: 'error',
        title: 'Error',
        text: 'Error al cargar las personas'
      });
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const handleBuscar = async (termino) => {
    if (!termino.trim()) {
      cargarPersonas();
      return;
    }

    try {
      setLoading(true);
      const response = await personaService.buscar(termino);
      if (response.exito) {
        setPersonas(response.datos);
      }
    } catch (error) {
      Swal.fire({
        icon: 'error',
        title: 'Error',
        text: 'Error al buscar personas'
      });
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const handleNuevo = () => {
    setPersonaEditar(null);
    setMostrarFormulario(true);
  };

  const handleEditar = (persona) => {
    setPersonaEditar(persona);
    setMostrarFormulario(true);
  };

  const handleEliminar = async (id) => {
    try {
      setLoading(true);
      const response = await personaService.eliminar(id);
      if (response.exito) {
        Swal.fire({
          icon: 'success',
          title: '¡Eliminado!',
          text: 'Persona eliminada exitosamente',
          timer: 2000,
          showConfirmButton: false
        });
        cargarPersonas();
      }
    } catch (error) {
      Swal.fire({
        icon: 'error',
        title: 'Error',
        text: error.response?.data?.mensaje || 'Error al eliminar la persona'
      });
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (datos) => {
    try {
      setLoading(true);
      let response;

      if (personaEditar) {
        response = await personaService.actualizar(personaEditar.id, datos);
        Swal.fire({
          icon: 'success',
          title: '¡Actualizado!',
          text: 'Persona actualizada exitosamente',
          timer: 2000,
          showConfirmButton: false
        });
      } else {
        response = await personaService.crear(datos);
        Swal.fire({
          icon: 'success',
          title: '¡Creado!',
          text: 'Persona creada exitosamente',
          timer: 2000,
          showConfirmButton: false
        });
      }

      if (response.exito) {
        setMostrarFormulario(false);
        setPersonaEditar(null);
        cargarPersonas();
      }
    } catch (error) {
      Swal.fire({
        icon: 'error',
        title: 'Error',
        text: error.response?.data?.mensaje || 'Error al guardar la persona'
      });
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const handleCancelar = () => {
    setMostrarFormulario(false);
    setPersonaEditar(null);
  };

  return (
    <div className="app">
      <header className="app-header">
        <h1>Gestión de Personas</h1>
      </header>

      <main className="app-main">
        {loading && <div className="loading">Cargando...</div>}

        {!mostrarFormulario ? (
          <>
            <SearchBar onBuscar={handleBuscar} onNuevo={handleNuevo} />
            <PersonaLista
              personas={personas}
              onEditar={handleEditar}
              onEliminar={handleEliminar}
            />
          </>
        ) : (
          <PersonaForm
            personaEditar={personaEditar}
            onSubmit={handleSubmit}
            onCancelar={handleCancelar}
          />
        )}
      </main>

      <footer className="app-footer">
        <p>Sistema de Gestión de Personas - 2025</p>
      </footer>
    </div>
  );
}

export default App;
