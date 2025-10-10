import React from "react";

export default function Header() {
  return (
    <header className="topbar">
      <div className="brand">
        <div className="logo">🤖</div>
        <div>
          <div className="brand-title">AIMarketer</div>
          <div className="brand-sub">Autonomous Multi-Agent Campaign Planner</div>
        </div>
      </div>
      <nav className="nav">
        <button className="ghost">Demo</button>
        <button className="ghost">Docs</button>
      </nav>
    </header>
  );
}
