import React from 'react';

const AgentCollaborationTimeline = ({ campaignResults, isProcessing = false }) => {
  const timelineSteps = [
    {
      id: 'creative',
      name: 'Creative Agent',
      icon: '🎨',
      color: '#7c3aed',
      description: 'Analyzing campaign strategy and creative approach...',
      result: campaignResults?.Creative,
      status: campaignResults?.Creative ? 'completed' : (isProcessing ? 'processing' : 'pending')
    },
    {
      id: 'finance',
      name: 'Finance Agent',
      icon: '💰',
      color: '#06b6d4',
      description: 'Validating budget and financial feasibility...',
      result: campaignResults?.Finance,
      status: campaignResults?.Finance ? 'completed' : (isProcessing ? 'processing' : 'pending')
    },
    {
      id: 'inventory',
      name: 'Inventory Agent',
      icon: '📦',
      color: '#10b981',
      description: 'Checking product availability and stock levels...',
      result: campaignResults?.Inventory,
      status: campaignResults?.Inventory ? 'completed' : (isProcessing ? 'processing' : 'pending')
    },
    {
      id: 'negotiation',
      name: 'Agent Negotiation',
      icon: '🤝',
      color: '#f59e0b',
      description: 'Agents collaborating to finalize campaign details...',
      result: campaignResults ? 'Agents successfully collaborated and reached consensus' : null,
      status: campaignResults ? 'completed' : (isProcessing ? 'processing' : 'pending')
    },
    {
      id: 'final',
      name: 'Final Campaign Plan',
      icon: '🎯',
      color: '#10b981',
      description: 'Generating comprehensive campaign strategy...',
      result: campaignResults?.['Final Plan'],
      status: campaignResults?.['Final Plan'] ? 'completed' : (isProcessing ? 'processing' : 'pending')
    }
  ];

  const getStatusIcon = (status) => {
    switch (status) {
      case 'completed':
        return '✅';
      case 'processing':
        return '⏳';
      default:
        return '⏸️';
    }
  };

  const getStatusText = (status) => {
    switch (status) {
      case 'completed':
        return 'Completed';
      case 'processing':
        return 'Processing...';
      default:
        return 'Waiting';
    }
  };

  return (
    <div className="timeline-container">
      <h2 className="timeline-title">Agent Collaboration Timeline</h2>
      
      <div className="timeline">
        {timelineSteps.map((step, index) => (
          <div key={step.id} className={`timeline-step ${step.status}`}>
            <div className="timeline-marker">
              <div 
                className="timeline-icon"
                style={{ 
                  backgroundColor: step.status === 'completed' ? step.color : 'transparent',
                  border: `2px solid ${step.color}`
                }}
              >
                {step.status === 'completed' ? '✓' : step.icon}
              </div>
              {index < timelineSteps.length - 1 && (
                <div 
                  className={`timeline-line ${step.status === 'completed' ? 'completed' : ''}`}
                  style={{ '--line-color': step.color }}
                />
              )}
            </div>
            
            <div className="timeline-content">
              <div className="timeline-header">
                <h3 className="timeline-step-name">{step.name}</h3>
                <div className="timeline-status">
                  <span className="status-icon">{getStatusIcon(step.status)}</span>
                  <span className="status-text">{getStatusText(step.status)}</span>
                </div>
              </div>
              
              <p className="timeline-description">{step.description}</p>
              
              {step.result && (
                <div className="timeline-result">
                  <strong>Result:</strong> {step.result}
                </div>
              )}
              
              {!step.result && step.status === 'pending' && (
                <div className="timeline-waiting">
                  <em>Waiting for previous steps to complete...</em>
                </div>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default AgentCollaborationTimeline;
