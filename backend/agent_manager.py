import json
import os
from agents.creative_agent import creative_agent
from agents.finance_agent import finance_agent  
from agents.inventory_agent import inventory_agent

def run_agents(query, product):
    """
    Enhanced agent manager with better error handling and logging
    """
    
    # Get the absolute path to the data folder
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(base_dir, "data")
    
    # Make sure the data folder exists
    os.makedirs(data_dir, exist_ok=True)
    
    budget_path = os.path.join(data_dir, "budget.json")
    inventory_path = os.path.join(data_dir, "inventory.json")
    
    # Create default files if they don't exist
    if not os.path.exists(budget_path):
        with open(budget_path, "w") as f:
            json.dump({"total_budget": 10000}, f)
    
    if not os.path.exists(inventory_path):
        with open(inventory_path, "w") as f:
            json.dump({"items": []}, f)
    
    # Load data safely with error handling
    try:
        with open(budget_path) as f:
            budget_data = json.load(f)
        budget = budget_data.get("total_budget", 10000)
        
        with open(inventory_path) as f:
            inventory_data = json.load(f)
    
    except (json.JSONDecodeError, FileNotFoundError) as e:
        print(f"Error loading data: {e}")
        budget = 10000
        inventory_data = {"items": []}
    
    # Run agents with error handling
    try:
        print(f"🤖 Running Creative Agent for: {query}")
        creative = creative_agent(query, product)

    except Exception as e:
        creative = f"Creative Agent: Error occurred - {str(e)}"
    
    try:
        finance = finance_agent(creative, budget)
        inventory = inventory_agent(product, inventory_data)
    except Exception as e:
        finance = f"Finance Agent: Error occurred - {str(e)}"
        inventory = f"Inventory Agent: Error occurred - {str(e)}"
    
    return {
        "Creative": creative,
        "Finance": finance,
        "Inventory": inventory,
        "Final Plan": f"Campaign Strategy: {creative[:100]}... | Budget Status: {finance} | Stock Status: {inventory}"
    }
