import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { runCampaign } from "../api";
import { motion } from "framer-motion";

export default function CampaignForm() {
  const [query, setQuery] = useState("");
  const [product, setProduct] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    try {
      const results = await runCampaign(query, product);
      navigate("/agents", { state: { results, query, product } });
    } catch (err) {
      setError("Failed to get results. Please try again.");
    }
    setLoading(false);
  };

  return (
    <section
      style={{
        minHeight: "100vh",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        backgroundColor: "#12152e",
        padding: "3rem 1rem",
      }}
    >
      <motion.form
        onSubmit={handleSubmit}
        initial={{ opacity: 0, y: 30 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8 }}
        style={{
          background: "rgba(255, 255, 255, 0.07)",
          borderRadius: "24px",
          padding: "3rem 3.5rem",
          width: "100%",
          maxWidth: 460,
          backdropFilter: "blur(22px)",
          boxShadow: "0 8px 48px rgba(124, 58, 237, 0.25)",
          border: "1.5px solid rgba(124, 58, 237, 0.3)",
          color: "#e1e6f9",
          fontFamily: "'Inter', sans-serif",
          userSelect: "none",
        }}
      >
        <h2
          style={{
            fontFamily: "'Lexend', 'Inter', sans-serif",
            fontWeight: 900,
            fontSize: "2.5rem",
            marginBottom: "1.8rem",
            background:
              "linear-gradient(90deg, #7c3aed 0%, #06b6d4 80%)",
            WebkitBackgroundClip: "text",
            WebkitTextFillColor: "transparent",
            textAlign: "center",
          }}
        >
          Plan Your Campaign
        </h2>

        <div style={{ position: "relative", marginBottom: "2rem" }}>
          <input
            id="campaign-input"
            type="text"
            autoFocus
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            required
            style={{
              width: "100%",
              padding: "1.2rem 1.4rem",
              borderRadius: "14px",
              border: "1.5px solid rgba(255,255,255,0.2)",
              outline: "none",
              background: "rgba(255, 255, 255, 0.08)",
              color: "#fff",
              fontSize: "1.15rem",
              transition: "all 0.3s ease",
              boxShadow: "inset 0 0 5px rgba(124, 58, 237, 0.4)",
            }}
            onFocus={(e) =>
              (e.target.style.border = "1.5px solid #7c3aed")}
            onBlur={(e) =>
              (e.target.style.border = "1.5px solid rgba(255,255,255,0.2)")}
            placeholder=" "
          />
          <label
            htmlFor="campaign-input"
            style={{
              position: "absolute",
              top: 14,
              left: 14,
              fontSize: "0.9rem",
              color: "rgba(255, 255, 255, 0.5)",
              pointerEvents: "none",
              transition: "all 0.3s ease",
              fontWeight: 600,
              userSelect: "none",
            }}
          >
            Campaign request
          </label>
        </div>

        <div style={{ position: "relative", marginBottom: "2.5rem" }}>
          <input
            id="product-input"
            type="text"
            value={product}
            onChange={(e) => setProduct(e.target.value)}
            required
            style={{
              width: "100%",
              padding: "1.2rem 1.4rem",
              borderRadius: "14px",
              border: "1.5px solid rgba(255,255,255,0.2)",
              outline: "none",
              background: "rgba(255, 255, 255, 0.08)",
              color: "#fff",
              fontSize: "1.15rem",
              transition: "all 0.3s ease",
              boxShadow: "inset 0 0 5px rgba(6, 182, 212, 0.4)",
            }}
            onFocus={(e) =>
              (e.target.style.border = "1.5px solid #06b6d4")}
            onBlur={(e) =>
              (e.target.style.border = "1.5px solid rgba(255,255,255,0.2)")}
            placeholder=" "
          />
          <label
            htmlFor="product-input"
            style={{
              position: "absolute",
              top: 14,
              left: 14,
              fontSize: "0.9rem",
              color: "rgba(255, 255, 255, 0.5)",
              pointerEvents: "none",
              transition: "all 0.3s ease",
              fontWeight: 600,
              userSelect: "none",
            }}
          >
            Product name
          </label>
        </div>

        <motion.button
          type="submit"
          style={{
            padding: "1.2rem 2rem",
            borderRadius: "28px",
            fontWeight: "700",
            fontSize: "1.2rem",
            color: "#fff",
            border: "none",
            cursor: loading ? "not-allowed" : "pointer",
            background:
              loading
                ? "linear-gradient(90deg,#7c3aed99,#06b6d499)"
                : "linear-gradient(90deg,#7c3aed,#06b6d4)",
            boxShadow: loading
              ? "0 0 12px #7c3aed99, 0 0 24px #06b6d499"
              : "0 0 24px #7c3aed, 0 0 48px #06b6d4",
            transition: "all 0.3s ease",
            userSelect: "none",
            display: "flex",
            justifyContent: "center",
            alignItems: "center",
          }}
          whileHover={{ scale: loading ? 1 : 1.05, boxShadow: "0 0 32px #7c3aed" }}
          whileTap={{ scale: loading ? 1 : 0.95 }}
          disabled={loading}
        >
          {loading ? "Processing..." : "Submit"}
        </motion.button>

        {error && (
          <div
            style={{
              marginTop: "1rem",
              fontWeight: "600",
              color: "#ff6584",
              textAlign: "center",
            }}
          >
            {error}
          </div>
        )}
      </motion.form>
    </section>
  );
}
