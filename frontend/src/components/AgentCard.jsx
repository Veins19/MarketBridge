import React, { useState } from 'react';
import './AgentCard.css';

const AgentCard = ({ agent, hasResults, isProcessing }) => {
  const formatResultForDisplay = (result) => {
    if (!result) return null;

    // Handle structured output with sections
    if (result.includes('**') && result.includes('📊') || result.includes('🎨') || result.includes('💰') || result.includes('📦')) {
      return formatStructuredOutput(result);
    }

    // Original formatting for simple text
    const sections = result.split('\n\n');
    return sections.map((section, index) => {
      const lines = section.split('\n');
      const header = lines[0];
      const content = lines.slice(1);
      
      const isHeader = header.match(/[🎨💰📦✅⚠️❌]/) || 
                      header.includes('BREAKDOWN') || 
                      header.includes('ANALYSIS') || 
                      header.includes('METRICS');

      if (isHeader) {
        return (
          <div key={index} className="result-section">
            <div className="result-header">{header}</div>
            {content.length > 0 && (
              <div className="result-content">
                {content.map((line, lineIndex) => (
                  <div key={lineIndex} className="result-line">{line}</div>
                ))}
              </div>
            )}
          </div>
        );
      }

      return (
        <div key={index} className="result-paragraph">
          {section}
        </div>
      );
    });
  };

  // ADD: New function to format structured output
  const formatStructuredOutput = (result) => {
    const sections = result.split('\n\n');
    return sections.map((section, index) => {
      const lines = section.split('\n');
      
      // Check if this is a main heading (has ** and emoji)
      if (lines[0].includes('**') && lines[0].match(/[🎨💰📦📊🎯📈⚠️✅📋]/)) {
        const title = lines[0].replace(/\*\*/g, '').trim();
        const content = lines.slice(1);
        
        return (
          <div key={index} className="structured-section">
            <div className="structured-title">{title}</div>
            <div className="structured-content">
              {content.map((line, lineIndex) => {
                if (line.startsWith('•')) {
                  return <div key={lineIndex} className="bullet-point">{line}</div>;
                }
                if (line.match(/^\d+\./)) {
                  return <div key={lineIndex} className="numbered-item">{line}</div>;
                }
                return <div key={lineIndex} className="content-line">{line}</div>;
              })}
            </div>
          </div>
        );
      }
      
      return (
        <div key={index} className="result-paragraph">
          {section}
        </div>
      );
    });
  };

  const [isExpanded, setIsExpanded] = useState(false);

  const toggleExpand = () => {
    setIsExpanded(!isExpanded);
  };

  return (
    <div className={`agent-card ${hasResults ? 'has-results' : ''} ${isProcessing ? 'processing' : ''}`}>
      <div className="agent-header">
        <div className="agent-icon">
          <span className="agent-emoji">{agent.icon}</span>
        </div>
        <div className="agent-info">
          <h3 className="agent-name">{agent.name}</h3>
          <p className="agent-role">{agent.role}</p>
          <p className="agent-description">{agent.description}</p>
        </div>
        <div className="agent-status">
          {isProcessing && <div className="processing-indicator">Processing...</div>}
          {hasResults && (
            <button 
              className="expand-button"
              onClick={toggleExpand}
              aria-label={isExpanded ? 'Collapse' : 'Expand'}
            >
              {isExpanded ? '−' : '+'}
            </button>
          )}
        </div>
      </div>
      
      {hasResults && (
        <div className={`agent-results ${isExpanded ? 'expanded' : 'collapsed'}`}>
          <div className="agent-output">
            {formatResultForDisplay(agent.result)}
          </div>
        </div>
      )}
    </div>
  );
};

export default AgentCard;
