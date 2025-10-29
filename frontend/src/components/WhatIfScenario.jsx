import React, { useState } from 'react';
import './WhatIfScenario.css';

function WhatIfScenario() {
  const [inputs, setInputs] = useState({
    discount: 20,
    duration: 30,
    target_size: 5000,
    budget: 50000,
    product: 'Wireless Bluetooth Headphones',
    include_agent_analysis: true
  });
  
  const [scenarios, setScenarios] = useState([]);
  const [loading, setLoading] = useState(false);
  const [executiveSummary, setExecutiveSummary] = useState('');
  const [analysisMeta, setAnalysisMeta] = useState(null);
  const [error, setError] = useState('');

  const handleChange = (e) => {
    const { name, type, checked, value } = e.target;
    setInputs(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : (type === 'number' ? Number(value) : value)
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setScenarios([]);
    setExecutiveSummary('');
    setAnalysisMeta(null);

    try {
      console.log('🎯 Sending What-If request:', inputs);
      
      const response = await fetch('http://127.0.0.1:8000/api/what_if', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(inputs),
      });

      const data = await response.json();
      console.log('📊 What-If response:', data);
      
      if (data.success) {
        setScenarios(data.scenarios || []);
        setExecutiveSummary(data.executive_summary || '');
        setAnalysisMeta(data.analysis_meta || null);
      } else {
        setError(data.error || 'Analysis failed');
      }
    } catch (err) {
      console.error('❌ What-If request failed:', err);
      setError('Failed to connect to analysis engine');
    } finally {
      setLoading(false);
    }
  };

  const getPerformanceColor = (tier) => {
    const colors = {
      'Exceptional': '#10b981',
      'High': '#3b82f6', 
      'Good': '#8b5cf6',
      'Moderate': '#f59e0b',
      'Low': '#ef4444'
    };
    return colors[tier] || '#6b7280';
  };

  const getRiskColor = (risk) => {
    const colors = {
      'Low': '#10b981',
      'Medium': '#f59e0b', 
      'High': '#ef4444'
    };
    return colors[risk] || '#6b7280';
  };

  return (
    <div className="whatif-container">
      <div className="whatif-header">
        <h1>🎯 AI-Powered What-If Analysis</h1>
        <p>Generate intelligent campaign scenarios with sentiment analysis and agent optimization</p>
      </div>

      <div className="whatif-content">
        <div className="input-section">
          <form onSubmit={handleSubmit} className="whatif-form">
            <div className="form-row">
              <div className="form-group">
                <label htmlFor="product">Product</label>
                <input
                  type="text"
                  id="product"
                  name="product"
                  value={inputs.product}
                  onChange={handleChange}
                  className="input-modern"
                  placeholder="Enter product name"
                />
              </div>
              
              <div className="form-group">
                <label htmlFor="discount">Discount (%)</label>
                <input
                  type="number"
                  id="discount"
                  name="discount"
                  value={inputs.discount}
                  onChange={handleChange}
                  className="input-modern"
                  min="0"
                  max="100"
                />
              </div>
            </div>

            <div className="form-row">
              <div className="form-group">
                <label htmlFor="budget">Budget ($)</label>
                <input
                  type="number"
                  id="budget"
                  name="budget"
                  value={inputs.budget}
                  onChange={handleChange}
                  className="input-modern"
                  min="1000"
                  step="1000"
                />
              </div>
              
              <div className="form-group">
                <label htmlFor="target_size">Target Size</label>
                <input
                  type="number"
                  id="target_size"
                  name="target_size"
                  value={inputs.target_size}
                  onChange={handleChange}
                  className="input-modern"
                  min="100"
                  step="100"
                />
              </div>
            </div>

            <div className="form-row">
              <div className="form-group">
                <label htmlFor="duration">Duration (days)</label>
                <input
                  type="number"
                  id="duration"
                  name="duration"
                  value={inputs.duration}
                  onChange={handleChange}
                  className="input-modern"
                  min="7"
                  max="365"
                />
              </div>
              
              <div className="form-group">
                <label className="checkbox-label">
                  <input
                    type="checkbox"
                    name="include_agent_analysis"
                    checked={inputs.include_agent_analysis}
                    onChange={handleChange}
                    className="checkbox-modern"
                  />
                  Enable AI Agent Analysis
                  <span className="tooltip">Uses your FinBERT sentiment analysis and 4-agent system</span>
                </label>
              </div>
            </div>

            <button 
              type="submit" 
              className="analyze-btn" 
              disabled={loading}
            >
              {loading ? '🧠 Analyzing...' : '🚀 Generate AI Scenarios'}
            </button>
          </form>
        </div>

        {error && (
          <div className="error-message">
            <h3>⚠️ Analysis Error</h3>
            <p>{error}</p>
          </div>
        )}

        {executiveSummary && (
          <div className="executive-summary">
            <h3>📋 Executive Summary</h3>
            <p>{executiveSummary}</p>
            {analysisMeta?.ai_enhanced && (
              <div className="ai-badge">🧠 AI-Enhanced Analysis</div>
            )}
          </div>
        )}

        {scenarios.length > 0 && (
          <div className="scenarios-section">
            <div className="section-header">
              <h2>📊 Scenario Analysis Results</h2>
              <p>{scenarios.length} scenarios generated • Best ROI: {Math.max(...scenarios.map(s => s.roi))}%</p>
            </div>
            
            <div className="scenarios-grid">
              {scenarios.map((scenario) => (
                <div 
                  key={scenario.id} 
                  className={`scenario-card ${scenario.recommended ? 'recommended' : ''}`}
                >
                  <div className="scenario-header">
                    <h3>{scenario.name}</h3>
                    <div className="badges">
                      <span 
                        className="performance-badge"
                        style={{ backgroundColor: getPerformanceColor(scenario.performance_tier) }}
                      >
                        {scenario.performance_tier}
                      </span>
                      <span 
                        className="risk-badge"
                        style={{ backgroundColor: getRiskColor(scenario.risk_level) }}
                      >
                        {scenario.risk_level} Risk
                      </span>
                      {scenario.recommended && (
                        <span className="recommended-badge">⭐ Recommended</span>
                      )}
                    </div>
                  </div>

                  <p className="scenario-description">{scenario.description}</p>

                  <div className="metrics-grid">
                    <div className="metric">
                      <span className="metric-label">ROI</span>
                      <span className="metric-value roi">{scenario.roi}%</span>
                    </div>
                    <div className="metric">
                      <span className="metric-label">Probability</span>
                      <span className="metric-value">{scenario.probability}</span>
                    </div>
                    <div className="metric">
                      <span className="metric-label">Revenue</span>
                      <span className="metric-value">${scenario.expected_revenue?.toLocaleString()}</span>
                    </div>
                    <div className="metric">
                      <span className="metric-label">Conversions</span>
                      <span className="metric-value">{scenario.expected_conversions}</span>
                    </div>
                  </div>

                  {scenario.ai_insights && scenario.ai_insights.length > 0 && (
                    <div className="ai-insights">
                      <h4>🧠 AI Insights</h4>
                      <ul>
                        {scenario.ai_insights.map((insight, idx) => (
                          <li key={idx}>{insight}</li>
                        ))}
                      </ul>
                    </div>
                  )}

                  {scenario.enhancements && (
                    <div className="enhancements">
                      <h4>⚡ AI Enhancements</h4>
                      <div className="enhancement-tags">
                        {scenario.enhancements.sentiment_enhanced && 
                          <span className="enhancement-tag">💰 Sentiment Boosted</span>
                        }
                        {scenario.enhancements.creative_optimized && 
                          <span className="enhancement-tag">🎨 Creative Optimized</span>
                        }
                        {scenario.enhancements.finance_validated && 
                          <span className="enhancement-tag">💰 Finance Validated</span>
                        }
                        {scenario.enhancements.historically_informed && 
                          <span className="enhancement-tag">📊 Historically Informed</span>
                        }
                      </div>
                    </div>
                  )}

                  <div className="scenario-footer">
                    <span className="confidence">
                      AI Confidence: {(scenario.ai_confidence * 100).toFixed(0)}%
                    </span>
                    <span className="complexity">
                      Complexity: {scenario.execution_complexity}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {analysisMeta && (
          <div className="analysis-meta">
            <h3>📈 Analysis Metadata</h3>
            <div className="meta-grid">
              <div className="meta-item">
                <span>Engine:</span>
                <span>{analysisMeta.engine}</span>
              </div>
              <div className="meta-item">
                <span>Average ROI:</span>
                <span>{analysisMeta.average_roi}%</span>
              </div>
              <div className="meta-item">
                <span>Recommended:</span>
                <span>{analysisMeta.recommended_scenarios}/{analysisMeta.total_scenarios}</span>
              </div>
              <div className="meta-item">
                <span>AI Enhanced:</span>
                <span>{analysisMeta.ai_enhanced ? '✅ Yes' : '❌ No'}</span>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default WhatIfScenario;
