-- Add sentiment analysis columns to campaign_results table
ALTER TABLE campaign_results 
ADD COLUMN IF NOT EXISTS sentiment_enhanced BOOLEAN DEFAULT FALSE;

ALTER TABLE campaign_results 
ADD COLUMN IF NOT EXISTS sentiment_score DECIMAL(5,3) DEFAULT 0.000;

-- Add index for better performance
CREATE INDEX IF NOT EXISTS idx_campaign_results_sentiment_enhanced 
ON campaign_results(sentiment_enhanced);

-- Confirmation
SELECT 'Sentiment analysis columns added successfully' as status;
