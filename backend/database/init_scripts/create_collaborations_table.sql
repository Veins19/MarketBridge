-- Create collaborations table for multi-agent session tracking
CREATE TABLE IF NOT EXISTS collaborations (
    id SERIAL PRIMARY KEY,
    collaboration_id VARCHAR(50) UNIQUE NOT NULL,
    campaign_id VARCHAR(50),
    query TEXT NOT NULL,
    product VARCHAR(255),
    collaboration_mode VARCHAR(50) DEFAULT 'standard',
    agents_involved TEXT[], -- Array of agent names
    total_rounds INTEGER DEFAULT 1,
    total_interactions INTEGER DEFAULT 0,
    consensus_reached BOOLEAN DEFAULT FALSE,
    authority_structure VARCHAR(100),
    start_time TIMESTAMP DEFAULT NOW(),
    end_time TIMESTAMP,
    duration_seconds INTEGER,
    final_decision VARCHAR(50),
    success_probability DECIMAL(5,3),
    collaboration_metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Add indexes for performance
CREATE INDEX IF NOT EXISTS idx_collaborations_collaboration_id ON collaborations(collaboration_id);
CREATE INDEX IF NOT EXISTS idx_collaborations_campaign_id ON collaborations(campaign_id);
CREATE INDEX IF NOT EXISTS idx_collaborations_created_at ON collaborations(created_at);

-- Add trigger for updated_at
CREATE OR REPLACE FUNCTION update_collaborations_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_collaborations_updated_at
    BEFORE UPDATE ON collaborations
    FOR EACH ROW
    EXECUTE FUNCTION update_collaborations_updated_at();

-- Confirmation
SELECT 'Collaborations table created successfully' as status;
