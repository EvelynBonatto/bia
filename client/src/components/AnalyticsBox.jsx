import React from "react";
import { Link } from "react-router-dom";

// Box da home que leva para a tela de Analytics
const AnalyticsBox = () => (
  <Link to="/analytics" className="analytics-box">
    <span className="analytics-box-icon">📊</span>
    <div className="analytics-box-text">
      <h3>Ver Analytics</h3>
      <p>Visualize suas tarefas por prioridade</p>
    </div>
    <span className="analytics-box-arrow">→</span>
  </Link>
);

export default AnalyticsBox;
