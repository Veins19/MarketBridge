import os
import json
from dotenv import load_dotenv
import google.generativeai as genai
from google.generativeai.generative_models import GenerativeModel

load_dotenv()

# Initialize Gemini
try:
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    GEMINI_AVAILABLE = True
    print("✅ Gemini AI configured for Finance Agent")
except Exception as e:
    GEMINI_AVAILABLE = False
    print(f"⚠️ Gemini AI not available: {e}")

def load_budget_data():
    """Load budget allocation data"""
    try:
        budget_file = os.path.join(os.path.dirname(__file__), 'budget.json')
        with open(budget_file, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Budget data error: {e}")
        return {
            "digital_advertising": {"percentage": 60, "channels": ["Google Ads", "Facebook", "Instagram"]},
            "content_creation": {"percentage": 25, "tools": ["Design", "Video", "Copywriting"]}, 
            "influencer_marketing": {"percentage": 15, "focus": "Micro-influencers"}
        }

def finance_agent(query, product):
    """Enhanced Finance Agent with AI-powered budget analysis"""
    
    budget_data = load_budget_data()
    
    # Estimate budget from query
    budget_amount = extract_budget_from_query(query)
    
    # Create allocation breakdown
    allocations = {}
    for category, details in budget_data.items():
        percentage = details["percentage"]
        amount = int(budget_amount * percentage / 100)
        allocations[category] = {
            "amount": amount,
            "percentage": percentage,
            "details": details
        }
    
    if GEMINI_AVAILABLE:
        try:
            model = GenerativeModel('gemini-1.5-flash-latest')
            
            prompt = f"""As a finance expert, analyze this marketing budget for {product}:
Budget: ${budget_amount:,}
Allocation: {json.dumps(allocations, indent=2)}

Provide a 3-4 sentence financial analysis covering:
1. Budget adequacy for the campaign goals
2. Allocation efficiency and recommendations  
3. Expected ROI and payback period
4. Risk factors and optimization opportunities

Be specific with numbers and actionable advice."""
            
            response = model.generate_content(prompt)
            ai_analysis = response.text.strip()
            
            # ADD: Format the output beautifully
            return format_finance_output(ai_analysis, budget_amount, allocations)
            
        except Exception as e:
            print(f"Gemini error in finance agent: {e}")
    
    # Fallback analysis
    fallback_analysis = generate_finance_fallback(budget_amount, allocations, product)
    return format_finance_output(fallback_analysis, budget_amount, allocations)

def extract_budget_from_query(query):
    """Extract budget amount from query"""
    query_lower = query.lower()
    if "1000-5000" in query_lower or "small" in query_lower:
        return 3000
    elif "5000-25000" in query_lower or "medium" in query_lower:
        return 15000
    elif "25000-100000" in query_lower or "large" in query_lower:
        return 62500
    elif "100000+" in query_lower or "enterprise" in query_lower:
        return 150000
    else:
        return 15000  # Default medium budget

def generate_finance_fallback(budget, allocations, product):
    """Generate fallback financial analysis"""
    roi_multiplier = 3.2 if budget >= 25000 else 2.8 if budget >= 5000 else 2.4
    expected_revenue = int(budget * roi_multiplier)
    payback_months = 3 if budget >= 50000 else 4
    
    return f"""Budget of ${budget:,} is well-suited for {product} campaign with balanced allocation across digital channels (60%), content creation (25%), and influencer partnerships (15%). Expected ROI of {roi_multiplier}x generating ${expected_revenue:,} in revenue with {payback_months}-month payback period. Recommend maintaining higher digital ad spend for immediate traction while scaling content investments based on early performance metrics."""

# ADD: New formatting function  
def format_finance_output(analysis, budget, allocations):
    """Format finance output for better readability"""
    
    # Calculate totals
    digital_amount = allocations.get('digital_advertising', {}).get('amount', 0)
    content_amount = allocations.get('content_creation', {}).get('amount', 0)
    influencer_amount = allocations.get('influencer_marketing', {}).get('amount', 0)
    
    roi_multiplier = 3.2 if budget >= 25000 else 2.8 if budget >= 5000 else 2.4
    expected_revenue = int(budget * roi_multiplier)
    
    formatted_output = f"""💰 **FINANCIAL ANALYSIS & BUDGET ALLOCATION**

📊 **Budget Breakdown (${budget:,} Total):**
• Digital Advertising: ${digital_amount:,} (60%) - Google Ads, Social Media
• Content Creation: ${content_amount:,} (25%) - Design, Video, Copy
• Influencer Marketing: ${influencer_amount:,} (15%) - Micro-influencer partnerships

🧮 **Financial Projections:**
{analysis}

📈 **ROI Forecast:**
• Expected Revenue: ${expected_revenue:,}
• ROI Multiplier: {roi_multiplier}x
• Break-even: 3-4 months
• Profit Margin: {int((roi_multiplier-1)*100)}% after costs

⚠️ **Risk Mitigation:**
• Start with 70% budget allocation
• Monitor CPA/ROAS weekly
• Reserve 30% for high-performing channels
• Implement spend caps and daily limits"""

    return formatted_output
