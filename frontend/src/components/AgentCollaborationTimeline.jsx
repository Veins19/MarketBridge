import React, { useState } from "react";
import { motion } from "framer-motion";

const timelineSteps = [
  {
    key: "Creative",
    label: "Creative Agent",
    color: "#7c3aed",
    description: "Proposing creative campaign content and design ideas."
  },
  {
    key: "Finance",
    label: "Finance Agent",
    color: "#06b6d4",
    description: "Validating financial feasibility and budgeting constraints."
  },
  {
    key: "Inventory",
    label: "Inventory Agent",
    color: "#ff61a6",
    description: "Checking product availability and stock levels."
  },
  {
    key: "Negotiation",
    label: "Agent Negotiation",
    color: "#ff8c00",
    description:
      "Agents collaboratively debating and adjusting plan parameters."
  },
  {
    key: "Final",
    label: "Final Campaign Plan",
    color: "#00ffab",
    description: "Presenting the final, optimized campaign plan and summary."
  }
];

export default function AgentCollaborationTimeline({ results }) {
  const [expandedStep, setExpandedStep] = useState(null);

  return (
    <section
      style={{
        maxWidth: 700,
        margin: "3rem auto",
        padding: "0 1rem",
        fontFamily: "'Inter', sans-serif",
        color: "#e1e6f9",
      }}
    >
      <h2
        style={{
          textAlign: "center",
          fontWeight: 900,
          fontSize: "2rem",
          marginBottom: "2rem",
          background:
            "linear-gradient(90deg, #7c3aed 0%, #06b6d4 80%)",
          WebkitBackgroundClip: "text",
          WebkitTextFillColor: "transparent",
          userSelect: "none"
        }}
      >
        Agent Collaboration Timeline
      </h2>

      <div style={{ position: "relative", paddingLeft: 24, borderLeft: "3px solid #7c3aed7a" }}>
        {timelineSteps.map(({ key, label, color, description }, index) => {
          const isActive = results && results[key];
          const isExpanded = expandedStep === index;

          return (
            <motion.div
              key={key}
              initial={{ opacity: 0, x: -40 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: index * 0.16, duration: 0.6 }}
              style={{ marginBottom: 32, cursor: "pointer" }}
              onClick={() => setExpandedStep(isExpanded ? null : index)}
              role="button"
              tabIndex={0}
              onKeyDown={(e) => {
                if (e.key === "Enter" || e.key === " ") {
                  setExpandedStep(isExpanded ? null : index);
                }
              }}
              aria-expanded={isExpanded}
              aria-controls={`${key}-details`}
            >
              <div
                style={{
                  position: "relative",
                  paddingLeft: 36,
                  display: "flex",
                  alignItems: "center",
                  fontWeight: 700,
                  fontSize: "1.15rem",
                  color: isActive ? color : "#5a5f78",
                  userSelect: "none",
                  textShadow: isActive ? `0 0 12px ${color}` : "none"
                }}
              >
                <motion.div
                  style={{
                    position: "absolute",
                    left: 0,
                    width: 20,
                    height: 20,
                    borderRadius: "50%",
                    backgroundColor: color,
                    boxShadow: isActive
                      ? `0 0 12px ${color}, 0 0 24px ${color}77`
                      : "none",
                  }}
                  animate={{ scale: isActive ? 1.3 : 1 }}
                  transition={{ type: "spring", stiffness: 300, damping: 20 }}
                />
                {label} {isActive ? "✅" : "⏳"}
              </div>

              {isExpanded && (
                <motion.div
                  id={`${key}-details`}
                  initial={{ opacity: 0, height: 0 }}
                  animate={{ opacity: 1, height: "auto" }}
                  exit={{ opacity: 0, height: 0 }}
                  style={{
                    marginTop: 10,
                    backgroundColor: "rgba(124, 58, 237, 0.1)",
                    padding: "12px 18px",
                    borderRadius: 12,
                    fontSize: "0.94rem",
                    userSelect: "text",
                  }}
                >
                  <p style={{ margin: 0, color: "#cfcfff" }}>
                    {description}
                  </p>
                  <p style={{ color: "#aaaaaa", marginTop: 6 }}>
                    <strong>Result:</strong>{" "}
                    {results ? results[key] : "No data available."}
                  </p>
                </motion.div>
              )}
            </motion.div>
          );
        })}
      </div>
    </section>
  );
}
