
import React from "react";
import Hero from "./components/Hero.jsx";
import AgentSection from "./components/AgentSection.jsx";
import Footer from "./components/Footer.jsx";
import CampaignForm from "./components/CampaignForm.jsx";
import { Routes, Route } from "react-router-dom";

export default function App() {
  return (
    <div className="app">
      <Routes>
        <Route path="/" element={<Hero />} />
        <Route path="/campaign" element={<CampaignForm />} />
        <Route path="/agents" element={<AgentSection />} />
      </Routes>
      <Footer />
    </div>
  );
}
