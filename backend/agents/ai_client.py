"""
Shared AI client module for agent collaboration using Google's Gemini Pro model.
"""

import os
from dotenv import load_dotenv
import google.generativeai as genai
from google.generativeai.client import configure
from google.generativeai.generative_models import GenerativeModel

load_dotenv()
configure(api_key=os.getenv("GEMINI_API_KEY"))

class GeminiAIClient:
    def __init__(self):
        self.model = GenerativeModel('gemini-2.0-flash')
    
    async def generate_response(self, system_prompt: str, user_prompt: str) -> str:
        """Generate response using Gemini model with proper error handling"""
        try:
            response = self.model.generate_content(f"{system_prompt}\n\n{user_prompt}")
            return response.text.strip()
        except Exception as e:
            raise Exception(f"Gemini AI generation failed: {str(e)}")

# Global instance for reuse
gemini_client = GeminiAIClient()