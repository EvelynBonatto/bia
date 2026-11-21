import React, { useRef, useState } from "react";
import Modal from "./Modal";

const AddTask = ({ onAdd }) => {
  const [titulo, setTitulo] = useState("");
  const [dia, setDia] = useState("");
  const [importante, setImportante] = useState(true);
  const [showModal, setShowModal] = useState(false);
  const calendarioRef = useRef(null);

  // Abre o calendário nativo do navegador (input type="date" escondido)
  const abrirCalendario = () => {
    calendarioRef.current?.showPicker?.();
  };

  // O input date devolve "AAAA-MM-DD"; a API espera a string "DD/MM/AAAA"
  const onEscolherData = (e) => {
    if (!e.target.value) {
      setDia("");
      return;
    }
    const [ano, mes, diaDoMes] = e.target.value.split("-");
    setDia(`${diaDoMes}/${mes}/${ano}`);
  };

  const onSubmit = (e) => {
    e.preventDefault();

    if (!titulo.trim()) {
      setShowModal(true);
      return;
    }

    onAdd({ 
      titulo: titulo.trim(), 
      dia_atividade: dia || new Date().toLocaleDateString('pt-BR'), 
      importante 
    });

    setTitulo("");
    setDia("");
    setImportante(true);
  };

  return (
    <form className="add-form" onSubmit={onSubmit}>
      <div className="form-control">
        <label>Tarefa</label>
        <input
          type="text"
          placeholder="O que você precisa fazer?"
          value={titulo}
          onChange={(e) => setTitulo(e.target.value)}
        />
      </div>
      
      <div className="form-control form-control-date">
        <label>Data/Prazo</label>
        <input
          type="text"
          placeholder="Quando?"
          value={dia}
          readOnly
          onClick={abrirCalendario}
          onKeyDown={(e) => {
            if (e.key === "Enter" || e.key === " ") {
              e.preventDefault();
              abrirCalendario();
            }
          }}
        />
        <input
          type="date"
          ref={calendarioRef}
          className="date-picker-hidden"
          tabIndex={-1}
          aria-hidden="true"
          value={dia ? dia.split("/").reverse().join("-") : ""}
          onChange={onEscolherData}
        />
      </div>
      
      <div className="form-control-check">
        <input
          type="checkbox"
          id="importante"
          checked={importante}
          onChange={(e) => setImportante(e.target.checked)}
        />
        <label htmlFor="importante">Importante</label>
      </div>
      
      <button type="submit" className="btn btn-block success">
        Add New Task
      </button>
      
      <Modal
        isOpen={showModal}
        onClose={() => setShowModal(false)}
        title="Campo obrigatório"
        message="Por favor, adicione uma descrição para a tarefa"
        type="warning"
      />
    </form>
  );
};

export default AddTask;
