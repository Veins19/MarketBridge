-- Add RAG-related columns to campaign_results table
ALTER TABLE campaign_results 
ADD COLUMN IF NOT EXISTS rag_enhanced BOOLEAN DEFAULT FALSE;

ALTER TABLE campaign_results 
ADD COLUMN IF NOT EXISTS historical_campaigns_used INTEGER DEFAULT 0;

-- Add product_id column if missing
ALTER TABLE products 
ADD COLUMN IF NOT EXISTS product_id VARCHAR(50);

-- Update existing products with product_id if null
UPDATE products 
SET product_id = 'PROD_' || id 
WHERE product_id IS NULL;

-- Add index for better performance
CREATE INDEX IF NOT EXISTS idx_campaign_results_rag_enhanced 
ON campaign_results(rag_enhanced);

-- Confirmation
SELECT 'RAG columns added successfully' as status;
