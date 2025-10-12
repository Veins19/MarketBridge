import React from "react";
import Hero from "./components/Hero.jsx";
import AgentSection from "./components/AgentSection.jsx";
import Footer from "./components/Footer.jsx";
import CampaignForm from "./components/CampaignForm.jsx";
import Header from "./components/Header.jsx";
import { Routes, Route } from "react-router-dom";

export default function App() {
  return (
    <div className="app" style={{ display: "flex", flexDirection: "column", minHeight: "100vh" }}>
      <Header />
      <div style={{ flex: 1 }}>
        <Routes>
          <Route path="/" element={<Hero />} />
          <Route path="/campaign" element={<CampaignForm />} />
          <Route path="/agents" element={<AgentSection />} />
        </Routes>
      </div>
      <Footer />
    </div>
  );
}
