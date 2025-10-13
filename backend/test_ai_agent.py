from agents.creative_agent import creative_agent
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_creative_agent():
    """Test the AI-powered creative agent"""
    
    # Test queries
    test_queries = [
        "smartphone accessories",
        "eco-friendly water bottles", 
        "premium coffee beans",
        "fitness tracking app"
    ]
    
    print("🤖 Testing AI-Powered Creative Agent")
    print("=" * 50)
    
    for query in test_queries:
        print(f"\n📝 Query: {query}")
        print("-" * 30)
        
        try:
            result = creative_agent(query, query) # Assuming product is the same as query for testing purposes
            print(f"🎯 Response: {result}")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print("\n✅ Test completed!")

if __name__ == "__main__":
    test_creative_agent()
