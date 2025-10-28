import json
import os
from typing import Dict, List, Any
from dataclasses import dataclass
from agents.creative_agent import CreativeAgent
from agents.finance_agent import FinanceAgent  
from agents.inventory_agent import InventoryAgent

@dataclass
class AgentMessage:
    """Structure for inter-agent communication"""
    sender: str
    recipient: str
    message_type: str  # 'proposal', 'feedback', 'constraint', 'approval'
    content: Dict[str, Any]
    round_number: int = 1

@dataclass
class CampaignContext:
    """Shared context between all agents"""
    query: str
    product: str
    budget: float
    inventory_data: Dict
    customer_data: Dict
    constraints: List[str] = None
    
    def __post_init__(self):
        if self.constraints is None:
            self.constraints = []

class MultiAgentCoordinator:
    """Coordinates communication and negotiation between agents"""
    
    def __init__(self):
        self.creative_agent = CreativeAgent()
        self.finance_agent = FinanceAgent()
        self.inventory_agent = InventoryAgent()
        self.message_history: List[AgentMessage] = []
        self.negotiation_rounds = 2
        
    def load_data_context(self) -> CampaignContext:
        """Load all necessary data for campaign planning"""
        base_dir = os.path.dirname(os.path.abspath(__file__))
        data_dir = os.path.join(base_dir, "data")
        
        # Ensure data directory exists
        os.makedirs(data_dir, exist_ok=True)
        
        # Load budget data
        budget_path = os.path.join(data_dir, "budget.json")
        if not os.path.exists(budget_path):
            with open(budget_path, "w") as f:
                json.dump({
                    "total_budget": 100000,
                    "allocated_budget": 0,
                    "available_budget": 100000,
                    "min_roi_threshold": 0.20
                }, f)
        
        # Load inventory data
        inventory_path = os.path.join(data_dir, "inventory.json")
        if not os.path.exists(inventory_path):
            with open(inventory_path, "w") as f:
                json.dump({
                    "products": [
                        {"name": "iPhone 15", "stock": 150, "region": "North", "cost": 800, "price": 999},
                        {"name": "Samsung Galaxy", "stock": 120, "region": "South", "cost": 700, "price": 899},
                        {"name": "Laptop Pro", "stock": 80, "region": "East", "cost": 1200, "price": 1599}
                    ]
                }, f)
        
        # Load customer data
        customer_path = os.path.join(data_dir, "customers.json")
        if not os.path.exists(customer_path):
            with open(customer_path, "w") as f:
                json.dump({
                    "segments": [
                        {"name": "Young Professionals", "size": 25000, "avg_spend": 1200, "conversion_rate": 0.08},
                        {"name": "Tech Enthusiasts", "size": 15000, "avg_spend": 1800, "conversion_rate": 0.12},
                        {"name": "Budget Conscious", "size": 40000, "avg_spend": 600, "conversion_rate": 0.15}
                    ]
                }, f)
        
        try:
            with open(budget_path) as f:
                budget_data = json.load(f)
            with open(inventory_path) as f:
                inventory_data = json.load(f)
            with open(customer_path) as f:
                customer_data = json.load(f)
                
        except Exception as e:
            print(f"Error loading data: {e}")
            # Fallback data
            budget_data = {"available_budget": 50000}
            inventory_data = {"products": []}
            customer_data = {"segments": []}
            
        return budget_data, inventory_data, customer_data
    
    def send_message(self, message: AgentMessage):
        """Record agent communication"""
        self.message_history.append(message)
        print(f"📨 {message.sender} → {message.recipient}: {message.message_type}")
    
    def run_coordinated_campaign(self, query: str, product: str) -> Dict[str, Any]:
        """Main coordination function with multi-round negotiation"""
        
        # Load shared context
        budget_data, inventory_data, customer_data = self.load_data_context()
        
        context = CampaignContext(
            query=query,
            product=product,
            budget=budget_data.get("available_budget", 50000),
            inventory_data=inventory_data,
            customer_data=customer_data
        )
        
        print(f"🚀 Starting coordinated campaign planning for: {product}")
        print(f"💰 Available Budget: ${context.budget:,.2f}")
        
        # Phase 1: Initial Analysis (Each agent works independently)
        print("\n=== Phase 1: Independent Analysis ===")
        
        creative_proposal = self.creative_agent.analyze(context)
        finance_analysis = self.finance_agent.analyze(context, creative_proposal)
        inventory_analysis = self.inventory_agent.analyze(context, creative_proposal)
        
        # Phase 2: Multi-round Negotiation
        final_plan = self.negotiate_campaign_plan(
            context, creative_proposal, finance_analysis, inventory_analysis
        )
        
        # Phase 3: Final Synthesis
        print("\n=== Phase 3: Final Campaign Plan ===")
        
        return {
            "campaign_strategy": final_plan["strategy"],
            "financial_projection": final_plan["finance"],
            "inventory_status": final_plan["inventory"],
            "collaboration_summary": final_plan["collaboration"],
            "agent_messages": [{
                "sender": msg.sender,
                "recipient": msg.recipient,
                "type": msg.message_type,
                "round": msg.round_number
            } for msg in self.message_history[-10:]],  # Last 10 messages
            "success_probability": final_plan["success_probability"],
            "recommended_next_steps": final_plan["next_steps"]
        }
    
    def negotiate_campaign_plan(self, context, creative_proposal, finance_analysis, inventory_analysis):
        """Multi-round negotiation between agents"""
        
        print("\n=== Phase 2: Multi-Agent Negotiation ===")
        
        current_plan = {
            "strategy": creative_proposal,
            "finance": finance_analysis,
            "inventory": inventory_analysis
        }
        
        for round_num in range(1, self.negotiation_rounds + 1):
            print(f"\n--- Negotiation Round {round_num} ---")
            
            # Finance agent reviews creative proposal
            if finance_analysis["approval"] == "rejected":
                finance_feedback = self.finance_agent.negotiate(
                    creative_proposal, context, round_num
                )
                
                # Send feedback message
                self.send_message(AgentMessage(
                    sender="Finance",
                    recipient="Creative",
                    message_type="constraint",
                    content=finance_feedback,
                    round_number=round_num
                ))
                
                # Creative agent adjusts based on finance constraints
                adjusted_creative = self.creative_agent.negotiate(
                    finance_feedback, context, round_num
                )
                current_plan["strategy"] = adjusted_creative
            
            # Inventory agent checks feasibility
            if inventory_analysis["availability"] == "limited":
                inventory_feedback = self.inventory_agent.negotiate(
                    current_plan["strategy"], context, round_num
                )
                
                self.send_message(AgentMessage(
                    sender="Inventory",
                    recipient="Creative",
                    message_type="constraint",
                    content=inventory_feedback,
                    round_number=round_num
                ))
                
                # Adjust strategy based on inventory constraints
                final_creative = self.creative_agent.negotiate(
                    inventory_feedback, context, round_num
                )
                current_plan["strategy"] = final_creative
        
        # Final validation
        final_finance = self.finance_agent.final_validation(current_plan["strategy"], context)
        final_inventory = self.inventory_agent.final_validation(current_plan["strategy"], context)
        
        # Calculate success probability based on agent consensus
        success_prob = self.calculate_success_probability(
            current_plan["strategy"], final_finance, final_inventory
        )
        
        return {
            "strategy": current_plan["strategy"],
            "finance": final_finance,
            "inventory": final_inventory,
            "collaboration": f"Completed {self.negotiation_rounds} rounds of negotiation with {len(self.message_history)} agent interactions",
            "success_probability": success_prob,
            "next_steps": self.generate_next_steps(current_plan, final_finance, final_inventory)
        }
    
    def calculate_success_probability(self, strategy, finance, inventory):
        """Calculate campaign success probability based on agent outputs"""
        base_probability = 0.60
        
        # Finance factor
        if finance["approval"] == "approved":
            base_probability += 0.20
        elif finance["approval"] == "conditional":
            base_probability += 0.10
        
        # Inventory factor
        if inventory["availability"] == "excellent":
            base_probability += 0.15
        elif inventory["availability"] == "good":
            base_probability += 0.10
        
        # Strategy quality factor (based on creative output length and detail)
        if len(strategy.get("content", "")) > 200:
            base_probability += 0.05
        
        return min(base_probability, 0.95)  # Cap at 95%
    
    def generate_next_steps(self, strategy, finance, inventory):
        """Generate actionable next steps based on agent analysis"""
        steps = []
        
        if finance["approval"] == "conditional":
            steps.append(f"Secure additional budget of ${finance.get('additional_budget_needed', 0):,.2f}")
        
        if inventory["availability"] == "limited":
            steps.append("Coordinate with supply chain for inventory replenishment")
        
        steps.extend([
            "Finalize creative assets and content",
            "Set up campaign tracking and analytics",
            "Schedule campaign launch and monitoring"
        ])
        
        return steps

# Legacy function for backward compatibility
def run_agents(query, product):
    """Legacy wrapper function"""
    coordinator = MultiAgentCoordinator()
    results = coordinator.run_coordinated_campaign(query, product)
    
    # Format for backward compatibility
    return {
        "Creative": results["campaign_strategy"].get("content", "Creative strategy generated"),
        "Finance": results["financial_projection"].get("summary", "Financial analysis completed"),
        "Inventory": results["inventory_status"].get("summary", "Inventory check completed"),
        "Final Plan": results["collaboration_summary"],
        "Success Probability": f"{results['success_probability']*100:.1f}%",
        "Detailed Results": results
    }