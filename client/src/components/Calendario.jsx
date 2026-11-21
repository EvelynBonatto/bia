import React, { useEffect, useRef, useState } from "react";
import { FaChevronLeft, FaChevronRight } from "react-icons/fa";

const MESES = [
  "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
  "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro",
];
const DIAS_SEMANA = ["Dom", "Seg", "Ter", "Qua", "Qui", "Sex", "Sáb"];

// Converte uma data do JavaScript para a string "DD/MM/AAAA"
const formatarData = (data) => {
  const dia = String(data.getDate()).padStart(2, "0");
  const mes = String(data.getMonth() + 1).padStart(2, "0");
  return `${dia}/${mes}/${data.getFullYear()}`;
};

// Converte a string "DD/MM/AAAA" para uma data do JavaScript
const lerData = (texto) => {
  const [dia, mes, ano] = texto.split("/").map(Number);
  return new Date(ano, mes - 1, dia);
};

const Calendario = ({ dataSelecionada, onEscolher, onFechar }) => {
  const hoje = new Date();
  const inicial = dataSelecionada ? lerData(dataSelecionada) : hoje;
  const [mes, setMes] = useState(inicial.getMonth());
  const [ano, setAno] = useState(inicial.getFullYear());
  const calendarioRef = useRef(null);

  // Fecha o calendário ao clicar fora dele ou apertar Esc
  useEffect(() => {
    const clicarFora = (e) => {
      if (!calendarioRef.current?.parentElement.contains(e.target)) onFechar();
    };
    const apertarEsc = (e) => {
      if (e.key === "Escape") onFechar();
    };
    document.addEventListener("mousedown", clicarFora);
    document.addEventListener("keydown", apertarEsc);
    return () => {
      document.removeEventListener("mousedown", clicarFora);
      document.removeEventListener("keydown", apertarEsc);
    };
  }, [onFechar]);

  const mudarMes = (passo) => {
    const novo = new Date(ano, mes + passo, 1);
    setMes(novo.getMonth());
    setAno(novo.getFullYear());
  };

  // Espaços vazios antes do dia 1 + os dias do mês
  const primeiroDiaSemana = new Date(ano, mes, 1).getDay();
  const totalDias = new Date(ano, mes + 1, 0).getDate();
  const celulas = [
    ...Array(primeiroDiaSemana).fill(null),
    ...Array.from({ length: totalDias }, (_, i) => i + 1),
  ];

  return (
    <div className="calendario" ref={calendarioRef}>
      <div className="calendario-header">
        <button type="button" onClick={() => mudarMes(-1)} title="Mês anterior">
          <FaChevronLeft />
        </button>
        <span>{MESES[mes]} {ano}</span>
        <button type="button" onClick={() => mudarMes(1)} title="Próximo mês">
          <FaChevronRight />
        </button>
      </div>

      <div className="calendario-grid">
        {DIAS_SEMANA.map((nome) => (
          <span key={nome} className="calendario-dia-semana">{nome}</span>
        ))}

        {celulas.map((dia, i) => {
          if (!dia) return <span key={`vazio-${i}`} />;

          const texto = formatarData(new Date(ano, mes, dia));
          const classes = ["calendario-dia"];
          if (texto === dataSelecionada) classes.push("selecionado");
          if (texto === formatarData(hoje)) classes.push("hoje");

          return (
            <button
              key={texto}
              type="button"
              className={classes.join(" ")}
              onClick={() => onEscolher(texto)}
            >
              {dia}
            </button>
          );
        })}
      </div>
    </div>
  );
};

export default Calendario;
