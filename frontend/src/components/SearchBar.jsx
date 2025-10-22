import { useState } from 'react';
import './SearchBar.css';

const SearchBar = ({ onBuscar, onNuevo }) => {
  const [termino, setTermino] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    onBuscar(termino);
  };

  const handleClear = () => {
    setTermino('');
    onBuscar('');
  };

  return (
    <div className="search-bar">
      <form onSubmit={handleSubmit} className="search-form">
        <input
          type="text"
          placeholder="Buscar por nombre, apellido o documento..."
          value={termino}
          onChange={(e) => setTermino(e.target.value)}
          className="search-input"
        />
        <button type="submit" className="btn btn-search">
          Buscar
        </button>
        {termino && (
          <button type="button" className="btn btn-clear" onClick={handleClear}>
            Limpiar
          </button>
        )}
      </form>
      <button className="btn btn-new" onClick={onNuevo}>
          Nueva Persona
      </button>
    </div>
  );
};

export default SearchBar;
