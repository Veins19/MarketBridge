from fastapi import FastAPI
from pydantic import BaseModel
from scenario_generator import generate_scenarios
from fastapi.middleware.cors import CORSMiddleware   # <-- NEW

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class WhatIfRequest(BaseModel):
    discount: float
    duration: int
    target_size: int
    budget: int

@app.post("/api/what_if")
async def what_if(request: WhatIfRequest):
    scenarios = generate_scenarios(
        request.discount, 
        request.duration, 
        request.target_size, 
        request.budget
    )
    return {"scenarios": scenarios}

