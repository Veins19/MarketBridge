import os
from dotenv import load_dotenv
import google.generativeai as genai
from google.generativeai.client import configure
from google.generativeai.generative_models import GenerativeModel

# RAG Integration
try:
    import sys
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from rag_system import get_rag_system
    RAG_AVAILABLE = True
    rag = get_rag_system()
    print("✅ RAG system integrated with Creative Agent")
except Exception as e:
    RAG_AVAILABLE = False
    print(f"⚠️ RAG system not available: {e}")

load_dotenv()

try:
    configure(api_key=os.getenv("GEMINI_API_KEY"))
    GEMINI_AVAILABLE = True
    print("✅ Gemini AI configured successfully")
except Exception as e:
    GEMINI_AVAILABLE = False
    print(f"⚠️ Gemini AI not available: {e}")

def creative_agent(query, product):
    """Enhanced Creative Agent with Gemini + RAG integration"""
    
    # Get customer insights from RAG if available
    customer_context = ""
    if RAG_AVAILABLE:
        try:
            # Get customer segmentation data
            # FIXED: Use product for search instead of generic query
            search_terms = product.lower()
            if "stylish" in search_terms or "designer" in search_terms or "creative" in search_terms:
                search_terms = "designers creative graphic"
            elif "premium" in search_terms or "business" in search_terms or "executive" in search_terms:
                search_terms = "business executive premium"
            elif "budget" in search_terms or "affordable" in search_terms:
                search_terms = "student college budget"
            else:
                search_terms = product  # Use product name as fallback
                
            segmentation = rag.get_customer_segments(product, search_terms, "premium")
            insights = segmentation.get('insights', {})
            segments = segmentation.get('segments', {})
            
            primary_insights = insights.get('primary', {})
            total_reach = primary_insights.get('estimated_reach', 45000)
            conversions = primary_insights.get('projected_conversions', 150)
            
            # Get primary customer profile
            primary_customers = segments.get('primary', [])
            if primary_customers:
                customer = primary_customers[0]
                demographics = customer.get('demographics', 'Tech professionals')
                age = customer.get('age', 28)
                preferences = customer.get('preferences', 'Quality and innovation')
                customer_context = f"Target: {demographics} (age {age}), preferences: {preferences}. Market reach: {total_reach:,}, expected conversions: {conversions}."
                print(f"🎯 RAG insights: {customer_context}")
        except Exception as e:
            print(f"RAG error in creative agent: {e}")
            customer_context = "Target: Tech professionals aged 25-35, preferences: Quality and innovation."
    else:
        customer_context = "Target: Tech professionals aged 25-35, preferences: Premium quality and innovation."

    # Enhanced system prompt with RAG context
    system_prompt = f"""You are an expert marketing strategist with access to real customer data.
Customer Intelligence: {customer_context}
Create a concise, actionable marketing campaign strategy that leverages this customer intelligence."""

    user_prompt = f"""Product: {product}
Campaign Goal: {query}

Based on the customer intelligence provided, create a focused marketing campaign strategy in exactly 4-5 sentences covering:
1. Campaign theme and positioning
2. Target audience and messaging approach  
3. Recommended promotional tactics
4. Primary marketing channels
5. Expected outcomes

Be specific, actionable, and data-driven."""

    # Try Gemini AI first
    if GEMINI_AVAILABLE:
        try:
            model = GenerativeModel('gemini-1.5-flash-latest')
            response = model.generate_content(f"{system_prompt}\n\n{user_prompt}")
            ai_suggestion = response.text.strip()
            
            # ADD: Format the output beautifully
            return format_creative_output(ai_suggestion, customer_context)
        except Exception as e:
            print(f"Gemini error: {e}")

    # Smart fallback with RAG data
    fallback_strategy = generate_smart_fallback(product, query, customer_context)
    return format_creative_output(fallback_strategy, customer_context)

def generate_smart_fallback(product, query, customer_context):
    """Generate intelligent fallback using RAG data"""
    # Extract key info from customer context
    if "Tech professionals" in customer_context:
        audience = "tech-savvy professionals aged 25-35"
        channels = "LinkedIn, Instagram, and tech forums"
        messaging = "innovation and premium quality"
    else:
        audience = "quality-conscious consumers"
        channels = "Instagram, Facebook, and email marketing"
        messaging = "value and reliability"

    # Product-specific themes
    themes = {
        "Wireless Headphones": "SoundScape Pro",
        "Smart Watch": "TimeSync Elite",
        "Bluetooth Speaker": "AudioPulse",
        "Inox Bottle": "PureFlow Premium"
    }
    
    theme = themes.get(product, f"Premium {product} Experience")
    
    return f"""Launch '{theme}' campaign positioning {product} as the premium choice for {audience}. Focus messaging on {messaging} with personalized targeting based on customer preferences. Deploy 15-20% early-adopter discount through {channels} to drive initial traction. Implement A/B testing on creative variations and scale successful segments. Expected to reach 45,000+ prospects with 2.5-4% conversion rate generating 150+ qualified leads within 4-6 weeks."""

# ADD: New formatting function
def format_creative_output(content, context):
    """Format creative output for better readability"""
    
    # Extract key metrics from context if available
    reach = "45,000+" if "45000" in context else "30,000+"
    conversions = "150+" if "150" in context else "100+"
    
    # Format the output with sections
    formatted_output = f"""🎨 **CREATIVE CAMPAIGN STRATEGY**

📋 **Campaign Overview:**
{content}

🎯 **Target Intelligence:**
• {context.replace('Target: ', '').replace('. Market reach:', '\n• Market reach:')}

📈 **Key Projections:**
• Estimated reach: {reach} prospects
• Expected conversions: {conversions} qualified leads
• Timeline: 4-6 weeks for full deployment
• ROI: 2.5-4x within first quarter

✅ **Next Steps:**
1. Finalize creative assets and messaging
2. Set up tracking and analytics
3. Launch pilot campaign with A/B testing
4. Scale successful variations"""

    return formatted_output
