import './PersonaLista.css';
import Swal from 'sweetalert2';

const PersonaLista = ({ personas, onEditar, onEliminar }) => {
  const confirmarEliminar = (id, nombre) => {
    Swal.fire({
      title: '¿Estás seguro?',
      text: `¿Deseas eliminar a ${nombre}?`,
      icon: 'warning',
      showCancelButton: true,
      confirmButtonColor: '#d33',
      cancelButtonColor: '#3085d6',
      confirmButtonText: 'Sí, eliminar',
      cancelButtonText: 'Cancelar'
    }).then((result) => {
      if (result.isConfirmed) {
        onEliminar(id);
      }
    });
  };
  if (!personas || personas.length === 0) {
    return (
      <div className="no-data">
        <p>No hay personas registradas</p>
      </div>
    );
  }

  return (
    <div className="persona-lista-container">
      <div className="table-responsive">
        <table className="persona-tabla">
          <thead>
            <tr>
              <th>ID</th>
              <th>Nombre Completo</th>
              <th>Documento</th>
              <th>Género</th>
              <th>Correo</th>
              <th>Teléfono</th>
              <th>Acciones</th>
            </tr>
          </thead>
          <tbody>
            {personas.map((persona) => (
              <tr key={persona.id}>
                <td>{persona.id}</td>
                <td>
                  {`${persona.primer_nombre} ${persona.segundo_nombre || ''} ${persona.primer_apellido} ${persona.segundo_apellido || ''}`.trim()}
                </td>
                <td>{persona.numero_documento}</td>
                <td>{persona.genero || '-'}</td>
                <td>{persona.correo_electronico || '-'}</td>
                <td>{persona.telefono || '-'}</td>
                <td className="acciones">
                  <button
                    className="btn-icon btn-edit"
                    onClick={() => onEditar(persona)}
                    title="Editar"
                  >
                    <i className="bi bi-pencil-square"></i>
                  </button>
                  <button
                    className="btn-icon btn-delete"
                    onClick={() => confirmarEliminar(
                      persona.id, 
                      `${persona.primer_nombre} ${persona.primer_apellido}`
                    )}
                    title="Eliminar"
                  >
                    <i className="bi bi-trash3-fill"></i>
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default PersonaLista;
