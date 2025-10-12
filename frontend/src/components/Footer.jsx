import React from "react";

const socialLinks = [
  { href: "https://github.com/", label: "GitHub", icon: "🐙" },
  { href: "https://linkedin.com/", label: "LinkedIn", icon: "🔗" },
  { href: "https://twitter.com/", label: "Twitter", icon: "🐦" }
];

export default function Footer() {
  return (
    <footer
      style={{
        backdropFilter: "blur(16px)",
        background: "var(--header-bg)",
        borderTop: "1.5px solid var(--accent1)",
        boxShadow: "var(--shadow-glow)",
        padding: "1.5rem 2rem",
        color: "var(--text-color)",
        fontFamily: "'Inter', sans-serif",
        fontSize: "0.9rem",
        display: "flex",
        justifyContent: "space-between",
        alignItems: "center",
        flexWrap: "wrap",
        userSelect: "none"
      }}
    >
      <p style={{ margin: 0, flex: "1 1 300px" }}>
        © 2025 MarketBridge. All rights reserved.
      </p>
      <nav
        style={{
          display: "flex",
          gap: "1.6rem",
          flex: "1 1 200px",
          justifyContent: "flex-end"
        }}
      >
        {socialLinks.map(({ href, label, icon }) => (
          <a
            key={label}
            href={href}
            target="_blank"
            rel="noopener noreferrer"
            aria-label={label}
            style={{
              fontSize: "1.3rem",
              textDecoration: "none",
              color: "var(--accent1)",
              transition: "all 0.25s ease",
              cursor: "pointer",
              userSelect: "none",
              display: "inline-flex",
              alignItems: "center",
              justifyContent: "center",
              filter: "drop-shadow(0 0 2px var(--accent1))"
            }}
            onMouseEnter={e => e.currentTarget.style.color = "var(--accent2)"}
            onMouseLeave={e => e.currentTarget.style.color = "var(--accent1)"}
          >
            <span role="img" aria-hidden="true" style={{ marginRight: 6 }}>{icon}</span>
            {label}
          </a>
        ))}
      </nav>
    </footer>
  );
}
