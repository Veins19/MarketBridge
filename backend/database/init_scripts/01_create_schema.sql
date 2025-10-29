-- MarketBridge PostgreSQL Schema
-- Enterprise-grade database design for AI-powered marketing campaigns

-- Enable extensions for advanced features
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm"; -- For fuzzy text search

-- ============================================================================
-- CORE ENTITIES
-- ============================================================================

-- Companies/Organizations
CREATE TABLE companies (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    industry VARCHAR(100),
    size_category VARCHAR(50), -- 'startup', 'sme', 'enterprise'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Products catalog
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    company_id INTEGER REFERENCES companies(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    category VARCHAR(100) NOT NULL,
    base_price DECIMAL(12,2) NOT NULL,
    cost_price DECIMAL(12,2) NOT NULL,
    stock_quantity INTEGER DEFAULT 0,
    reorder_level INTEGER DEFAULT 10,
    is_active BOOLEAN DEFAULT true,
    
    -- Regional stock distribution (JSONB for flexibility)
    stock_regions JSONB DEFAULT '{}',
    
    -- Product metadata
    attributes JSONB DEFAULT '{}', -- size, color, specs, etc.
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Constraints
    CONSTRAINT positive_prices CHECK (base_price > 0 AND cost_price > 0),
    CONSTRAINT positive_stock CHECK (stock_quantity >= 0)
);

-- Customer segments and profiles
CREATE TABLE customers (
    id SERIAL PRIMARY KEY,
    company_id INTEGER REFERENCES companies(id) ON DELETE CASCADE,
    customer_id VARCHAR(100) NOT NULL, -- External customer ID
    name VARCHAR(255),
    email VARCHAR(255),
    segment VARCHAR(50) NOT NULL, -- 'high_value', 'regular', 'new', 'at_risk'
    
    -- Customer value metrics
    lifetime_value DECIMAL(12,2) DEFAULT 0,
    total_orders INTEGER DEFAULT 0,
    last_purchase_date DATE,
    acquisition_date DATE,
    
    -- Preferences and behavior
    preferred_channels JSONB DEFAULT '[]', -- ['email', 'social', 'sms']
    purchase_history JSONB DEFAULT '[]',
    behavioral_data JSONB DEFAULT '{}',
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    UNIQUE(company_id, customer_id)
);

-- ============================================================================
-- CAMPAIGN MANAGEMENT
-- ============================================================================

-- Marketing campaigns
CREATE TABLE campaigns (
    id SERIAL PRIMARY KEY,
    company_id INTEGER REFERENCES companies(id) ON DELETE CASCADE,
    campaign_id VARCHAR(100) NOT NULL,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    
    -- Campaign configuration
    campaign_type VARCHAR(50) NOT NULL, -- 'product_launch', 'seasonal_sale', 'retention'
    product_id INTEGER REFERENCES products(id),
    status VARCHAR(50) DEFAULT 'draft', -- 'draft', 'active', 'paused', 'completed'
    
    -- Target parameters
    target_audience_size INTEGER,
    target_segments JSONB DEFAULT '[]',
    target_channels JSONB DEFAULT '[]',
    target_regions JSONB DEFAULT '[]',
    
    -- Budget and timing
    budget DECIMAL(12,2),
    discount_rate DECIMAL(5,2) DEFAULT 0,
    duration_days INTEGER,
    start_date DATE,
    end_date DATE,
    
    -- Campaign metadata
    created_by VARCHAR(100),
    campaign_data JSONB DEFAULT '{}',
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    UNIQUE(company_id, campaign_id)
);

-- ============================================================================
-- MULTI-AGENT SYSTEM TABLES
-- ============================================================================

-- Agent analysis results
CREATE TABLE agent_analyses (
    id SERIAL PRIMARY KEY,
    campaign_id INTEGER REFERENCES campaigns(id) ON DELETE CASCADE,
    agent_type VARCHAR(50) NOT NULL, -- 'creative', 'finance', 'inventory', 'lead'
    analysis_id VARCHAR(100) NOT NULL,
    
    -- Agent response data
    agent_response JSONB NOT NULL,
    reasoning TEXT,
    confidence_level DECIMAL(3,2) DEFAULT 0.5,
    
    -- Analysis metadata
    analysis_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    processing_time_ms INTEGER,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Agent collaboration log
CREATE TABLE agent_collaborations (
    id SERIAL PRIMARY KEY,
    campaign_id INTEGER REFERENCES campaigns(id) ON DELETE CASCADE,
    session_id VARCHAR(100) NOT NULL,
    
    -- Collaboration details
    negotiation_round INTEGER DEFAULT 1,
    participating_agents JSONB NOT NULL, -- ['creative', 'finance', 'inventory']
    
    -- Interaction data
    interaction_type VARCHAR(50) NOT NULL, -- 'proposal', 'negotiation', 'synthesis'
    agent_interactions JSONB NOT NULL,
    consensus_reached BOOLEAN DEFAULT false,
    
    -- Results
    final_recommendation VARCHAR(50), -- 'approved', 'rejected', 'modified'
    collaboration_summary TEXT,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Campaign performance results
CREATE TABLE campaign_results (
    id SERIAL PRIMARY KEY,
    campaign_id INTEGER REFERENCES campaigns(id) ON DELETE CASCADE,
    
    -- Financial metrics
    projected_roi DECIMAL(8,2),
    projected_revenue DECIMAL(12,2),
    projected_profit DECIMAL(12,2),
    projected_customers INTEGER,
    
    -- Risk and success metrics
    risk_score DECIMAL(3,2),
    success_probability DECIMAL(3,2),
    
    -- Agent-specific outputs
    creative_output JSONB,
    finance_output JSONB,
    inventory_output JSONB,
    lead_agent_output JSONB,
    
    -- Performance tracking
    final_recommendation JSONB,
    negotiation_rounds INTEGER DEFAULT 1,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- What-if scenarios
CREATE TABLE scenarios (
    id SERIAL PRIMARY KEY,
    campaign_id INTEGER REFERENCES campaigns(id) ON DELETE CASCADE,
    scenario_name VARCHAR(255) NOT NULL,
    scenario_type VARCHAR(50) NOT NULL, -- 'conservative', 'balanced', 'aggressive'
    
    -- Input parameters
    input_parameters JSONB NOT NULL,
    
    -- Scenario results
    projected_roi DECIMAL(8,2),
    projected_revenue DECIMAL(12,2),
    success_probability DECIMAL(3,2),
    risk_assessment VARCHAR(50),
    
    -- Recommendations
    recommended_channels JSONB,
    targeting_strategy TEXT,
    budget_allocation JSONB,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================================
-- INDEXES FOR PERFORMANCE
-- ============================================================================

-- Primary lookup indexes
CREATE INDEX idx_products_company_id ON products(company_id);
CREATE INDEX idx_products_category ON products(category);
CREATE INDEX idx_products_active ON products(is_active) WHERE is_active = true;

CREATE INDEX idx_customers_company_id ON customers(company_id);
CREATE INDEX idx_customers_segment ON customers(segment);
CREATE INDEX idx_customers_ltv ON customers(lifetime_value DESC);

CREATE INDEX idx_campaigns_company_id ON campaigns(company_id);
CREATE INDEX idx_campaigns_status ON campaigns(status);
CREATE INDEX idx_campaigns_type ON campaigns(campaign_type);
CREATE INDEX idx_campaigns_dates ON campaigns(start_date, end_date);

-- Agent system indexes
CREATE INDEX idx_agent_analyses_campaign_id ON agent_analyses(campaign_id);
CREATE INDEX idx_agent_analyses_type ON agent_analyses(agent_type);
CREATE INDEX idx_agent_collaborations_campaign_id ON agent_collaborations(campaign_id);
CREATE INDEX idx_agent_collaborations_session ON agent_collaborations(session_id);

CREATE INDEX idx_campaign_results_campaign_id ON campaign_results(campaign_id);
CREATE INDEX idx_scenarios_campaign_id ON scenarios(campaign_id);

-- Full-text search indexes
CREATE INDEX idx_products_search ON products USING gin(to_tsvector('english', name || ' ' || coalesce(description, '')));
CREATE INDEX idx_campaigns_search ON campaigns USING gin(to_tsvector('english', name || ' ' || coalesce(description, '')));

-- ============================================================================
-- TRIGGERS FOR AUTO-UPDATES
-- ============================================================================

-- Auto-update updated_at timestamps
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_companies_updated_at BEFORE UPDATE ON companies FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_products_updated_at BEFORE UPDATE ON products FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_customers_updated_at BEFORE UPDATE ON customers FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_campaigns_updated_at BEFORE UPDATE ON campaigns FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- ============================================================================
-- COMMENTS FOR DOCUMENTATION
-- ============================================================================

COMMENT ON TABLE companies IS 'Organizations using MarketBridge for campaign planning';
COMMENT ON TABLE products IS 'Product catalog with inventory and pricing data';
COMMENT ON TABLE customers IS 'Customer profiles with segmentation and behavioral data';
COMMENT ON TABLE campaigns IS 'Marketing campaigns with multi-agent analysis';
COMMENT ON TABLE agent_analyses IS 'Individual agent analysis results (Creative, Finance, Inventory, Lead)';
COMMENT ON TABLE agent_collaborations IS 'Multi-agent collaboration sessions with negotiation logs';
COMMENT ON TABLE campaign_results IS 'Final campaign recommendations from multi-agent system';
COMMENT ON TABLE scenarios IS 'What-if scenario analysis results';

COMMENT ON COLUMN products.stock_regions IS 'JSON object with regional stock distribution: {"north": 50, "south": 30}';
COMMENT ON COLUMN customers.preferred_channels IS 'JSON array of preferred marketing channels: ["email", "social"]';
COMMENT ON COLUMN campaigns.target_segments IS 'JSON array of customer segments to target: ["high_value", "regular"]';
COMMENT ON COLUMN agent_analyses.agent_response IS 'Complete JSON response from agent analysis';
COMMENT ON COLUMN agent_collaborations.agent_interactions IS 'Detailed log of agent-to-agent communications';
