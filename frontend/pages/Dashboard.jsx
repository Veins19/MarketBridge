/* eslint-disable no-unused-vars */
import React, { useState } from "react";
import Header from "../components/Header";
import AgentCard from "../components/AgentCard";
import LoadingDots from "../components/LoadingDots";
import { runCampaign } from "../api";
import { motion } from "framer-motion";

export default function Dashboard() {
  const [query, setQuery] = useState("Plan a festive sale for Smartphone X within ₹2 lakh");
  const [product, setProduct] = useState("Smartphone X");
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleRun = async () => {
    setLoading(true);
    setError(null);
    setResults(null);
    try {
      const res = await runCampaign(query, product);
      // slight delay to let animation feel nicer
      await new Promise((r) => setTimeout(r, 350));
      setResults(res);
    } catch (e) {
      setError("Backend request failed. Is the backend running?");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="page">
      <Header />
      <main className="container">
        <section className="hero glass">
          <div className="hero-left">
            <h1>Design campaigns faster. Smarter.</h1>
            <p className="muted">
              Ask in plain English and our agent network will produce a campaign plan,
              validate budget, and confirm inventory — all with explainable reasoning.
            </p>

            <label className="field-label">Campaign request</label>
            <textarea
              className="input area"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
            />

            <div className="row">
              <div style={{ flex: 1 }}>
                <label className="field-label">Product</label>
                <input
                  className="input"
                  value={product}
                  onChange={(e) => setProduct(e.target.value)}
                />
              </div>

              <div style={{ width: 160, marginLeft: 16 }}>
                <label className="field-label">&nbsp;</label>
                <motion.button
                  whileTap={{ scale: 0.98 }}
                  whileHover={{ scale: 1.03 }}
                  className="cta"
                  onClick={handleRun}
                >
                  🚀 Generate Plan
                </motion.button>
              </div>
            </div>

            {loading && <LoadingDots text="Agents collaborating..." />}
            {error && <div className="error">{error}</div>}
          </div>

          <div className="hero-right">
            <div className="kpi-grid">
              <div className="kpi glass small">
                <div className="kpi-value">+12%</div>
                <div className="kpi-label">Projected Uplift</div>
              </div>
              <div className="kpi glass small">
                <div className="kpi-value">₹2.0L</div>
                <div className="kpi-label">Budget</div>
              </div>
              <div className="kpi glass small">
                <div className="kpi-value">3 agents</div>
                <div className="kpi-label">Collaborators</div>
              </div>
            </div>

            <motion.div
              initial={{ opacity: 0, y: 8 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.2 }}
              className="mock-phone glass"
            >
              <div className="phone-header">Campaign Preview</div>
              <div className="phone-body">
                <div className="preview-title">Festive Flash Sale — Smartphone X</div>
                <div className="preview-section">Target: Young customers (South)</div>
                <div className="preview-section">Discount: 15% off</div>
                <div className="preview-section">Est. Revenue Uplift: +12%</div>
              </div>
            </motion.div>
          </div>
        </section>

        <section style={{ marginTop: 28 }}>
          <h3 className="section-title">Agent Outputs</h3>
          {!results && (
            <p className="muted">Run the planner to see agent collaboration and reasoning.</p>
          )}

          <div className="grid">
            {results && (
              <>
                <AgentCard title="Creative Agent" content={results.Creative} color="#06b6d4" />
                <AgentCard title="Finance Agent" content={results.Finance} color="#f59e0b" />
                <AgentCard title="Inventory Agent" content={results.Inventory} color="#ef4444" />
              </>
            )}
          </div>

          {results && (
            <motion.div
              initial={{ opacity: 0, y: 12 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.15 }}
              className="glass final"
            >
              <h4 className="card-title">Final Plan</h4>
              <p className="card-body">{results["Final Plan"]}</p>
            </motion.div>
          )}
        </section>
      </main>
      <footer className="footer">Team — AIMarketer • Hackathon Demo</footer>
    </div>
  );
}
