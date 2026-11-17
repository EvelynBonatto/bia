import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";

const Versao = () => {
  const [versao, setVersao] = useState(null);
  const [erro, setErro] = useState(false);
  const [status, setStatus] = useState("checking"); // 'checking', 'online', 'offline'

  // Mesma lógica de descoberta da URL da API usada no VersionInfo
  const getApiUrl = () => {
    if (import.meta.env.VITE_API_URL) {
      return import.meta.env.VITE_API_URL;
    }
    if (window.location.port === "8080") {
      return window.location.origin;
    }
    return "http://localhost:8080";
  };

  useEffect(() => {
    const buscarVersao = async () => {
      // Mesmo critério do VersionInfo: timeout de 5s e resposta OK = online
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 5000);
      try {
        const response = await fetch(`${getApiUrl()}/api/versao`, {
          signal: controller.signal,
          cache: "no-cache",
        });
        if (!response.ok) {
          throw new Error(`HTTP ${response.status}`);
        }
        setVersao(await response.text());
        setStatus("online");
      } catch (error) {
        console.warn("Falha ao obter a versão da API:", error.message);
        setErro(true);
        setStatus("offline");
      } finally {
        clearTimeout(timeoutId);
      }
    };

    buscarVersao();
  }, []);

  const textoStatus = {
    checking: "Verificando conexão...",
    online: "🟢 API online",
    offline: "🔴 API offline",
  };

  return (
    <div className="about-page">
      <div className="about-content">
        <div className="feature-grid">
          <div className="feature-card highlight">
            <h3>Versão</h3>
            {erro ? (
              <p>Não foi possível obter a versão da API</p>
            ) : (
              <h4>{versao || "Carregando..."}</h4>
            )}
            <p>{textoStatus[status]}</p>
          </div>
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
