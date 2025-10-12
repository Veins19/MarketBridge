import React from "react";
import ThemeToggle from "./ThemeToggle.jsx";
import { NavLink } from "react-router-dom";

const links = [
  { to: "/", label: "Home" },
  { to: "/campaign", label: "Campaign" },
  { to: "/agents", label: "Agents" }
];

export default function Header() {
  return (
    <header
      style={{
        position: "fixed",
        top: 0,
        left: 0,
        width: "100vw",
        height: 62,
        background: "var(--header-bg)",
        borderBottom: "2.5px solid var(--accent1)",
        boxShadow: "0 4px 14px 0 var(--accent1), 0 1px 2px 0 rgba(0,0,0,0.1)", // reduced glow and lighter shadow
        backdropFilter: "blur(14px)",
        zIndex: 2000,
        fontFamily: "'Lexend', 'Inter', sans-serif",
        userSelect: "none",
        transition: "background 0.3s, box-shadow 0.3s"
      }}
    >
      <div
        style={{
          maxWidth: 1150,
          margin: "0 auto",
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          height: "100%",
          padding: "0 1.2rem"
        }}
      >
        <div
          style={{
            fontWeight: 900,
            fontSize: "1.55rem",
            color: "var(--accent1)",
            letterSpacing: ".04em",
            cursor: "default",
            textShadow: "0 1px 5px var(--accent1)", // softer text shadow
          }}
        >
          MarketBridge
        </div>
        <nav style={{ display: "flex", alignItems: "center", gap: 28 }}>
          {links.map(({ to, label }) => (
            <NavLink
              key={to}
              to={to}
              style={({ isActive }) => ({
                fontWeight: 700,
                fontFamily: "'Inter', sans-serif",
                fontSize: "1rem",
                color: isActive ? "var(--accent2)" : "var(--text-color)",
                borderRadius: "9px",
                borderBottom: isActive
                  ? "3px solid var(--accent2)"
                  : "3px solid transparent",
                background: isActive
                  ? "rgba(6,182,212,0.10)"
                  : "transparent",
                boxShadow: isActive ? "0 0 3px var(--accent2)" : "none", // reduced glow on active nav link
                padding: "0 .56rem",
                transition: "all 0.2s"
              })}
              end={to === "/"}
            >
              {label}
            </NavLink>
          ))}
          <ThemeToggle />
        </nav>
      </div>
    </header>
  );
}
