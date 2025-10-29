import React from 'react';
import './CampaignExecutionPlan.css';

const CampaignExecutionPlan = ({ campaignResults }) => {
  const planData = campaignResults?.['Final Plan'];
  
  if (!planData) return null;

  // Clean and format the plan text for better readability
  const cleanPlanText = (text) => {
    if (!text) return '';
    
    // Remove excessive formatting and make it more readable
    return text
      .replace(/\*\*/g, '') // Remove bold markdown
      .replace(/\n{3,}/g, '\n\n') // Reduce multiple line breaks
      .replace(/^\s+|\s+$/g, '') // Trim whitespace
      .split('\n')
      .map(line => line.trim())
      .filter(line => line.length > 0)
      .join('\n');
  };

  const formattedPlan = cleanPlanText(planData);

  return (
    <div className="campaign-execution-plan">
      <div className="plan-header">
        <div className="plan-title-container">
          <span className="plan-icon">🎯</span>
          <h2 className="plan-title">Campaign Execution Plan</h2>
        </div>
        <div className="plan-status">
          <div className="status-indicator ready"></div>
          <span className="status-text">Ready to Launch</span>
        </div>
      </div>
      
      <div className="plan-content-wrapper">
        <div className="plan-content">
          <div className="plan-text">
            {formattedPlan.split('\n').map((line, index) => {
              // Check if line is a header/section title
              if (line.includes('🎨') || line.includes('💰') || line.includes('📦') || 
                  line.includes('✅') || line.includes('📊') || line.includes('🎯') ||
                  line.includes('CAMPAIGN') || line.includes('STRATEGY') || 
                  line.includes('BUDGET') || line.includes('ANALYSIS')) {
                return (
                  <div key={index} className="plan-section-title">
                    {line}
                  </div>
                );
              }
              
              // Check if line is a bullet point
              if (line.startsWith('•') || line.startsWith('-') || line.startsWith('*')) {
                return (
                  <div key={index} className="plan-bullet-point">
                    <span className="bullet">•</span>
                    <span className="bullet-content">{line.replace(/^[•\-*]\s*/, '')}</span>
                  </div>
                );
              }
              
              // Check if line contains metrics (has numbers/percentages)
              if (line.match(/\d+%|\$[\d,]+|\d+\.\d+/) && line.includes(':')) {
                const [label, value] = line.split(':');
                return (
                  <div key={index} className="plan-metric">
                    <span className="metric-label">{label.trim()}:</span>
                    <span className="metric-value">{value?.trim()}</span>
                  </div>
                );
              }
              
              // Regular paragraph text
              if (line.trim()) {
                return (
                  <div key={index} className="plan-paragraph">
                    {line}
                  </div>
                );
              }
              
              return null;
            })}
          </div>
          
          {/* Campaign Summary Box */}
          <div className="campaign-summary-box">
            <h4>📈 Campaign Overview</h4>
            <div className="summary-items">
              <div className="summary-item">
                <span className="summary-label">Platform:</span>
                <span className="summary-value">MarketBridge AI</span>
              </div>
              <div className="summary-item">
                <span className="summary-label">Strategy:</span>
                <span className="summary-value">AI-Powered Marketing</span>
              </div>
              <div className="summary-item">
                <span className="summary-label">Status:</span>
                <span className="summary-value success">Validated & Ready</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default CampaignExecutionPlan;
