import json
import os
from agents.creative_agent import creative_agent
from agents.finance_agent import finance_agent
from agents.inventory_agent import inventory_agent

def run_agents(query, product):
    # get the absolute path to the data folder
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(base_dir, "data")

    # make sure the data folder exists
    os.makedirs(data_dir, exist_ok=True)

    budget_path = os.path.join(data_dir, "budget.json")
    inventory_path = os.path.join(data_dir, "inventory.json")

    # create default files if they don’t exist
    if not os.path.exists(budget_path):
        with open(budget_path, "w") as f:
            json.dump({"total_budget": 10000}, f)

    if not os.path.exists(inventory_path):
        with open(inventory_path, "w") as f:
            json.dump({"items": []}, f)

    # load data safely
    with open(budget_path) as f:
        budget_data = json.load(f)
    budget = budget_data.get("total_budget", 10000)

    with open(inventory_path) as f:
        inventory_data = json.load(f)

    # run agents
    creative = creative_agent(query)
    finance = finance_agent(creative, budget)
    inventory = inventory_agent(product, inventory_data)

    return {
        "Creative": creative,
        "Finance": finance,
        "Inventory": inventory,
        "Final Plan": f"{creative} | {finance} | {inventory}"
    }
