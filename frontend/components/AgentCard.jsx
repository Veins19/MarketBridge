import React from "react";
// eslint-disable-next-line no-unused-vars
import { motion } from "framer-motion";

export default function AgentCard({ title, content, color }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 12, scale: 0.98 }}
      animate={{ opacity: 1, y: 0, scale: 1 }}
      transition={{ duration: 0.35 }}
      className="glass card"
      style={{ borderLeft: `4px solid ${color || "#7c3aed"}` }}
    >
      <h4 className="card-title">{title}</h4>
      <p className="card-body">{content}</p>
    </motion.div>
  );
}
