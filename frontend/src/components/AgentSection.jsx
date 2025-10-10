
import { motion } from "framer-motion";
import { useLocation } from "react-router-dom";
import "./AgentSection.css";

const agentMeta = [
  { key: "Creative", title: "Creative Agent", color: "rgba(255, 123, 100, 0.18)" },
  { key: "Finance", title: "Finance Agent", color: "rgba(100, 200, 255, 0.18)" },
  { key: "Inventory", title: "Inventory Agent", color: "rgba(100, 255, 180, 0.18)" },
];

export default function AgentSection() {
  const location = useLocation();
  const results = location.state?.results;
  const query = location.state?.query;
  const product = location.state?.product;

  return (
    <section className="agents" style={{
      minHeight: "100vh",
      display: "flex",
      flexDirection: "column",
      justifyContent: "center",
      alignItems: "center",
      background: "linear-gradient(135deg, #00dbde, #fc00ff)",
      padding: "4rem 2rem"
    }}>
      <motion.div
        initial={{ opacity: 0, y: 30 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.7 }}
        style={{
          background: "rgba(255,255,255,0.85)",
          borderRadius: "24px",
          boxShadow: "0 8px 40px rgba(2, 6, 23, 0.18)",
          padding: "2.5rem 2rem",
          maxWidth: "700px",
          width: "100%",
          marginBottom: "2rem"
        }}
      >
        <h2 style={{
          fontSize: "2rem",
          fontWeight: "bold",
          marginBottom: "1.5rem",
          textAlign: "center",
          background: "linear-gradient(90deg, #ff7eb9, #ff758c)",
          WebkitBackgroundClip: "text",
          WebkitTextFillColor: "transparent"
        }}>
          AI Agent Results
        </h2>
        <div style={{ textAlign: "center", marginBottom: "1.5rem", fontSize: "1.1rem" }}>
          <span style={{ color: "#fc00ff", fontWeight: 600 }}>Campaign:</span> {query}<br />
          <span style={{ color: "#00dbde", fontWeight: 600 }}>Product:</span> {product}
        </div>
        <div style={{ display: "flex", gap: "2rem", justifyContent: "center", flexWrap: "wrap" }}>
          {agentMeta.map((agent, idx) => (
            <motion.div
              key={agent.key}
              className="agent-card glass"
              style={{
                backgroundColor: agent.color,
                flex: 1,
                minWidth: "200px",
                maxWidth: "220px",
                margin: "0.5rem 0"
              }}
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: idx * 0.3 }}
            >
              <h3 style={{
                fontSize: "1.2rem",
                fontWeight: "bold",
                marginBottom: "1rem",
                background: "linear-gradient(90deg, #00dbde, #fc00ff)",
                WebkitBackgroundClip: "text",
                WebkitTextFillColor: "transparent"
              }}>{agent.title}</h3>
              <p style={{ fontSize: "1rem", color: "#333" }}>
                {results ? results[agent.key] : "Awaiting input..."}
              </p>
            </motion.div>
          ))}
        </div>
        {results?.["Final Plan"] && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 1.2 }}
            style={{
              marginTop: "2.5rem",
              padding: "1.5rem",
              background: "linear-gradient(90deg, #ff7eb9, #ff758c)",
              borderRadius: "16px",
              color: "#fff",
              fontWeight: "bold",
              fontSize: "1.1rem",
              boxShadow: "0 4px 20px rgba(255, 123, 100, 0.18)"
            }}
          >
            Final Plan: {results["Final Plan"]}
          </motion.div>
        )}
      </motion.div>
    </section>
  );
}
