import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { Bar, BarChart, CartesianGrid, XAxis, YAxis } from "recharts";
import {
  ChartContainer,
  ChartTooltip,
  ChartTooltipContent,
} from "@/components/ui/chart";

const apiUrl = import.meta.env.VITE_API_URL || "http://localhost:8080";

// Configuração do gráfico (shadcn/ui): nome e cor de cada série
const chartConfig = {
  quantidade: {
    label: "Tarefas",
    color: "var(--accent-primary)",
  },
};

const Analytics = () => {
  const [tasks, setTasks] = useState([]);
  const [carregando, setCarregando] = useState(true);
  const [erro, setErro] = useState(false);

  // Busca as tarefas sempre que a tela é aberta, para mostrar os dados atualizados
  useEffect(() => {
    const buscarTarefas = async () => {
      try {
        const res = await fetch(`${apiUrl}/api/tarefas`);
        if (!res.ok) {
          throw new Error(`HTTP ${res.status}`);
        }
        const json = await res.json();
        // A API pode responder com { data: [...] } (com cache) ou direto com a lista
        setTasks(json.data || json);
      } catch (error) {
        console.warn("Falha ao carregar tarefas:", error.message);
        setErro(true);
      } finally {
        setCarregando(false);
      }
    };

    buscarTarefas();
  }, []);

  const importantes = tasks.filter((task) => task.importante).length;
  const naoImportantes = tasks.length - importantes;

  const chartData = [
    { prioridade: "Importantes", quantidade: importantes },
    { prioridade: "Não importantes", quantidade: naoImportantes },
  ];

  const renderConteudo = () => {
    if (carregando) {
      return <p className="analytics-message">Carregando...</p>;
    }

    if (erro) {
      return (
        <p className="analytics-message">Não foi possível carregar as tarefas</p>
      );
    }

    if (tasks.length === 0) {
      return (
        <div className="empty-state">
          <h3>Não há tarefas para exibir 📊</h3>
          <p>Cadastre tarefas na tela inicial para ver o gráfico.</p>
        </div>
      );
    }

    return (
      <ChartContainer config={chartConfig} className="analytics-chart">
        <BarChart accessibilityLayer data={chartData}>
          <CartesianGrid vertical={false} />
          <XAxis dataKey="prioridade" tickLine={false} axisLine={false} />
          <YAxis allowDecimals={false} tickLine={false} axisLine={false} />
          <ChartTooltip content={<ChartTooltipContent />} />
          <Bar dataKey="quantidade" fill="var(--color-quantidade)" radius={8} />
        </BarChart>
      </ChartContainer>
    );
  };

  return (
    <div className="about-page">
      <div className="about-content">
        <div className="analytics-header">
          <h2>📊 Analytics</h2>
          <p>Quantidade de tarefas por prioridade</p>
        </div>
        {renderConteudo()}
      </div>

      <div className="about-footer">
        <Link to="/" className="back-button">
          ← Voltar
        </Link>
      </div>
    </div>
  );
};

export default Analytics;
