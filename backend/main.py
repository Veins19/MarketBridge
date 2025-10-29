from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from agent_manager import run_agents
import uvicorn

# Import WebSocket manager
from websocket_manager import ws_manager

app = FastAPI(title="MarketBridge API", version="1.0.0")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CampaignRequest(BaseModel):
    query: str
    product: str

# WebSocket endpoint for real-time agent collaboration
@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await ws_manager.connect(websocket, client_id)
    try:
        while True:
            data = await websocket.receive_text()
            # Handle incoming WebSocket messages if needed
            print(f"📡 Received from {client_id}: {data}")
    except WebSocketDisconnect:
        ws_manager.disconnect(client_id)

@app.get("/")
async def root():
    return {"message": "MarketBridge API is running!", "status": "healthy"}

@app.post("/run_campaign")
async def run_campaign(request: CampaignRequest):
    """
    Run the multi-agent campaign planning system
    """
    try:
        print(f"🚀 Processing campaign request: {request.product}")
        
        result = run_agents(request.query, request.product)
        
        # Debug: Print the result structure
        print("📊 Backend result structure:")
        print(f"  Keys: {list(result.keys())}")
        print(f"  Creative length: {len(result.get('Creative', ''))}")
        print(f"  Finance length: {len(result.get('Finance', ''))}")
        print(f"  Inventory length: {len(result.get('Inventory', ''))}")
        print(f"  Final Plan length: {len(result.get('Final Plan', ''))}")
        
        response_data = {
            "success": True,
            "data": result
        }
        
        print("✅ Sending response to frontend...")
        return response_data
        
    except Exception as e:
        print(f"❌ Error processing campaign: {str(e)}")
        import traceback
        traceback.print_exc()
        return {
            "success": False,
            "error": str(e)
        }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "MarketBridge backend is operational"}

if __name__ == "__main__":
    print("🚀 Starting MarketBridge Backend Server...")
    print("📡 Server will be available at: http://localhost:8000")
    print("📖 API Documentation: http://localhost:8000/docs")
    print("🔄 Press Ctrl+C to stop the server")
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
