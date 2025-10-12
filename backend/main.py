from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from agent_manager import run_agents

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CampaignRequest(BaseModel):
    query: str
    product: str

@app.post("/run_campaign")
def run_campaign(request: CampaignRequest):
    results = run_agents(request.query, request.product)
    return results
