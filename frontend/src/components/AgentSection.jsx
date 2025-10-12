import React, { useState, useEffect } from 'react';
import { useLocation } from 'react-router-dom';
import AgentCard from './AgentCard';
import AgentCollaborationTimeline from './AgentCollaborationTimeline';
import './AgentSection.css';

const AgentSection = () => {
  const location = useLocation();
  const [campaignResults, setCampaignResults] = useState(null);
  const [campaignQuery, setCampaignQuery] = useState('');
  const [campaignProduct, setCampaignProduct] = useState('');
  const [isProcessing, setIsProcessing] = useState(false);

  // Get campaign results from navigation state (when coming from CampaignForm)
  useEffect(() => {
    if (location.state?.results) {
      setCampaignResults(location.state.results);
      setCampaignQuery(location.state.query || '');
      setCampaignProduct(location.state.product || '');
      setIsProcessing(false);
    }
  }, [location.state]);

  const agents = [
    {
      id: 'creative',
      name: 'Creative Agent',
      role: 'Campaign Strategy',
      description: 'Generates innovative marketing campaigns with targeted discount strategies and customer segmentation.',
      capabilities: [
        'Campaign ideation and strategy',
        'Customer segmentation analysis',
        'Discount and promotion planning',
        'Creative content suggestions',
        'Market trend analysis'
      ],
      icon: '🎨',
      color: '#7c3aed',
      stats: {
        'Campaigns Created': '150+',
        'Success Rate': '94%',
        'Avg. ROI': '340%'
      },
      result: campaignResults?.Creative
    },
    {
      id: 'finance',
      name: 'Finance Agent',
      role: 'Budget Validation',
      description: 'Validates campaign budgets against available funds and ensures financial feasibility of marketing initiatives.',
      capabilities: [
        'Budget analysis and validation',
        'Cost-effectiveness evaluation',
        'Financial risk assessment',
        'ROI projections',
        'Spending optimization'
      ],
      icon: '💰',
      color: '#06b6d4',
      stats: {
        'Budget Approved': '$2.5M+',
        'Cost Savings': '23%',
        'Accuracy Rate': '99.8%'
      },
      result: campaignResults?.Finance
    },
    {
      id: 'inventory',
      name: 'Inventory Agent',
      role: 'Stock Management',
      description: 'Monitors product availability across regions and ensures campaigns align with inventory levels.',
      capabilities: [
        'Real-time inventory tracking',
        'Regional availability analysis',
        'Stock level optimization',
        'Demand forecasting',
        'Supply chain coordination'
      ],
      icon: '📦',
      color: '#10b981',
      stats: {
        'Products Tracked': '10,000+',
        'Regions Covered': '25',
        'Accuracy': '98.5%'
      },
      result: campaignResults?.Inventory
    }
  ];

  return (
    <div className="agents-page">
      {/* Hero Section */}
      <section className="agents-hero">
        <div className="container">
          <div className="hero-content">
            <h1 className="hero-title">
              {campaignResults ? 'Campaign Results Ready!' : 'Meet Your AI Marketing Team'}
            </h1>
            <p className="hero-subtitle">
              {campaignResults 
                ? `Campaign analysis completed for "${campaignQuery}" targeting "${campaignProduct}"` 
                : 'Three specialized agents working together to create, validate, and execute your marketing campaigns with precision and intelligence.'
              }
            </p>
          </div>
        </div>
      </section>

      {/* Campaign Results Section */}
      {campaignResults && (
        <section className="campaign-results-section">
          <div className="container">
            <div className="results-header">
              <h2>Campaign Analysis Results</h2>
              <div className="campaign-meta">
                <span className="meta-item">Query: <strong>{campaignQuery}</strong></span>
                <span className="meta-item">Product: <strong>{campaignProduct}</strong></span>
                <span className="meta-item">Status: <span className="status-success">✓ Complete</span></span>
              </div>
            </div>

            {/* Final Plan Card */}
            <div className="final-plan-card">
              <h3>🎯 Final Marketing Plan</h3>
              <p className="final-plan-text">{campaignResults['Final Plan']}</p>
            </div>
          </div>
        </section>
      )}

      {/* Agents Grid with Results */}
      <section className="agents-grid-section">
        <div className="container">
          <div className="section-header">
            <h2>{campaignResults ? 'Agent Analysis' : 'Agent Capabilities'}</h2>
            <p>{campaignResults ? 'See what each agent contributed to your campaign' : 'Each agent brings unique expertise to your marketing campaigns'}</p>
          </div>
          
          <div className="agents-grid">
            {agents.map((agent) => (
              <AgentCard 
                key={agent.id} 
                agent={agent} 
                hasResults={!!campaignResults}
                isProcessing={isProcessing}
              />
            ))}
          </div>
        </div>
      </section>

      {/* Collaboration Timeline - UPDATE THIS SECTION */}
<section className="collaboration-section">
  <div className="container">
    <div className="section-header">
      <h2>Agent Collaboration Workflow</h2>
      <p>See how our agents work together seamlessly</p>
    </div>
    <AgentCollaborationTimeline 
      campaignResults={campaignResults} 
      isProcessing={isProcessing}
    />
  </div>
</section>


      {/* Stats Overview */}
      {!campaignResults && (
        <section className="stats-section">
          <div className="container">
            <div className="stats-grid">
              <div className="stat-card">
                <h3>150+</h3>
                <p>Campaigns Created</p>
              </div>
              <div className="stat-card">
                <h3>$2.5M+</h3>
                <p>Budget Managed</p>
              </div>
              <div className="stat-card">
                <h3>10,000+</h3>
                <p>Products Tracked</p>
              </div>
              <div className="stat-card">
                <h3>98.5%</h3>
                <p>Average Accuracy</p>
              </div>
            </div>
          </div>
        </section>
      )}
    </div>
  );
};

export default AgentSection;
