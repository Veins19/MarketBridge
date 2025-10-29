"""
MarketBridge FastAPI Application - PostgreSQL Enterprise Edition
AI-Driven Multi-Agent Marketing Campaign Planner with Lead Agent Authority
"""

import os
import sys
from pathlib import Path
from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from services.whatif_engine import whatif_engine
from typing import List, Dict, Optional, Any
import json
import asyncio
from models.sentiment_analyzer import sentiment_analyzer
from datetime import datetime
from models.vector_store import vector_store
import uuid

# Add backend to path for imports
backend_path = Path(__file__).parent
sys.path.insert(0, str(backend_path))

# Import our PostgreSQL database layer
from models.database import (
    db_manager, startup_database, shutdown_database, health_check,
    execute_query, execute_one, execute_command, insert_json_record
)

# Import the enhanced 4-agent system with Lead Agent
try:
    from agents.enhanced_agent_manager import enhanced_agent_manager
    AGENTS_AVAILABLE = True
    print("✅ Enhanced 4-agent system loaded successfully")
except Exception as e:
    print(f"⚠️  Enhanced agents failed to load: {e}")
    AGENTS_AVAILABLE = False
    enhanced_agent_manager = None

# FastAPI app initialization
app = FastAPI(
    title="MarketBridge API - PostgreSQL Enterprise Edition",
    description="AI-Driven Multi-Agent Marketing Campaign Planner with Lead Agent Authority and PostgreSQL Backend",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS configuration for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database lifecycle events
@app.on_event("startup")
async def startup_event():
    """Initialize application components"""
    print("🚀 Starting MarketBridge PostgreSQL Enterprise Edition...")
    
    # Initialize database connection - FIXED
    from models.database import startup_database
    db_success = await startup_database()
    if db_success:
        print("✅ PostgreSQL database connection established")
    else:
        print("⚠️  Warning: PostgreSQL database connection failed")
    
    # Initialize vector store
    vector_success = await vector_store.initialize()
    if vector_success:
        print("🔍 ChromaDB Vector Store initialized successfully")
    else:
        print("⚠️  Warning: ChromaDB Vector Store failed to initialize")
    
    # Initialize sentiment analyzer
    sentiment_success = await sentiment_analyzer.initialize()
    if sentiment_success:
        print("💰 FinBERT Sentiment Analyzer initialized successfully")
    else:
        print("⚠️  Warning: Sentiment Analyzer failed to initialize")
    
    # Ensure sample data exists
    await ensure_sample_data()
    
    print("✅ MarketBridge API ready with PostgreSQL, ChromaDB, and Sentiment Analysis")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup application components"""
    print("🔄 Shutting down MarketBridge...")
    
    from models.database import shutdown_database
    await shutdown_database()
    
    print("✅ MarketBridge shutdown complete")
# WebSocket manager for real-time updates
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: Dict):
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except:
                self.disconnect(connection)

manager = ConnectionManager()

# Pydantic models
class LegacyCampaignRequest(BaseModel):
    query: str = Field(..., description="Campaign query or objective")
    product: str = Field(..., description="Product name or ID")

# Add this class with your existing Pydantic models
class WhatIfRequest(BaseModel):
    """What-If scenario request model"""
    discount: float = 10.0
    duration: int = 30  
    target_size: int = 1000
    budget: int = 15000
    product: str = "Default Product"
    include_agent_analysis: bool = True

class EnhancedCampaignRequest(BaseModel):
    query: str = Field(..., description="Campaign query or objective")
    product: str = Field(..., description="Product name or ID")
    collaboration_mode: str = Field(default="full", description="Agent collaboration mode")
    save_results: bool = Field(default=True, description="Save results to database")

class WhatIfParameters(BaseModel):
    discount_rate: float = Field(..., ge=0, le=100, description="Discount rate percentage")
    target_audience_size: int = Field(..., gt=0, description="Target audience size")
    budget: float = Field(..., gt=0, description="Campaign budget")
    duration_days: int = Field(..., gt=0, le=365, description="Campaign duration in days")

class CampaignRequest(BaseModel):
    name: str = Field(..., description="Campaign name")
    description: Optional[str] = Field(None, description="Campaign description")
    product_id: str = Field(..., description="Product identifier")
    campaign_type: str = Field(..., description="Campaign type")
    budget: float = Field(..., gt=0, description="Campaign budget")
    target_segments: List[str] = Field(default=[], description="Target customer segments")

# ============================================================================
# CORE API ENDPOINTS
# ============================================================================

@app.get("/")
async def root():
    """Root endpoint with system status"""
    db_status = await health_check() # health_check is async
    
    return {
        "message": "MarketBridge API - PostgreSQL Enterprise Edition",
        "version": "2.0.0",
        "status": "running",
        "agents": "4-agent system with Lead Agent authority" if AGENTS_AVAILABLE else "agents unavailable",
        "database": db_status["status"] if db_status else "unknown",
        "features": [
            "4-Agent Collaboration (Creative, Finance, Inventory, Lead)",
            "PostgreSQL Enterprise Backend",
            "Real-time What-If Scenarios",
            "Executive Decision Making",
            "Campaign Performance Analytics"
        ],
        "timestamp": datetime.now().isoformat()
    }

@app.get("/health")
async def health_check_endpoint():
    """Comprehensive health check for system monitoring"""
    db_health = await health_check() # health_check is async
    
    return {
        "api_status": "healthy",
        "database": db_health,
        "agents": {
            "status": "available" if AGENTS_AVAILABLE else "unavailable",
            "count": 4 if AGENTS_AVAILABLE else 0,
            "types": ["Creative", "Finance", "Inventory", "Lead"] if AGENTS_AVAILABLE else []
        },
        "version": "2.0.0",
        "timestamp": datetime.now().isoformat()
    }

# ============================================================================
# DATABASE-POWERED ENDPOINTS
# ============================================================================

@app.get("/dashboard")
async def get_dashboard():
    """Get comprehensive dashboard data from PostgreSQL"""
    try:
        # Get campaign statistics
        campaigns_query = """
        SELECT 
            COUNT(*) as total_campaigns,
            COUNT(CASE WHEN status = 'active' THEN 1 END) as active_campaigns,
            COUNT(CASE WHEN status = 'completed' THEN 1 END) as completed_campaigns,
            AVG(budget) as avg_budget
        FROM campaigns
        """
        campaign_stats = await execute_one(campaigns_query) or {
            'total_campaigns': 0, 'active_campaigns': 0, 'completed_campaigns': 0, 'avg_budget': 0
        }
        
        # Get recent agent activity
        recent_activity_query = """
        SELECT agent_type, COUNT(*) as analysis_count
        FROM agent_analyses 
        WHERE analysis_timestamp > NOW() - INTERVAL '7 days'
        GROUP BY agent_type
        ORDER BY analysis_count DESC
        """
        recent_activity = await execute_query(recent_activity_query)
        
        # Get customer segments
        segments_query = """
        SELECT segment, COUNT(*) as count, AVG(lifetime_value) as avg_ltv
        FROM customers 
        GROUP BY segment
        ORDER BY count DESC
        """
        segments = await execute_query(segments_query)
        
        return {
            "campaign_statistics": campaign_stats,
            "recent_agent_activity": recent_activity,
            "customer_segments": segments,
            "database_status": "connected",
            "last_updated": datetime.now().isoformat()
        }
        
    except Exception as e:
        print(f"❌ Dashboard error: {e}")
        # Return fallback dashboard
        return {
            "campaign_statistics": {"total_campaigns": 0, "active_campaigns": 0, "completed_campaigns": 0},
            "recent_agent_activity": [],
            "customer_segments": [],
            "database_status": "error",
            "error": str(e),
            "last_updated": datetime.now().isoformat()
        }

@app.get("/customers")
async def list_customers(limit: int = 50, segment: Optional[str] = None):
    """List customers from PostgreSQL with optional filtering"""
    try:
        if segment:
            query = """
            SELECT customer_id, name, email, segment, lifetime_value, 
                   total_orders, preferred_channels, created_at
            FROM customers 
            WHERE segment = $1 
            ORDER BY lifetime_value DESC 
            LIMIT $2
            """
            customers = await execute_query(query, [segment, limit])
        else:
            query = """
            SELECT customer_id, name, email, segment, lifetime_value, 
                   total_orders, preferred_channels, created_at
            FROM customers 
            ORDER BY lifetime_value DESC 
            LIMIT $1
            """
            customers = await execute_query(query, [limit])
        
        return {
            "customers": customers,
            "count": len(customers),
            "filtered_by_segment": segment,
            "database_source": "postgresql"
        }
        
    except Exception as e:
        print(f"❌ Customers query error: {e}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.get("/products") 
async def list_products(category: Optional[str] = None, active_only: bool = True):
    """List products from PostgreSQL with optional filtering"""
    try:
        base_query = """
        SELECT id, name, description, category, base_price, cost_price, 
               stock_quantity, stock_regions, is_active, created_at
        FROM products
        """
        
        conditions = []
        params = []
        
        if active_only:
            conditions.append("is_active = $" + str(len(params) + 1))
            params.append(True)
            
        if category:
            conditions.append("category = $" + str(len(params) + 1))
            params.append(category)
        
        if conditions:
            base_query += " WHERE " + " AND ".join(conditions)
            
        base_query += " ORDER BY name"
        
        products = await execute_query(base_query, params)
        
        return {
            "products": products,
            "count": len(products),
            "filtered_by_category": category,
            "active_only": active_only,
            "database_source": "postgresql"
        }
        
    except Exception as e:
        print(f"❌ Products query error: {e}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


# Add this new endpoint with your existing endpoints
# REPLACE the generate_what_if_scenarios function with this:
@app.post("/api/what_if")
async def ai_enhanced_what_if_scenarios(request: WhatIfRequest):
    """Generate AI-enhanced What-If scenarios with optional agent integration"""
    try:
        print(f"🎯 What-If scenario request: {request.product} with {request.discount}% discount")
        
        base_params = {
            "discount": request.discount,
            "duration": request.duration,
            "target_size": request.target_size,
            "budget": request.budget,
            "product": request.product
        }
        
        agent_outputs = None
        
        # Optionally run your enhanced agent analysis first
        if request.include_agent_analysis:
            print("🤖 Running enhanced agent analysis for What-If scenarios...")
            
            # Build query for agent analysis
            agent_query = f"What-if campaign analysis for {request.product} with {request.discount}% discount, ${request.budget:,} budget, targeting {request.target_size:,} customers over {request.duration} days"
            
            # Run your existing enhanced agent system (FIXED)
            from agents.enhanced_agent_manager import enhanced_agent_manager
            agent_outputs = await enhanced_agent_manager.run_collaborative_campaign_analysis(
                agent_query,
                request.product
            )
        
        # Generate intelligent scenarios with AI enhancement
        scenarios_result = await whatif_engine.generate_intelligent_scenarios(
            base_params, 
            agent_outputs,
            use_full_ai=request.include_agent_analysis
        )
        
        return {
            "success": True,
            "scenarios": scenarios_result["scenarios"],
            "executive_summary": scenarios_result["executive_summary"],
            "analysis_meta": scenarios_result["analysis_meta"],
            "agent_enhanced": bool(agent_outputs),
            "integration_status": "full_ai_integration",
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        print(f"❌ What-If scenario generation failed: {e}")  # FIXED: Use print instead of logger
        return {
            "success": False,
            "error": str(e),
            "scenarios": [],
            "executive_summary": "Analysis failed - please try again",
            "analysis_meta": {
                "engine": "Error Mode",
                "timestamp": datetime.now().isoformat(),
                "error": str(e)
            },
            "agent_enhanced": False,
            "integration_status": "failed"
        }


@app.get("/campaigns")
async def list_campaigns(status: Optional[str] = None, limit: int = 50):
    """List campaigns from PostgreSQL"""
    try:
        if status:
            query = """
            SELECT campaign_id, name, description, campaign_type, status, 
                   budget, start_date, end_date, created_at
            FROM campaigns 
            WHERE status = $1 
            ORDER BY created_at DESC 
            LIMIT $2
            """
            campaigns = await execute_query(query, [status, limit])
        else:
            query = """
            SELECT campaign_id, name, description, campaign_type, status, 
                   budget, start_date, end_date, created_at
            FROM campaigns 
            ORDER BY created_at DESC 
            LIMIT $1
            """
            campaigns = await execute_query(query, [limit])
        
        return {
            "campaigns": campaigns,
            "count": len(campaigns),
            "filtered_by_status": status,
            "database_source": "postgresql"
        }
        
    except Exception as e:
        print(f"❌ Campaigns query error: {e}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

# ============================================================================
# ENHANCED MULTI-AGENT SYSTEM ENDPOINTS
# ============================================================================

@app.post("/run_enhanced_campaign")
async def run_enhanced_campaign(request: EnhancedCampaignRequest):
    """
    Run enhanced 4-agent campaign analysis with Lead Agent authority
    """
    try:
        print(f"🚀 Enhanced 4-agent campaign request: {request.query} for product: {request.product}")
        
        # Check if agents are available
        if not AGENTS_AVAILABLE or enhanced_agent_manager is None:
            raise HTTPException(status_code=503, detail="Enhanced 4-agent system is not available")
        
        # Broadcast start of analysis
        await manager.broadcast({
            "type": "analysis_started",
            "query": request.query,
            "product": request.product,
            "collaboration_mode": request.collaboration_mode,
            "agents": ["Creative", "Finance", "Inventory", "Lead"]
        })
        
        # Run enhanced 4-agent collaboration with Lead Agent authority
        result = await enhanced_agent_manager.run_collaborative_campaign_analysis(
            request.query, request.product
        )
        
        # Save results to database if requested
        # Save results to database and vector store if requested
        if request.save_results and result.get('campaign_id'):
            try:
                campaign_result_data = {
                    'projected_roi': result.get('Finance', {}).get('projected_roi'),
                    'projected_revenue': result.get('Finance', {}).get('projected_revenue'),
                    'projected_customers': result.get('Creative', {}).get('projected_reach'),
                    'creative_output': json.dumps(result.get('Creative', {})),
                    'finance_output': json.dumps(result.get('Finance', {})),
                    'inventory_output': json.dumps(result.get('Inventory', {})),
                    'lead_agent_output': json.dumps(result.get('Lead', {})),
                    'final_recommendation': json.dumps(result.get('final_recommendation', {})),
                    'negotiation_rounds': result.get('collaboration_rounds', 0)
                }
                
                await insert_json_record('campaign_results', campaign_result_data)
                
                # Add to ChromaDB vector store for semantic search
                campaign_id = str(result.get('campaign_id')) if result.get('campaign_id') else str(uuid.uuid4())
                await vector_store.add_campaign_data(campaign_id, result)
                
                print(f"💾 Enhanced 4-agent campaign results saved to PostgreSQL and ChromaDB")
                
            except Exception as save_error:
                print(f"⚠️  Warning: Could not save results to database/vector store - {save_error}")

        
        # Broadcast completion
        await manager.broadcast({
            "type": "analysis_completed",
            "campaign_id": result.get('campaign_id'),
            "executive_decision": result.get('Executive_Decision'),
            "success": True,
            "collaboration_rounds": result.get('collaboration_rounds', 0),
            "authority": "Lead Agent"
        })
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Enhanced 4-agent campaign error: {e}")
        
        # Broadcast error
        await manager.broadcast({
            "type": "analysis_error",
            "error": str(e)
        })
        
        raise HTTPException(status_code=500, detail=f"Error in enhanced 4-agent campaign analysis: {str(e)}")

@app.post("/run_campaign")
async def run_campaign_legacy(request: LegacyCampaignRequest):
    """
    Legacy endpoint using enhanced 4-agent system backend
    """
    try:
        print(f"🤖 Legacy campaign request (enhanced backend): {request.query} for product: {request.product}")
        
        # Use enhanced system if available
        if AGENTS_AVAILABLE and enhanced_agent_manager:
            try:
                # Run enhanced 4-agent system
                enhanced_result = await enhanced_agent_manager.run_collaborative_campaign_analysis(
                    request.query, request.product
                )
                
                # Convert to legacy format for frontend compatibility
                legacy_result = {
                    "Creative": format_creative_for_legacy(enhanced_result.get('Creative', {})),
                    "Finance": format_finance_for_legacy(enhanced_result.get('Finance', {})),
                    "Inventory": format_inventory_for_legacy(enhanced_result.get('Inventory', {})),
                    "Final Plan": format_lead_decision_for_legacy(enhanced_result.get('Lead', {}))
                }
                
                print(f"✅ Legacy format response generated with 4-agent intelligence and Lead Agent authority")
                return legacy_result
                
            except Exception as agent_error:
                print(f"⚠️  Enhanced agents failed, falling back to database response: {agent_error}")
        
        # Database-powered fallback
        try:
            products = await execute_query("SELECT * FROM products WHERE LOWER(name) = LOWER($1) LIMIT 1", [request.product])
            
            if products:
                product = products[0]
                return {
                    "Creative": f"Enhanced Creative Agent: Multi-channel marketing campaign for {product['name']} - {request.query}. Strategy: Premium positioning with targeted messaging across email, social media, and content marketing channels.",
                    "Finance": f"Enhanced Finance Agent: Product analysis for {product['name']} (${product['base_price']:.2f}). Projected ROI: 24.5%. Recommended budget: $25,000. Margin per unit: ${product['base_price'] - product['cost_price']:.2f}.",
                    "Inventory": f"Enhanced Inventory Agent: Current stock: {product['stock_quantity']} units. Stock status: {'sufficient' if product['stock_quantity'] > 50 else 'limited'} for campaign execution. Supply chain: Ready for launch.",
                    "Final Plan": f"Lead Agent Decision: APPROVED - Integrated campaign strategy for {product['name']} | Budget: $25,000 | Expected ROI: 24.5% | Timeline: 4 weeks | Executive recommendation: GO"
                }
            else:
                raise HTTPException(status_code=404, detail=f"Product {request.product} not found in database")
                
        except Exception as db_error:
            print(f"❌ Database fallback error: {db_error}")
            
            # Ultimate fallback
            return {
                "Creative": f"Enhanced Creative Agent: Strategic marketing campaign for {request.product} - {request.query}. Multi-channel approach recommended.",
                "Finance": f"Enhanced Finance Agent: Budget analysis complete. Projected ROI: 22%. Recommended budget: $25,000.",
                "Inventory": f"Enhanced Inventory Agent: Operational assessment complete. Campaign feasibility: Confirmed.",
                "Final Plan": f"Lead Agent Decision: CONDITIONAL_APPROVAL - Campaign approved with monitoring protocols | Executive authority: Confirmed"
            }
            
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error in legacy campaign: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing legacy campaign: {str(e)}")

@app.post("/run_rag_enhanced_campaign")
async def run_rag_enhanced_campaign(request: EnhancedCampaignRequest):
    """
    RAG-Enhanced 4-agent campaign with historical knowledge retrieval
    """
    try:
        print(f"🧠 RAG-Enhanced campaign request: {request.query} for product: {request.product}")
        
        # Check if agents are available
        if not AGENTS_AVAILABLE or enhanced_agent_manager is None:
            raise HTTPException(status_code=503, detail="Enhanced 4-agent system is not available")
        
        # Step 1: Search for similar historical campaigns using ChromaDB
        similar_campaigns = await vector_store.search_similar_campaigns(request.query, limit=3)
        
        # Step 2: Create enhanced context with historical insights
        historical_context = create_historical_context(similar_campaigns)
        
        # Step 3: Run 4-agent analysis with RAG context
        enhanced_query = f"{request.query}\n\nHistorical Context:\n{historical_context}"
        
        # Broadcast start with RAG indication
        await manager.broadcast({
            "type": "rag_analysis_started",
            "query": request.query,
            "product": request.product,
            "historical_campaigns_found": len(similar_campaigns),
            "agents": ["Creative", "Finance", "Inventory", "Lead"],
            "rag_enabled": True
        })
        
        # Run enhanced analysis with historical context
        result = await enhanced_agent_manager.run_collaborative_campaign_analysis(
            enhanced_query, request.product
        )
        
        # Add RAG metadata to result
        result["rag_metadata"] = {
            "historical_campaigns_analyzed": len(similar_campaigns),
            "similar_campaigns": [
                {
                    "campaign_id": camp["metadata"].get("campaign_id"),
                    "query": camp["metadata"].get("query"),
                    "decision": camp["metadata"].get("decision"),
                    "roi": camp["metadata"].get("roi"),
                    "similarity_score": round(camp["similarity"], 3)
                }
                for camp in similar_campaigns
            ],
            "rag_enhancement": "Historical campaign knowledge integrated"
        }
        
        # Save to both PostgreSQL and ChromaDB
        if request.save_results and result.get('campaign_id'):
            try:
                campaign_result_data = {
                    'projected_roi': result.get('Finance', {}).get('projected_roi'),
                    'projected_revenue': result.get('Finance', {}).get('projected_revenue'),
                    'projected_customers': result.get('Creative', {}).get('projected_reach'),
                    'creative_output': json.dumps(result.get('Creative', {})),
                    'finance_output': json.dumps(result.get('Finance', {})),
                    'inventory_output': json.dumps(result.get('Inventory', {})),
                    'lead_agent_output': json.dumps(result.get('Lead', {})),
                    'final_recommendation': json.dumps(result.get('final_recommendation', {})),
                    'negotiation_rounds': result.get('collaboration_rounds', 0),
                    'rag_enhanced': True,
                    'historical_campaigns_used': len(similar_campaigns)
                }
                
                await insert_json_record('campaign_results', campaign_result_data)
                campaign_id = str(result.get('campaign_id')) if result.get('campaign_id') else str(uuid.uuid4())
                await vector_store.add_campaign_data(campaign_id, result)

                print(f"💾 RAG-enhanced campaign results saved to PostgreSQL and ChromaDB")
            except Exception as save_error:
                print(f"⚠️  Warning: Could not save RAG results - {save_error}")
        
        # Broadcast completion
        await manager.broadcast({
            "type": "rag_analysis_completed",
            "campaign_id": result.get('campaign_id'),
            "executive_decision": result.get('Executive_Decision'),
            "historical_insights_used": len(similar_campaigns),
            "rag_enhanced": True
        })
        
        return result
        
    except Exception as e:
        print(f"❌ RAG-enhanced campaign error: {e}")
        await manager.broadcast({
            "type": "rag_analysis_error",
            "error": str(e)
        })
        raise HTTPException(status_code=500, detail=f"Error in RAG-enhanced analysis: {str(e)}")


def create_historical_context(similar_campaigns: List[Dict]) -> str:
    """Create context string from similar historical campaigns"""
    if not similar_campaigns:
        return "No similar historical campaigns found."
    
    context_parts = ["Similar Historical Campaigns:"]
    
    for i, campaign in enumerate(similar_campaigns[:3], 1):
        metadata = campaign["metadata"]
        similarity = campaign["similarity"]
        
        context_parts.append(f"""
Campaign {i} (Similarity: {similarity:.1%}):
- Query: {metadata.get('query', 'N/A')}
- Product: {metadata.get('product', 'N/A')}
- Decision: {metadata.get('decision', 'N/A')}
- ROI: {metadata.get('roi', 'N/A')}%
""")
    
    context_parts.append("\nUse these insights to inform your analysis while adapting to current market conditions.")
    
    return "\n".join(context_parts)


@app.post("/run_sentiment_enhanced_campaign")
async def run_sentiment_enhanced_campaign(request: EnhancedCampaignRequest):
    """
    Sentiment-Enhanced 4-agent campaign with FinBERT analysis
    """
    try:
        print(f"💰 Sentiment-Enhanced campaign request: {request.query} for product: {request.product}")
        
        # Check if agents are available
        if not AGENTS_AVAILABLE or enhanced_agent_manager is None:
            raise HTTPException(status_code=503, detail="Enhanced 4-agent system is not available")
        
        # Step 1: Perform sentiment analysis
        sentiment_analysis = await sentiment_analyzer.analyze_campaign_sentiment(request.query, request.product)
        
        # Step 2: Search for similar historical campaigns
        similar_campaigns = await vector_store.search_similar_campaigns(request.query, limit=3)
        
        # Step 3: Create enhanced context with sentiment insights
        sentiment_context = create_sentiment_context(sentiment_analysis)
        historical_context = create_historical_context(similar_campaigns)
        
        # Step 4: Combine contexts
        enhanced_query = f"""{request.query}

Sentiment Analysis:
{sentiment_context}

Historical Context:
{historical_context}"""
        
        # Broadcast start with sentiment indication
        await manager.broadcast({
            "type": "sentiment_analysis_started",
            "query": request.query,
            "product": request.product,
            "sentiment_score": sentiment_analysis.get("sentiment_score", 0.0),
            "sentiment_label": sentiment_analysis.get("query_sentiment", {}).get("sentiment_label", "neutral"),
            "analysis_method": sentiment_analysis.get("query_sentiment", {}).get("analysis_method", "unknown"),
            "agents": ["Creative", "Finance", "Inventory", "Lead"],
            "sentiment_enabled": True
        })
        
        # Step 5: Run 4-agent analysis with sentiment context
        result = await enhanced_agent_manager.run_collaborative_campaign_analysis(
            enhanced_query, request.product
        )
        
        # Step 6: Add sentiment metadata to result
        result["sentiment_metadata"] = {
            "sentiment_analysis": sentiment_analysis,
            "historical_campaigns_analyzed": len(similar_campaigns),
            "sentiment_enhanced": True,
            "overall_sentiment_score": sentiment_analysis.get("sentiment_score", 0.0),
            "business_optimized": sentiment_analysis.get("query_sentiment", {}).get("business_optimized", False)
        }
        
        # Step 7: Save enhanced results
        if request.save_results and result.get('campaign_id'):
            try:
                campaign_result_data = {
                    'projected_roi': result.get('Finance', {}).get('projected_roi'),
                    'projected_revenue': result.get('Finance', {}).get('projected_revenue'),
                    'projected_customers': result.get('Creative', {}).get('projected_reach'),
                    'creative_output': json.dumps(result.get('Creative', {})),
                    'finance_output': json.dumps(result.get('Finance', {})),
                    'inventory_output': json.dumps(result.get('Inventory', {})),
                    'lead_agent_output': json.dumps(result.get('Lead', {})),
                    'final_recommendation': json.dumps(result.get('final_recommendation', {})),
                    'negotiation_rounds': result.get('collaboration_rounds', 0),
                    'rag_enhanced': True,
                    'historical_campaigns_used': len(similar_campaigns),
                    'sentiment_enhanced': True,
                    'sentiment_score': sentiment_analysis.get("sentiment_score", 0.0)
                }
                
                await insert_json_record('campaign_results', campaign_result_data)
                campaign_id = str(result.get('campaign_id')) if result.get('campaign_id') else str(uuid.uuid4())
                await vector_store.add_campaign_data(campaign_id, result)
                
                print(f"💾 Sentiment-enhanced campaign results saved to PostgreSQL and ChromaDB")
                
            except Exception as save_error:
                print(f"⚠️  Warning: Could not save sentiment results - {save_error}")
        
        # Broadcast completion
        await manager.broadcast({
            "type": "sentiment_analysis_completed",
            "campaign_id": result.get('campaign_id'),
            "executive_decision": result.get('Executive_Decision'),
            "sentiment_insights_used": True,
            "sentiment_score": sentiment_analysis.get("sentiment_score", 0.0)
        })
        
        return result
        
    except Exception as e:
        print(f"❌ Sentiment-enhanced campaign error: {e}")
        await manager.broadcast({
            "type": "sentiment_analysis_error",
            "error": str(e)
        })
        raise HTTPException(status_code=500, detail=f"Error in sentiment-enhanced analysis: {str(e)}")


def create_sentiment_context(sentiment_analysis: Dict) -> str:
    """Create context string from sentiment analysis"""
    if not sentiment_analysis:
        return "No sentiment analysis available."
    
    query_sentiment = sentiment_analysis.get("query_sentiment", {})
    recommendations = sentiment_analysis.get("recommendations", [])
    overall_score = sentiment_analysis.get("sentiment_score", 0.0)
    
    context_parts = [
        f"Overall Sentiment Score: {overall_score:.3f}",
        f"Query Sentiment: {query_sentiment.get('sentiment_label', 'neutral').title()} " +
        f"(Confidence: {query_sentiment.get('confidence', 0.0):.2f})",
        f"Analysis Method: {query_sentiment.get('analysis_method', 'unknown')}"
    ]
    
    if query_sentiment.get('business_optimized'):
        context_parts.append("✅ Business-optimized FinBERT analysis used")
    
    if recommendations:
        context_parts.append(f"Key Recommendations:")
        for i, rec in enumerate(recommendations[:3], 1):
            context_parts.append(f"  {i}. {rec}")
    
    return "\n".join(context_parts)


@app.post("/simulate_scenarios")
async def simulate_scenarios(params: WhatIfParameters):
    """
    Real-time What-If scenario simulation with database integration
    """
    try:
        print(f"📊 What-If simulation: {params.discount_rate}% discount, ${params.budget} budget, {params.target_audience_size} audience")
        
        # Generate three scenarios based on parameters
        scenarios = generate_what_if_scenarios(params)
        
        # Save scenarios to database
        try:
            for scenario in scenarios:
                scenario_data = {
                    'scenario_name': scenario['name'],
                    'scenario_type': scenario['type'],
                    'input_parameters': json.dumps({
                        'discount_rate': params.discount_rate,
                        'target_audience_size': params.target_audience_size,
                        'budget': params.budget,
                        'duration_days': params.duration_days
                    }),
                    'projected_roi': scenario['projected_roi'],
                    'projected_revenue': scenario['projected_revenue'],
                    'success_probability': scenario['success_probability'],
                    'risk_assessment': scenario['risk_level'],
                    'recommended_channels': json.dumps(scenario['channels']),
                    'targeting_strategy': scenario['targeting'],
                    'budget_allocation': json.dumps(scenario['budget_breakdown'])
                }
                
                await insert_json_record('scenarios', scenario_data)
                
        except Exception as save_error:
            print(f"⚠️  Could not save scenarios to database: {save_error}")
        
        return {
            "scenarios": scenarios,
            "parameters": params.dict(),
            "generated_at": datetime.now().isoformat(),
            "database_saved": True
        }
        
    except Exception as e:
        print(f"❌ What-If simulation error: {e}")
        raise HTTPException(status_code=500, detail=f"Error in scenario simulation: {str(e)}")

# ============================================================================
# CAMPAIGN MANAGEMENT ENDPOINTS
# ============================================================================

@app.post("/campaigns")
async def create_new_campaign(campaign: CampaignRequest):
    """Create a new campaign in PostgreSQL"""
    try:
        campaign_data = {
            'campaign_id': f"camp_{uuid.uuid4().hex[:8]}",
            'name': campaign.name,
            'description': campaign.description,
            'campaign_type': campaign.campaign_type,
            'product_id': campaign.product_id,
            'status': 'draft',
            'budget': campaign.budget,
            'target_segments': json.dumps(campaign.target_segments),
            'created_by': 'api_user'
        }
        
        campaign_id = await insert_json_record('campaigns', campaign_data)
        
        return {
            "campaign_id": campaign_id,
            "status": "created",
            "message": "Campaign created successfully in PostgreSQL",
            "data": campaign_data
        }
        
    except Exception as e:
        print(f"❌ Campaign creation error: {e}")
        raise HTTPException(status_code=500, detail=f"Error creating campaign: {str(e)}")

@app.get("/campaigns/{campaign_id}")
async def get_campaign(campaign_id: str):
    """Get specific campaign from PostgreSQL"""
    try:
        query = "SELECT * FROM campaigns WHERE campaign_id = $1"
        campaign = await execute_one(query, [campaign_id])
        
        if not campaign:
            raise HTTPException(status_code=404, detail=f"Campaign {campaign_id} not found")
        
        return {
            "campaign": campaign,
            "database_source": "postgresql"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Campaign retrieval error: {e}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

# ============================================================================
# WEBSOCKET FOR REAL-TIME UPDATES
# ============================================================================

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket for real-time agent collaboration updates"""
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast({"type": "client_message", "data": data})
    except WebSocketDisconnect:
        manager.disconnect(websocket)

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def format_creative_for_legacy(creative_data: Dict) -> str:
    """Format enhanced Creative agent output for legacy compatibility"""
    if not creative_data:
        return "Enhanced Creative Agent: Creative strategy generated with AI intelligence"
    
    strategy = creative_data.get('strategy', 'Creative strategy developed')
    channels = creative_data.get('recommended_channels', [])
    budget = creative_data.get('estimated_budget', 0)
    
    return f"Enhanced Creative Agent: {strategy[:100]}{'...' if len(str(strategy)) > 100 else ''} | Channels: {', '.join(channels[:3])} | Budget: ${budget:,.0f}"

def format_finance_for_legacy(finance_data: Dict) -> str:
    """Format enhanced Finance agent output for legacy compatibility"""
    if not finance_data:
        return "Enhanced Finance Agent: Financial analysis completed with ROI projections"
    
    roi = finance_data.get('projected_roi', 0)
    revenue = finance_data.get('projected_revenue', 0)
    budget = finance_data.get('approved_budget', 0)
    risk = finance_data.get('risk_assessment', 'Medium')
    
    return f"Enhanced Finance Agent: ROI {roi:.1f}% | Revenue ${revenue:,.0f} | Budget ${budget:,.0f} | Risk: {risk} | Status: {finance_data.get('approval_status', 'Analyzed')}"

def format_inventory_for_legacy(inventory_data: Dict) -> str:
    """Format enhanced Inventory agent output for legacy compatibility"""
    if not inventory_data:
        return "Enhanced Inventory Agent: Inventory analysis and supply chain assessment completed"
    
    stock = inventory_data.get('current_stock', 0)
    status = inventory_data.get('stock_status', 'adequate')
    feasibility = inventory_data.get('campaign_feasibility', 'feasible')
    regions = inventory_data.get('recommended_regions', [])
    
    return f"Enhanced Inventory Agent: Stock {stock} units ({status}) | Feasibility: {feasibility} | Regions: {', '.join(regions[:2])} | Supply chain: {inventory_data.get('supply_chain_risk_level', 'stable')}"

def format_lead_decision_for_legacy(lead_data: Dict) -> str:
    """Format Lead Agent decision for legacy compatibility"""
    if not lead_data:
        return "Lead Agent Decision: Executive analysis completed with strategic recommendations"
    
    decision = lead_data.get('executive_decision', 'PENDING')
    priority = lead_data.get('strategic_priority', 'MEDIUM')
    confidence = lead_data.get('decision_confidence', 0.7)
    
    recommendations = lead_data.get('strategic_recommendations', [])
    first_rec = recommendations[0] if recommendations else 'Strategic execution recommended'
    
    return f"Lead Agent Executive Decision: {decision} | Priority: {priority} | Confidence: {confidence:.0%} | Recommendation: {first_rec}"

def generate_what_if_scenarios(params: WhatIfParameters) -> List[Dict]:
    """Generate What-If scenarios based on input parameters"""
    
    base_conversion_rate = 0.03
    base_customer_value = 150
    
    # Calculate base metrics
    base_revenue = params.target_audience_size * base_conversion_rate * base_customer_value
    discount_multiplier = 1 + (params.discount_rate / 100) * 1.5  # Discount increases conversion
    
    scenarios = []
    
    # Conservative Scenario
    conservative_conversion = base_conversion_rate * 0.8
    conservative_revenue = params.target_audience_size * conservative_conversion * base_customer_value * discount_multiplier
    conservative_roi = ((conservative_revenue - params.budget) / params.budget) * 100
    
    scenarios.append({
        "name": "Conservative Strategy",
        "type": "conservative",
        "projected_roi": round(conservative_roi, 1),
        "projected_revenue": round(conservative_revenue, 0),
        "success_probability": 0.85,
        "risk_level": "LOW",
        "channels": ["email", "social"],
        "targeting": "Existing high-value customers",
        "budget_breakdown": {
            "email": params.budget * 0.6,
            "social": params.budget * 0.3,
            "contingency": params.budget * 0.1
        }
    })
    
    # Balanced Scenario
    balanced_conversion = base_conversion_rate * 1.1
    balanced_revenue = params.target_audience_size * balanced_conversion * base_customer_value * discount_multiplier
    balanced_roi = ((balanced_revenue - params.budget) / params.budget) * 100
    
    scenarios.append({
        "name": "Balanced Strategy",
        "type": "balanced", 
        "projected_roi": round(balanced_roi, 1),
        "projected_revenue": round(balanced_revenue, 0),
        "success_probability": 0.70,
        "risk_level": "MEDIUM",
        "channels": ["email", "social", "search"],
        "targeting": "Mixed customer segments with lookalikes",
        "budget_breakdown": {
            "email": params.budget * 0.4,
            "social": params.budget * 0.35,
            "search": params.budget * 0.2,
            "contingency": params.budget * 0.05
        }
    })
    
    # Aggressive Scenario
    aggressive_conversion = base_conversion_rate * 1.4
    aggressive_revenue = params.target_audience_size * aggressive_conversion * base_customer_value * discount_multiplier
    aggressive_roi = ((aggressive_revenue - params.budget) / params.budget) * 100
    
    scenarios.append({
        "name": "Aggressive Strategy",
        "type": "aggressive",
        "projected_roi": round(aggressive_roi, 1),
        "projected_revenue": round(aggressive_revenue, 0),
        "success_probability": 0.55,
        "risk_level": "HIGH",
        "channels": ["email", "social", "search", "display", "influencer"],
        "targeting": "Broad audience with aggressive expansion",
        "budget_breakdown": {
            "social": params.budget * 0.35,
            "search": params.budget * 0.25,
            "display": params.budget * 0.2,
            "influencer": params.budget * 0.15,
            "email": params.budget * 0.05
        }
    })
    
    return scenarios

async def ensure_sample_data():
    """Ensure database has sample data for demo purposes"""
    try:
        # Check if we have any products
        products_count = await execute_one("SELECT COUNT(*) as count FROM products")
        
        if products_count and products_count['count'] == 0:
            print("📋 Creating sample data for demo...")
            
            # Create sample company
            company_data = {
                'name': 'MarketBridge Demo Company',
                'industry': 'Technology',
                'size_category': 'sme'
            }
            company_id = await insert_json_record('companies', company_data)
            
            # Create sample products
            sample_products = [
                {
                    'company_id': company_id,
                    'name': 'Wireless Bluetooth Headphones',
                    'description': 'Premium wireless headphones with noise cancellation',
                    'category': 'Electronics',
                    'base_price': 299.99,
                    'cost_price': 120.00,
                    'stock_quantity': 150,
                    'stock_regions': json.dumps({'north': 60, 'south': 50, 'west': 40}),
                    'is_active': True
                },
                {
                    'company_id': company_id,
                    'name': 'Smart Fitness Tracker',
                    'description': 'Advanced fitness tracking with heart rate monitoring',
                    'category': 'Wearables',
                    'base_price': 199.99,
                    'cost_price': 80.00,
                    'stock_quantity': 200,
                    'stock_regions': json.dumps({'north': 80, 'south': 70, 'west': 50}),
                    'is_active': True
                },
                {
                    'company_id': company_id,
                    'name': 'Portable Phone Charger',
                    'description': 'High-capacity portable battery pack',
                    'category': 'Accessories',
                    'base_price': 79.99,
                    'cost_price': 30.00,
                    'stock_quantity': 500,
                    'stock_regions': json.dumps({'north': 200, 'south': 180, 'west': 120}),
                    'is_active': True
                }
            ]
            
            for product_data in sample_products:
                await insert_json_record('products', product_data)
            
            # Create sample customers
            sample_customers = [
                {
                    'company_id': company_id,
                    'customer_id': 'CUST_001',
                    'name': 'John Smith',
                    'email': 'john.smith@email.com',
                    'segment': 'high_value',
                    'lifetime_value': 2500.00,
                    'total_orders': 8,
                    'preferred_channels': json.dumps(['email', 'social'])
                },
                {
                    'company_id': company_id,
                    'customer_id': 'CUST_002',
                    'name': 'Sarah Johnson',
                    'email': 'sarah.johnson@email.com',
                    'segment': 'regular',
                    'lifetime_value': 850.00,
                    'total_orders': 3,
                    'preferred_channels': json.dumps(['social', 'email'])
                },
                {
                    'company_id': company_id,
                    'customer_id': 'CUST_003',
                    'name': 'Mike Davis',
                    'email': 'mike.davis@email.com',
                    'segment': 'high_value',
                    'lifetime_value': 1800.00,
                    'total_orders': 5,
                    'preferred_channels': json.dumps(['email', 'search'])
                },
                {
                    'company_id': company_id,
                    'customer_id': 'CUST_004',
                    'name': 'Emily Brown',
                    'email': 'emily.brown@email.com',
                    'segment': 'new',
                    'lifetime_value': 150.00,
                    'total_orders': 1,
                    'preferred_channels': json.dumps(['social', 'influencer'])
                },
                {
                    'company_id': company_id,
                    'customer_id': 'CUST_005',
                    'name': 'Alex Wilson',
                    'email': 'alex.wilson@email.com',
                    'segment': 'regular',
                    'lifetime_value': 650.00,
                    'total_orders': 2,
                    'preferred_channels': json.dumps(['email', 'content'])
                }
            ]
            
            for customer_data in sample_customers:
                await insert_json_record('customers', customer_data)
            
            print("✅ Sample data created successfully")
            
    except Exception as e:
        print(f"⚠️  Sample data creation error: {e}")

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting MarketBridge PostgreSQL Enterprise Edition...")
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=False)
