import os
import json
from datetime import datetime, timedelta
from dotenv import load_dotenv
import google.generativeai as genai
from google.generativeai.generative_models import GenerativeModel

load_dotenv()

# Initialize Gemini AI (like other agents)
try:
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    GEMINI_AVAILABLE = True
    print("✅ Gemini AI configured for Inventory Agent")
except Exception as e:
    GEMINI_AVAILABLE = False
    print(f"⚠️ Gemini AI not available: {e}")

def load_inventory_data():
    """Load comprehensive inventory data from JSON file"""
    try:
        inventory_file = os.path.join(os.path.dirname(__file__), 'inventory.json')
        with open(inventory_file, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Inventory data error: {e}")
        # Enhanced fallback data
        return {
            "products": [
                {
                    "name": "Wireless Headphones",
                    "sku": "WH-2024-001",
                    "stock": 1200,
                    "reserved": 300,
                    "incoming": 500,
                    "lead_time": 14,
                    "category": "Electronics",
                    "cost": 45,
                    "retail_price": 89,
                    "seasonal_demand": {
                        "Q1": 0.8, "Q2": 1.0, "Q3": 1.1, "Q4": 1.4
                    },
                    "supplier": "TechAudio Corp",
                    "min_threshold": 200
                },
                {
                    "name": "Smart Watch", 
                    "sku": "SW-2024-002",
                    "stock": 800,
                    "reserved": 150,
                    "incoming": 300,
                    "lead_time": 21,
                    "category": "Wearables",
                    "cost": 78,
                    "retail_price": 149,
                    "seasonal_demand": {
                        "Q1": 0.9, "Q2": 1.2, "Q3": 1.0, "Q4": 1.3
                    },
                    "supplier": "SmartTech Ltd",
                    "min_threshold": 150
                },
                {
                    "name": "Bluetooth Speaker",
                    "sku": "BS-2024-003", 
                    "stock": 950,
                    "reserved": 180,
                    "incoming": 400,
                    "lead_time": 10,
                    "category": "Audio",
                    "cost": 32,
                    "retail_price": 69,
                    "seasonal_demand": {
                        "Q1": 0.7, "Q2": 1.3, "Q3": 1.2, "Q4": 1.5
                    },
                    "supplier": "AudioMax Inc",
                    "min_threshold": 300
                }
            ],
            "warehouses": [
                {"location": "West Coast", "capacity": 5000, "current": 3200},
                {"location": "East Coast", "capacity": 4500, "current": 2800},
                {"location": "Central", "capacity": 3000, "current": 1900}
            ],
            "supply_chain_status": {
                "overall_health": "Good",
                "average_lead_time": 15,
                "supplier_reliability": 0.94,
                "seasonal_forecast_accuracy": 0.87
            }
        }

def inventory_agent(query, product):
    """Enhanced AI-Powered Inventory Agent with intelligent analysis"""
    
    inventory_data = load_inventory_data()
    products = inventory_data.get("products", [])
    supply_chain = inventory_data.get("supply_chain_status", {})
    warehouses = inventory_data.get("warehouses", [])
    
    # Find matching product with fuzzy matching
    product_info = find_best_product_match(product, products)
    
    # Calculate advanced inventory metrics
    inventory_metrics = calculate_inventory_intelligence(product_info, query, supply_chain)
    
    # Get current quarter for seasonal analysis
    current_quarter = f"Q{(datetime.now().month - 1) // 3 + 1}"
    seasonal_multiplier = product_info.get("seasonal_demand", {}).get(current_quarter, 1.0)
    
    # Enhanced campaign demand estimation
    campaign_demand = estimate_intelligent_campaign_demand(query, product, seasonal_multiplier)
    
    if GEMINI_AVAILABLE:
        try:
            model = GenerativeModel('gemini-1.5-flash-latest')
            
            prompt = f"""As a supply chain expert, analyze this inventory situation:

Product: {product_info['name']} (SKU: {product_info.get('sku', 'N/A')})
Current Stock: {product_info['stock']} units
Available: {inventory_metrics['available']} units  
Reserved: {product_info.get('reserved', 0)} units
Incoming: {product_info.get('incoming', 0)} units (ETA: {inventory_metrics['incoming_date']})

Campaign: {query} for {product}
Estimated Demand: {campaign_demand} units
Current Quarter: {current_quarter} (seasonal multiplier: {seasonal_multiplier}x)
Lead Time: {product_info.get('lead_time', 14)} days
Supplier Reliability: {supply_chain.get('supplier_reliability', 0.94) * 100:.1f}%

Supply Chain Status: {supply_chain.get('overall_health', 'Good')}

Provide a 4-5 sentence strategic inventory analysis covering:
1. Stock adequacy for the campaign goals
2. Risk assessment and mitigation strategies
3. Seasonal considerations and demand patterns
4. Supplier coordination and reorder recommendations
5. Competitive advantages from inventory position

Be specific with numbers, timelines, and actionable supply chain insights."""
            
            response = model.generate_content(prompt)
            ai_analysis = response.text.strip()
            
            # Format with AI analysis
            return format_advanced_inventory_output(
                ai_analysis, product_info, inventory_metrics, 
                campaign_demand, supply_chain, warehouses, seasonal_multiplier
            )
            
        except Exception as e:
            print(f"Gemini error in inventory agent: {e}")
    
    # Smart fallback with enhanced logic
    fallback_analysis = generate_intelligent_inventory_analysis(
        product_info, inventory_metrics, campaign_demand, seasonal_multiplier
    )
    
    return format_advanced_inventory_output(
        fallback_analysis, product_info, inventory_metrics,
        campaign_demand, supply_chain, warehouses, seasonal_multiplier
    )

def find_best_product_match(product, products):
    """Advanced product matching with fuzzy logic"""
    product_lower = product.lower()
    
    # Direct name matching
    for item in products:
        if product_lower in item["name"].lower() or item["name"].lower() in product_lower:
            return item
    
    # Category-based matching
    category_mapping = {
        "headphones": "Electronics",
        "watch": "Wearables", 
        "speaker": "Audio",
        "audio": "Audio",
        "tech": "Electronics"
    }
    
    for keyword, category in category_mapping.items():
        if keyword in product_lower:
            for item in products:
                if item.get("category") == category:
                    return item
    
    # Enhanced default product
    return {
        "name": product,
        "sku": f"GEN-2024-{hash(product) % 1000:03d}",
        "stock": 850,
        "reserved": 200,
        "incoming": 400,
        "lead_time": 14,
        "category": "General",
        "cost": 50,
        "retail_price": 99,
        "seasonal_demand": {"Q1": 0.9, "Q2": 1.0, "Q3": 1.1, "Q4": 1.3},
        "supplier": "Premium Supply Co",
        "min_threshold": 200
    }

def calculate_inventory_intelligence(product_info, query, supply_chain):
    """Calculate advanced inventory metrics and intelligence"""
    available = product_info["stock"] - product_info.get("reserved", 0)
    incoming_date = datetime.now() + timedelta(days=product_info.get("lead_time", 14))
    
    # Calculate inventory turnover and velocity
    cost = product_info.get("cost", 50)
    retail_price = product_info.get("retail_price", 99)
    margin = ((retail_price - cost) / retail_price) * 100
    
    # Supply chain health score
    reliability = supply_chain.get("supplier_reliability", 0.94)
    lead_time = product_info.get("lead_time", 14)
    
    health_score = (reliability * 0.6) + ((21 - min(lead_time, 21)) / 21 * 0.4)
    
    return {
        "available": available,
        "incoming_date": incoming_date.strftime("%b %d"),
        "margin_percentage": margin,
        "supply_chain_health": health_score,
        "turnover_potential": available / 30,  # units per day potential
        "stock_value": available * cost
    }

def estimate_intelligent_campaign_demand(query, product, seasonal_multiplier):
    """AI-enhanced demand estimation with multiple factors"""
    base_demand = 200  # Default baseline
    
    # Campaign type multipliers
    query_lower = query.lower()
    if "launch" in query_lower:
        base_demand = 350
    elif "seasonal" in query_lower or "sale" in query_lower:
        base_demand = 450
    elif "awareness" in query_lower or "brand" in query_lower:
        base_demand = 150
    elif "retention" in query_lower:
        base_demand = 180
    elif "lead generation" in query_lower:
        base_demand = 220
    
    # Product category adjustments
    product_lower = product.lower()
    if "headphones" in product_lower or "audio" in product_lower:
        base_demand *= 1.2  # High demand category
    elif "watch" in product_lower or "wearable" in product_lower:
        base_demand *= 1.1
    elif "speaker" in product_lower:
        base_demand *= 1.3  # Very popular
    
    # Apply seasonal multiplier
    final_demand = int(base_demand * seasonal_multiplier)
    
    return final_demand

def generate_intelligent_inventory_analysis(product_info, metrics, demand, seasonal_multiplier):
    """Generate smart fallback analysis"""
    available = metrics["available"]
    health_score = metrics["supply_chain_health"]
    
    if available >= demand * 1.5:
        adequacy = "Excellent - inventory levels support aggressive scaling"
    elif available >= demand * 1.2:
        adequacy = "Strong - adequate buffer for demand fluctuations"
    elif available >= demand:
        adequacy = "Adequate - meets projected demand with monitoring needed"
    else:
        adequacy = "Risk - insufficient inventory may constrain campaign performance"
    
    supplier_status = "highly reliable" if health_score > 0.9 else "reliable" if health_score > 0.8 else "requires attention"
    
    return f"""Inventory analysis shows {adequacy.lower()} with {available:
} units available against an estimated demand of {demand} units for the campaign. Seasonal factors (multiplier: {seasonal_multiplier}x) have been considered in demand projections. The supply chain is currently {supplier_status}, with a health score of {health_score:.2f}. It is recommended to coordinate closely with {product_info.get('supplier', 'the supplier')} to ensure timely replenishments and consider pre-emptive reordering if demand surges beyond estimates."""