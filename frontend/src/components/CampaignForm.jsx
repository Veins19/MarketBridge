/* eslint-disable no-unused-vars */



import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { runCampaign } from "../api";
import { motion } from "framer-motion";

export default function CampaignForm() {
  const [query, setQuery] = useState("");
  const [product, setProduct] = useState("");
  const navigate = useNavigate();


  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    try {
      const results = await runCampaign(query, product);
      navigate("/agents", { state: { results, query, product } });
    } catch (err) {
      console.error("Error in runCampaign:", err);
      setError("Failed to get results. Please try again.");
    } finally {
      setLoading(false);
    }
  };


  return (
    <section id="campaign-form" style={{
      minHeight: "100vh",
      display: "flex",
      flexDirection: "column",
      justifyContent: "center",
      alignItems: "center",
      background: "linear-gradient(135deg, #ff7eb9, #ff758c)",
    }}>
      <motion.div
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.7 }}
        style={{
          background: "rgba(255,255,255,0.85)",
          borderRadius: "24px",
          boxShadow: "0 8px 40px rgba(2, 6, 23, 0.18)",
          padding: "2.5rem 2rem",
          maxWidth: "420px",
          width: "100%",
          margin: "2rem 0"
        }}
      >
        <h2 style={{
          fontSize: "2.2rem",
          fontWeight: "bold",
          marginBottom: "2rem",
          textAlign: "center",
          background: "linear-gradient(90deg, #00dbde, #fc00ff)",
          WebkitBackgroundClip: "text",
          WebkitTextFillColor: "transparent"
        }}>
          Start Your Campaign
        </h2>
        <form onSubmit={handleSubmit}>
          <motion.div
            initial={{ opacity: 0, x: -30 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.6 }}
            style={{ marginBottom: "1.5rem" }}
          >
            <label style={{ display: "block", marginBottom: "0.5rem", fontWeight: 600 }}>Enter campaign request</label>
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              style={{
                width: "100%",
                padding: "1rem",
                borderRadius: "12px",
                border: "1px solid #e0e0e0",
                fontSize: "1rem",
                outline: "none",
                boxShadow: "0 2px 8px rgba(0,0,0,0.04)"
              }}
              required
            />
          </motion.div>
          <motion.div
            initial={{ opacity: 0, x: 30 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.6, delay: 0.2 }}
            style={{ marginBottom: "1.5rem" }}
          >
            <label style={{ display: "block", marginBottom: "0.5rem", fontWeight: 600 }}>Enter product name</label>
            <input
              type="text"
              value={product}
              onChange={(e) => setProduct(e.target.value)}
              style={{
                width: "100%",
                padding: "1rem",
                borderRadius: "12px",
                border: "1px solid #e0e0e0",
                fontSize: "1rem",
                outline: "none",
                boxShadow: "0 2px 8px rgba(0,0,0,0.04)"
              }}
              required
            />
          </motion.div>
          <motion.button
            type="submit"
            style={{
              width: "100%",
              padding: "1rem",
              background: "linear-gradient(90deg, #00dbde, #fc00ff)",
              color: "#fff",
              fontWeight: "bold",
              fontSize: "1.1rem",
              border: "none",
              borderRadius: "12px",
              cursor: loading ? "not-allowed" : "pointer",
              boxShadow: "0 8px 30px rgba(0, 219, 222, 0.18)",
              transition: "all 0.3s",
              opacity: loading ? 0.7 : 1
            }}
            disabled={loading}
            whileHover={{ scale: loading ? 1 : 1.04 }}
            whileTap={{ scale: loading ? 1 : 0.98 }}
          >
            {loading ? (
              <span style={{ display: "flex", alignItems: "center", justifyContent: "center" }}>
                <motion.span
                  initial={{ rotate: 0 }}
                  animate={{ rotate: 360 }}
                  transition={{ repeat: Infinity, duration: 1 }}
                  style={{
                    display: "inline-block",
                    width: "22px",
                    height: "22px",
                    border: "3px solid #fff",
                    borderTop: "3px solid #00dbde",
                    borderRadius: "50%",
                    marginRight: "8px"
                  }}
                />
                Processing...
              </span>
            ) : "Submit"}
          </motion.button>
          {error && <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} style={{ color: "#fc00ff", marginTop: "1rem", textAlign: "center" }}>{error}</motion.div>}
        </form>
      </motion.div>
    </section>
  );
}
