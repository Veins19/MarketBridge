import os
from dotenv import load_dotenv
import google.generativeai as genai # Import statement moved to the top
from google.generativeai.client import configure
from google.generativeai.generative_models import GenerativeModel


load_dotenv()
configure(api_key=os.getenv("GEMINI_API_KEY"))

def creative_agent(query, product):
    system_prompt = (
        "You are a creative marketing strategist AI agent. Your role is to generate "
        "concise, actionable marketing campaign ideas."
    )
    user_prompt = (
        f"Product: {product}\n"
        f"Campaign Description/Query: {query}\n"
        "In 5-7 sentences, give a concise, creative marketing campaign idea for this product. "
        "Include: 1) a campaign theme, 2) the main target audience, 3) one promotional tactic, and 4) one recommended marketing channel. "
        "Be brief and actionable."
    )
    try:
        model = GenerativeModel('gemini-2.5-pro')
        response = model.generate_content(f"{system_prompt}\n\n{user_prompt}")
        ai_suggestion = response.text.strip()
        return f"Creative Agent (Gemini): {ai_suggestion}"
    except Exception as e:
        return f"Creative Agent: Error generating Gemini response ({str(e)}). Fallback: Suggests a 15% discount campaign for '{product}' targeting young customers."
