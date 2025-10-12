import React from "react";
import { useTheme } from "./ThemeContext.jsx";

export default function ThemeToggle() {
  const { theme, toggleTheme } = useTheme();

  return (
    <button
      onClick={toggleTheme}
      aria-label="Toggle theme"
      style={{
        padding: "8px 16px",
        borderRadius: 20,
        border: "none",
        background: "var(--accent2)",
        color: theme === "dark" ? "#fff" : "#21243b",
        fontWeight: 700,
        fontSize: "1rem",
        marginLeft: 10,
        cursor: "pointer",
        boxShadow: "var(--shadow-glow)",
        userSelect: "none",
        transition: "all 0.4s"
      }}
    >
      {theme === "dark" ? "Light Mode" : "Dark Mode"}
    </button>
  );
}
