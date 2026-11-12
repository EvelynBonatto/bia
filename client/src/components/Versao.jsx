import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { useLog } from "../contexts/LogContext.jsx";

const apiUrl = import.meta.env.VITE_API_URL || "http://localhost:8080";

const Versao = () => {
  const [version, setVersion] = useState("");
  const [status, setStatus] = useState("checking"); // 'checking', 'online', 'offline'
  const [lastCheck, setLastCheck] = useState(null);
  const { logApiRequest, logApiResponse, logApiError } = useLog();

  const fetchVersion = async () => {
    const url = `${apiUrl}/api/versao`;
    setStatus("checking");
    logApiRequest("GET", url);

    try {
      const res = await fetch(url);
      const data = await res.text();

      logApiResponse("GET", url, res.status, data);

      if (!res.ok) {
        throw new Error(`HTTP ${res.status}: ${res.statusText}`);
      }

      setVersion(data);
      setStatus("online");
      setLastCheck(new Date());
    } catch (error) {
      logApiError("GET", url, error);
      setStatus("offline");
      setVersion("");
      setLastCheck(new Date());
    }
  };

  useEffect(() => {
    fetchVersion();
  }, []);

  const getStatusIcon = () => {
    switch (status) {
      case "online":
        return "🟢";
      case "offline":
        return "🔴";
      case "checking":
        return "🟡";
      default:
        return "⚪";
    }
  };

  const getStatusText = () => {
    switch (status) {
      case "online":
        return "Online";
      case "offline":
        return "Offline";
      case "checking":
        return "Verificando...";
      default:
        return "Desconhecido";
    }
  };

  const getStatusClass = () => {
    switch (status) {
      case "online":
        return "versao-status--online";
      case "offline":
        return "versao-status--offline";
      case "checking":
        return "versao-status--checking";
      default:
        return "";
    }
  };

  const formatTime = (date) => {
    if (!date) return "--";
    return date.toLocaleTimeString("pt-BR", {
      hour: "2-digit",
      minute: "2-digit",
      second: "2-digit",
    });
  };

  return (
    <div className="about-page versao-page">
      <div className="about-content">
        {/* Hero com versão em destaque */}
        <div className="about-hero versao-hero">
          <h2>Versão da API</h2>
          {status === "online" ? (
            <p className="about-subtitle">{version}</p>
          ) : status === "checking" ? (
            <p className="about-subtitle">Verificando...</p>
          ) : (
            <p className="about-subtitle">Indisponível</p>
          )}
        </div>

        {/* Status da conexão */}
        <div className="feature-grid">
          <div className="feature-card">
            <h3>Status da Conexão</h3>
            <div className={`versao-status-badge ${getStatusClass()}`}>
              <span className="versao-status-icon">{getStatusIcon()}</span>
              <span>{getStatusText()}</span>
            </div>
            {lastCheck && (
              <p className="versao-meta">Última verificação: {formatTime(lastCheck)}</p>
            )}
          </div>
        </div>

        {/* Botões de ação */}
        <div className="versao-actions">
          {status === "offline" && (
            <button className="btn btn-block" onClick={fetchVersion}>
              🔄 Tentar novamente
            </button>
          )}
          {status === "online" && (
            <button className="btn btn-block" onClick={fetchVersion}>
              🔄 Atualizar
            </button>
          )}
          {status === "checking" && (
            <button className="btn btn-block" disabled>
              🔄 Verificando...
            </button>
          )}
        </div>
      </div>

      <div className="about-footer">
        <Link to="/" className="back-button">
          ← Voltar
        </Link>
      </div>
    </div>
  );
};

export default Versao;
