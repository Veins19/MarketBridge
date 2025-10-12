import React, { useState } from 'react';

const AgentCard = ({ agent, hasResults, isProcessing }) => {
  const [isExpanded, setIsExpanded] = useState(false);

  return (
    <div className={`agent-card ${hasResults ? 'has-results' : ''}`} style={{ '--agent-color': agent.color }}>
      <div className="agent-header">
        <div className="agent-icon">{agent.icon}</div>
        <div className="agent-info">
          <h3 className="agent-name">{agent.name}</h3>
          <p className="agent-role">{agent.role}</p>
        </div>
        <div className="agent-status">
          <span className={`status-dot ${hasResults ? 'complete' : 'active'}`}></span>
          <span className="status-text">
            {isProcessing ? 'Processing...' : hasResults ? 'Complete' : 'Active'}
          </span>
        </div>
      </div>

      <p className="agent-description">{agent.description}</p>

      {/* Campaign Result Display */}
      {hasResults && agent.result && (
        <div className="campaign-result">
          <h4>🎯 Campaign Analysis</h4>
          <div className="result-content">
            <p>{agent.result}</p>
          </div>
        </div>
      )}

      {/* Show processing state */}
      {isProcessing && (
        <div className="processing-state">
          <div className="processing-spinner"></div>
          <p>Agent is analyzing your campaign...</p>
        </div>
      )}

      <div className="agent-stats">
        {Object.entries(agent.stats).map(([key, value]) => (
          <div key={key} className="stat-item">
            <span className="stat-value">{value}</span>
            <span className="stat-label">{key}</span>
          </div>
        ))}
      </div>

      <div className={`agent-capabilities ${isExpanded ? 'expanded' : ''}`}>
        <h4>Key Capabilities</h4>
        <ul className="capabilities-list">
          {agent.capabilities.slice(0, isExpanded ? agent.capabilities.length : 3).map((capability, index) => (
            <li key={index} className="capability-item">
              <span className="capability-icon">✓</span>
              {capability}
            </li>
          ))}
        </ul>
        
        {agent.capabilities.length > 3 && (
          <button 
            className="expand-btn"
            onClick={() => setIsExpanded(!isExpanded)}
          >
            {isExpanded ? 'Show Less' : `+${agent.capabilities.length - 3} More`}
          </button>
        )}
      </div>

      <div className="agent-actions">
        <button className="action-btn primary">View Details</button>
        <button className="action-btn secondary">Configure</button>
      </div>
    </div>
  );
};

export default AgentCard;
