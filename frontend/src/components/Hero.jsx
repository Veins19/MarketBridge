import React from "react";
import { motion } from "framer-motion";
import { useNavigate } from "react-router-dom";

const BlobBackground = () => (
  <svg
    style={{
      position: "absolute",
      top: 0,
      left: 0,
      width: "100%",
      height: "100%",
      zIndex: -1,
      filter: "blur(70px)",
      opacity: 0.3,
      transform: "translate3d(0, 0, 0)"
    }}
    viewBox="0 0 600 600"
    xmlns="http://www.w3.org/2000/svg"
  >
    <motion.path
      fill="url(#gradient)"
      animate={{
        d: [
          "M421.7,316Q379,382,316.5,415Q254,448,184.5,419.5Q115,391,83,331.5Q51,272,81.5,215Q112,158,179.5,114.5Q247,71,310,109Q373,147,423,195Q473,243,421.7,316Z",
          "M411,302.5Q353,365,298,387Q243,409,196,377.5Q149,346,122,292.5Q95,239,123.5,188.5Q152,138,207.5,111Q263,84,322,95Q381,106,413,158Q445,210,411,302.5Z",
          "M404,306Q356,362,298.5,389.5Q241,417,183.5,375Q126,333,119,268.5Q112,204,163,154.5Q214,105,273,90Q332,75,393,120Q454,165,404,306Z",
          "M421.7,316Q379,382,316.5,415Q254,448,184.5,419.5Q115,391,83,331.5Q51,272,81.5,215Q112,158,179.5,114.5Q247,71,310,109Q373,147,423,195Q473,243,421.7,316Z"
        ]
      }}
      transition={{ repeat: Infinity, duration: 20, ease: "easeInOut" }}
    />
    <defs>
      <linearGradient id="gradient" x1="0" y1="0" x2="1" y2="1">
        <stop offset="0%" stopColor="#7c3aed" />
        <stop offset="100%" stopColor="#06b6d4" />
      </linearGradient>
    </defs>
  </svg>
);

export default function Hero() {
  const navigate = useNavigate();

  return (
    <section
      style={{
        position: "relative",
        height: "100vh",
        display: "flex",
        flexDirection: "column",
        justifyContent: "center",
        alignItems: "center",
        padding: "3rem 1rem",
        overflow: "hidden",
        backgroundColor: "#12152e"
      }}
    >
      <BlobBackground />
      <motion.h1
        initial={{ opacity: 0, y: 50 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 1.2, ease: "easeOut" }}
        style={{
          fontFamily: "'Lexend', 'Inter', sans-serif",
          fontWeight: 900,
          fontSize: "3.8rem",
          maxWidth: "700px",
          textAlign: "center",
          marginBottom: "1rem",
          background:
            "linear-gradient(90deg, #7c3aed 0%, #06b6d4 50%, #ff61a6 100%)",
          WebkitBackgroundClip: "text",
          WebkitTextFillColor: "transparent",
          userSelect: "none",
          lineHeight: 1.1,
          letterSpacing: "-0.03em",
          textShadow: "0px 2px 12px rgba(124, 58, 237, 0.6)"
        }}
      >
        Design Campaigns Faster. Smarter. Futuristic.
      </motion.h1>
      <motion.p
        initial={{ opacity: 0, y: 40 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.3, duration: 1 }}
        style={{
          fontFamily: "'Inter', sans-serif",
          fontWeight: 400,
          fontSize: "1.1rem",
          maxWidth: "460px",
          marginBottom: "2.5rem",
          color: "rgba(200, 210, 240, 0.8)",
          textAlign: "center",
          userSelect: "none"
        }}
      >
        Empower your marketing, finance, and inventory planning with
        AI-driven agent collaboration.
      </motion.p>

      <motion.button
        onClick={() => navigate("/campaign")}
        whileHover={{ scale: 1.06, boxShadow: "0 0 16px #7c3aed" }}
        whileTap={{ scale: 0.96 }}
        style={{
          padding: "1.2rem 3.2rem",
          fontSize: "1.15rem",
          fontWeight: "700",
          color: "#fff",
          borderRadius: "28px",
          border: "none",
          cursor: "pointer",
          background:
            "linear-gradient(90deg, #7c3aed, #06b6d4, #ff61a6)",
          boxShadow:
            "0 0 10px rgba(124, 58, 237, 0.8), 0 0 30px rgba(6, 182, 212, 0.8), 0 0 40px #ff61a6",
          userSelect: "none",
          transition: "all 0.3s ease"
        }}
      >
        Get Started
      </motion.button>
    </section>
  );
}
