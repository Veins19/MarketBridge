import os
from dotenv import load_dotenv
import google.generativeai as genai
from google.generativeai.client import configure
from google.generativeai.generative_models import GenerativeModel
from typing import Dict, Any, List
import json
import re

load_dotenv()
configure(api_key=os.getenv("GEMINI_API_KEY"))

class CreativeAgent:
    """Enhanced Creative Agent with coordination and negotiation capabilities"""
    
    def __init__(self):
        self.agent_name = "Creative"
        self.model = GenerativeModel('gemini-1.5-pro')
        self.negotiation_history = []
        
    def analyze(self, context) -> Dict[str, Any]:
        """Initial creative analysis based on campaign context"""
        print(f"🎨 {self.agent_name} Agent: Analyzing campaign requirements...")
        
        # Analyze customer segments for targeting
        target_segment = self._select_target_segment(context.customer_data)
        
        # Generate creative strategy using Gemini
        creative_strategy = self._generate_creative_strategy(
            context.query, context.product, target_segment, context.budget
        )
        
        # Extract key elements from strategy
        strategy_elements = self._parse_strategy_elements(creative_strategy)
        
        result = {
            "content": creative_strategy,
            "target_segment": target_segment,
            "strategy_elements": strategy_elements,
            "estimated_budget_needed": self._estimate_budget_requirement(strategy_elements),
            "campaign_duration": strategy_elements.get("duration", 30),
            "channels": strategy_elements.get("channels", ["Social Media", "Email"]),
            "creative_confidence": 0.85
        }
        
        print(f"✓ Target Segment: {target_segment['name']} ({target_segment['size']:,} customers)")
        print(f"✓ Estimated Budget Need: ${result['estimated_budget_needed']:,.2f}")
        
        return result
    
    def negotiate(self, feedback: Dict[str, Any], context, round_number: int) -> Dict[str, Any]:
        """Negotiate and adjust strategy based on other agents' feedback"""
        print(f"🤝 {self.agent_name} Agent: Negotiating (Round {round_number})...")
        
        self.negotiation_history.append({
            "round": round_number,
            "feedback_received": feedback,
            "context": context.product
        })
        
        # Adjust strategy based on feedback type
        if "budget_constraint" in feedback:
            adjusted_strategy = self._adjust_for_budget_constraint(
                feedback, context
            )
        elif "inventory_limitation" in feedback:
            adjusted_strategy = self._adjust_for_inventory_constraint(
                feedback, context
            )
        else:
            adjusted_strategy = self._general_strategy_adjustment(
                feedback, context
            )
        
        print(f"✓ Strategy adjusted based on {feedback.get('constraint_type', 'general')} constraints")
        
        return adjusted_strategy
    
    def _select_target_segment(self, customer_data: Dict) -> Dict[str, Any]:
        """Select optimal customer segment based on data"""
        segments = customer_data.get("segments", [])
        
        if not segments:
            return {
                "name": "General Audience",
                "size": 10000,
                "avg_spend": 800,
                "conversion_rate": 0.10
            }
        
        # Select segment with best revenue potential (size * avg_spend * conversion_rate)
        best_segment = max(segments, key=lambda s: 
            s["size"] * s["avg_spend"] * s["conversion_rate"]
        )
        
        return best_segment
    
    def _generate_creative_strategy(self, query: str, product: str, 
                                  target_segment: Dict, budget: float) -> str:
        """Generate creative strategy using Gemini AI"""
        
        system_prompt = (
            "You are a senior creative strategist AI agent specializing in data-driven "
            "marketing campaigns. You create strategies that balance creativity with "
            "business objectives and constraints."
        )
        
        user_prompt = f"""
Campaign Brief:
- Product: {product}
- Campaign Query: {query}
- Target Segment: {target_segment['name']} ({target_segment['size']:,} customers)
- Segment Profile: Avg Spend ${target_segment['avg_spend']}, Conversion Rate {target_segment['conversion_rate']:.1%}
- Available Budget: ${budget:,.2f}

Create a comprehensive marketing campaign strategy that includes:
1. **Campaign Theme** - A compelling central message
2. **Value Proposition** - Key benefits for the target segment
3. **Creative Approach** - Specific creative tactics and messaging
4. **Channel Strategy** - Recommended marketing channels with rationale
5. **Budget Allocation** - Suggested spend distribution across channels
6. **Timeline** - Campaign duration and key milestones
7. **Success Metrics** - KPIs to measure campaign effectiveness

Format your response as a detailed but concise strategy (200-300 words).
"""
        
        try:
            response = self.model.generate_content(f"{system_prompt}\n\n{user_prompt}")
            return response.text.strip()
        except Exception as e:
            print(f"Warning: Gemini API error ({str(e)}). Using fallback strategy.")
            return self._fallback_creative_strategy(product, target_segment, budget)
    
    def _fallback_creative_strategy(self, product: str, target_segment: Dict, budget: float) -> str:
        """Fallback strategy when Gemini API is unavailable"""
        return f"""
**Campaign Theme:** "Smart Choice for {target_segment['name']}"

**Value Proposition:** {product} offers exceptional value and innovation perfect for {target_segment['name']} who value quality and smart purchasing decisions.

**Creative Approach:** Develop authentic testimonials and user-generated content showcasing real {target_segment['name']} using {product} in their daily lives. Focus on practical benefits and lifestyle enhancement.

**Channel Strategy:** 
- Social Media (60%): Instagram and LinkedIn for visual storytelling
- Email Marketing (25%): Personalized campaigns for the {target_segment['name']} segment
- Search Ads (15%): Target high-intent keywords

**Budget Allocation:** ${budget*.6:,.0f} social, ${budget*.25:,.0f} email, ${budget*.15:,.0f} search ads

**Timeline:** 30-day campaign with weekly content themes and performance optimization

**Success Metrics:** {target_segment['conversion_rate']*100:.1f}% conversion rate target, ${target_segment['avg_spend']:.0f} average order value, 15% brand awareness lift
"""
    
    def _parse_strategy_elements(self, strategy: str) -> Dict[str, Any]:
        """Extract key elements from strategy text"""
        elements = {
            "channels": [],
            "duration": 30,
            "budget_split": {}
        }
        
        # Extract channels
        channel_patterns = [
            r'social media|instagram|facebook|twitter|linkedin',
            r'email|newsletter',
            r'search|google ads|ppc',
            r'display|banner',
            r'influencer|partnership'
        ]
        
        strategy_lower = strategy.lower()
        for pattern in channel_patterns:
            if re.search(pattern, strategy_lower):
                if 'social' in pattern:
                    elements["channels"].append("Social Media")
                elif 'email' in pattern:
                    elements["channels"].append("Email")
                elif 'search' in pattern:
                    elements["channels"].append("Search Ads")
                elif 'display' in pattern:
                    elements["channels"].append("Display Ads")
                elif 'influencer' in pattern:
                    elements["channels"].append("Influencer")
        
        # Default channels if none found
        if not elements["channels"]:
            elements["channels"] = ["Social Media", "Email"]
        
        # Extract duration
        duration_match = re.search(r'(\d+)[- ]day', strategy_lower)
        if duration_match:
            elements["duration"] = int(duration_match.group(1))
        
        return elements
    
    def _estimate_budget_requirement(self, strategy_elements: Dict) -> float:
        """Estimate budget needed based on strategy elements"""
        channel_costs = {
            "Social Media": 15000,
            "Email": 5000,
            "Search Ads": 20000,
            "Display Ads": 12000,
            "Influencer": 25000
        }
        
        total_cost = 0
        for channel in strategy_elements.get("channels", []):
            total_cost += channel_costs.get(channel, 10000)
        
        # Duration multiplier
        duration = strategy_elements.get("duration", 30)
        duration_multiplier = min(duration / 30, 2.0)  # Cap at 2x for long campaigns
        
        return total_cost * duration_multiplier
    
    def _adjust_for_budget_constraint(self, feedback: Dict, context) -> Dict[str, Any]:
        """Adjust strategy for budget constraints"""
        max_budget = feedback.get("max_budget", context.budget * 0.8)
        
        adjustment_prompt = f"""
Original campaign needs budget adjustment due to financial constraints.

Constraint: Maximum budget available is ${max_budget:,.2f}
Product: {context.product}

Provide a revised cost-effective strategy that:
1. Reduces budget requirements by focusing on high-ROI channels
2. Maintains campaign effectiveness
3. Suggests creative cost-saving measures
4. Prioritizes organic and earned media opportunities

Provide a concise revised strategy (150-200 words).
"""
        
        try:
            response = self.model.generate_content(adjustment_prompt)
            adjusted_content = response.text.strip()
        except Exception as e:
            adjusted_content = f"""
**Budget-Optimized Strategy for {context.product}:**

Focus on cost-effective channels: Email marketing (40% of budget) for direct customer engagement, organic social media content (30%) with user-generated content campaigns, and targeted search ads (30%) for high-intent customers.

**Cost-Saving Measures:**
- Partner with micro-influencers for product exchanges
- Leverage customer testimonials for authentic content
- Use automated email sequences to reduce manual costs
- Focus on 2-3 high-performing channels instead of broad approach

**Timeline:** 21-day focused campaign with weekly optimization
**Expected Results:** Maintain 80% of original campaign effectiveness while reducing budget by {((context.budget - max_budget) / context.budget * 100):.0f}%
"""
        
        return {
            "content": adjusted_content,
            "estimated_budget_needed": max_budget,
            "adjustment_type": "budget_constraint",
            "compromise_level": "moderate"
        }
    
    def _adjust_for_inventory_constraint(self, feedback: Dict, context) -> Dict[str, Any]:
        """Adjust strategy for inventory limitations"""
        available_stock = feedback.get("available_stock", 0)
        regions = feedback.get("available_regions", ["Online"])
        
        adjustment_prompt = f"""
Campaign strategy needs adjustment due to inventory constraints.

Product: {context.product}
Available Stock: {available_stock} units
Available Regions: {', '.join(regions)}

Revise the strategy to:
1. Focus on regions with available inventory
2. Adjust campaign scale to match stock levels
3. Include pre-order or waitlist strategies if appropriate
4. Suggest inventory-conscious messaging

Provide revised strategy (150-200 words).
"""
        
        try:
            response = self.model.generate_content(adjustment_prompt)
            adjusted_content = response.text.strip()
        except Exception as e:
            adjusted_content = f"""
**Inventory-Adjusted Strategy for {context.product}:**

Limit campaign to {', '.join(regions)} region(s) with {available_stock} units available. 

**Scarcity Marketing Approach:**
- "Limited Stock Available" messaging to create urgency
- Geo-targeted campaigns only in regions with inventory
- Pre-order campaigns for out-of-stock regions
- Email waitlist for future restocking notifications

**Channel Adjustment:**
- Precise geo-targeting on all digital channels
- Reduced campaign spend to match available inventory
- Focus on high-conversion audiences first

**Timeline:** Accelerated 14-day campaign to move available inventory
**Inventory Buffer:** Reserve 10% stock for service/returns
"""
        
        return {
            "content": adjusted_content,
            "estimated_budget_needed": context.budget * 0.6,  # Reduced scope
            "adjustment_type": "inventory_constraint",
            "target_regions": regions,
            "max_reach": available_stock * 10  # Assume 10% conversion
        }
    
    def _general_strategy_adjustment(self, feedback: Dict, context) -> Dict[str, Any]:
        """General strategy adjustments based on feedback"""
        return {
            "content": f"Adjusted strategy for {context.product} based on cross-agent feedback and constraints.",
            "estimated_budget_needed": context.budget * 0.9,
            "adjustment_type": "general_optimization"
        }

# Legacy function for backward compatibility
def creative_agent(query, product):
    """Legacy function wrapper"""
    agent = CreativeAgent()
    
    # Create minimal context for legacy support
    class MinimalContext:
        def __init__(self, query, product):
            self.query = query
            self.product = product
            self.budget = 50000
            self.customer_data = {
                "segments": [
                    {"name": "Target Audience", "size": 15000, "avg_spend": 800, "conversion_rate": 0.12}
                ]
            }
    
    context = MinimalContext(query, product)
    result = agent.analyze(context)
    
    return f"Creative Agent (Enhanced): {result['content'][:200]}... [Target: {result['target_segment']['name']}]"