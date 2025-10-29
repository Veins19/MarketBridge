"""
Simplified MarketBridge API for testing basic functionality.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
import os
from pathlib import Path

app = FastAPI(
    title="MarketBridge API - Simple",
    description="Basic version for testing",
    version="2.0.0-test"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],
)

# Test database connectivity
def test_database():
    """Test if our database exists and is accessible"""
    try:
        db_path = Path(__file__).parent / "marketbridge.db"
        if not db_path.exists():
            return {"status": "error", "message": "Database file not found"}
        
        import sqlite3
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()
        
        # Test query
        cursor.execute("SELECT COUNT(*) FROM customers")
        customer_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM products")  
        product_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM campaigns")
        campaign_count = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            "status": "success",
            "customers": customer_count,
            "products": product_count,
            "campaigns": campaign_count
        }
        
    except Exception as e:
        return {"status": "error", "message": str(e)}

# Basic request models
class LegacyCampaignRequest(BaseModel):
    query: str
    product: str

@app.get("/")
async def root():
    """Root endpoint"""
    db_status = test_database()
    return {
        "message": "MarketBridge API - Simple Test Version",
        "status": "running",
        "database": db_status,
        "endpoints": ["/", "/health", "/test-db", "/run_campaign"]
    }

@app.get("/health")
async def health():
    """Health check"""
    db_status = test_database()
    return {
        "api": "healthy",
        "database": db_status,
        "timestamp": "2025-10-28T18:58:00"
    }

@app.get("/test-db")
async def test_db():
    """Test database connectivity"""
    return test_database()

@app.post("/run_campaign") 
async def run_campaign(request: LegacyCampaignRequest):
    """Basic campaign endpoint for testing"""
    try:
        # Test database access
        db_status = test_database()
        
        if db_status["status"] == "error":
            raise HTTPException(status_code=500, detail=f"Database error: {db_status['message']}")
        
        # Simple response
        return {
            "Creative": f"Creative Agent: Campaign idea for {request.product} - {request.query}",
            "Finance": "Finance Agent: Budget analysis shows positive ROI potential",
            "Inventory": f"Inventory Agent: Stock levels checked for {request.product}",
            "Final Plan": f"Campaign: {request.query[:50]}... | Product: {request.product} | Status: Ready for execution",
            "Database": f"Connected - {db_status['customers']} customers, {db_status['products']} products"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    print("🧪 Starting Simple MarketBridge API for testing...")
    uvicorn.run(app, host="0.0.0.0", port=8000)
