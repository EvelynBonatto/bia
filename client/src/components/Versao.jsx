import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";

const Versao = () => {
  const [versao, setVersao] = useState(null);
  const [erro, setErro] = useState(false);

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
      try {
        const response = await fetch(`${getApiUrl()}/api/versao`, {
          cache: "no-cache",
        });
        if (!response.ok) {
          throw new Error(`HTTP ${response.status}`);
        }
        setVersao(await response.text());
      } catch (error) {
        console.warn("Falha ao obter a versão da API:", error.message);
        setErro(true);
      }
    };

    buscarVersao();
  }, []);

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
