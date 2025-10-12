import React from "react";
import { useLocation } from "react-router-dom";
import { motion } from "framer-motion";
import AgentCollaborationTimeline from "./AgentCollaborationTimeline.jsx";


const agents = [
  {
    key: "Creative",
    label: "Creative Agent",
    gradient: "linear-gradient(135deg, #ff61a6 0%, #7c3aed 100%)",
    avatar: "🎨",
  },
  {
    key: "Finance",
    label: "Finance Agent",
    gradient: "linear-gradient(135deg, #06b6d4 0%, #00f2fe 100%)",
    avatar: "💰",
  },
  {
    key: "Inventory",
    label: "Inventory Agent",
    gradient: "linear-gradient(135deg, #1de9b6 0%, #60efff 100%)",
    avatar: "📦",
  },
];

export default function AgentSection() {
  const location = useLocation();
  const results = location.state?.results;
  const query = location.state?.query;
  const product = location.state?.product;

  return (
    <section
      style={{
        minHeight: "100vh",
        padding: "3rem 2rem",
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        backgroundColor: "#12152e",
        position: "relative",
      }}
    >
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8 }}
        style={{
          background: "rgba(255, 255, 255, 0.07)",
          borderRadius: "24px",
          padding: "2.5rem 2rem",
          maxWidth: 900,
          width: "100%",
          boxShadow: "0 6px 40px rgba(124, 58, 237, 0.2)",
          backdropFilter: "blur(18px)",
          border: "1.5px solid rgba(124, 58, 237, 0.3)",
          color: "#ddd",
          marginBottom: "2rem",
          textAlign: "center",
        }}
      >
        <h2
          style={{
            fontWeight: 900,
            fontSize: "2.2rem",
            fontFamily: "'Lexend', 'Inter', sans-serif",
            background:
              "linear-gradient(90deg, #ff61a6, #7c3aed, #06b6d4)",
            WebkitBackgroundClip: "text",
            WebkitTextFillColor: "transparent",
            marginBottom: "0.8rem",
          }}
        >
          AI Agent Collaboration Results
        </h2>
        <div style={{ fontSize: "1.1rem", color: "#bbb" }}>
          Campaign: <strong style={{ color: "#ff61a6" }}>{query || "N/A"}</strong> | Product:{" "}
          <strong style={{ color: "#06b6d4" }}>{product || "N/A"}</strong>
        </div>
      </motion.div>

      <div
        style={{
          display: "flex",
          gap: "2rem",
          flexWrap: "wrap",
          justifyContent: "center",
          maxWidth: 920,
          width: "100%",
        }}
      >
        {agents.map((agent, i) => (
          <motion.div
            key={agent.key}
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: i * 0.15, duration: 0.8 }}
            style={{
              flex: "1 1 280px",
              background: agent.gradient,
              borderRadius: "20px",
              color: "#fff",
              padding: "2rem",
              boxShadow: `0 0 20px 1px ${agent.gradient
                .replace("linear-gradient(135deg,", "")
                .replace("0%,", "")
                .replace("100%)", "")}`,
              border: "1.5px solid rgba(255, 255, 255, 0.1)",
              cursor: "default",
              display: "flex",
              flexDirection: "column",
              alignItems: "center",
              userSelect: "none",
              position: "relative",
            }}
          >
            <div
              style={{
                fontSize: "3rem",
                marginBottom: "1rem",
                filter:
                  "drop-shadow(0 0 8px rgba(0,0,0,0.15)) drop-shadow(0 0 10px #fff)",
              }}
              aria-label={`${agent.label} icon`}
            >
              {agent.avatar}
            </div>
            <h3
              style={{
                fontFamily: "'Lexend', 'Inter', sans-serif",
                fontWeight: 700,
                fontSize: "1.6rem",
                marginBottom: "1rem",
                textShadow: "0 2px 6px rgba(0,0,0,0.25)",
              }}
            >
              {agent.label}
            </h3>
            <p
              style={{
                minHeight: "72px",
                fontSize: "1rem",
                color: "#e0e7ffdd",
                textAlign: "center",
                lineHeight: "1.3",
              }}
            >
              {results ? results[agent.key] : "Agent awaiting input..."}
            </p>
          </motion.div>
        ))}
      </div>
<AgentCollaborationTimeline results={results} />

      {results?.["Final Plan"] && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.5, duration: 0.8 }}
          style={{
            marginTop: "3rem",
            padding: "1.6rem 2rem",
            maxWidth: 900,
            background:
              "linear-gradient(135deg, #7c3aedcc, #06b6d4cc)",
            borderRadius: "20px",
            boxShadow: "0 6px 24px rgba(124, 58, 237, 0.35)",
            color: "#fff",
            fontWeight: 700,
            fontSize: "1.25rem",
            userSelect: "none",
            textAlign: "center",
          }}
        >
          Final Plan: {results["Final Plan"]}
        </motion.div>
      )}
    </section>
  );
}
