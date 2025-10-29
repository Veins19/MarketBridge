"""
Simple server runner for MarketBridge API.
This fixes import issues and provides better error reporting.
"""

import sys
import os
from pathlib import Path

# Add the current directory to Python path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

try:
    print("🔍 Testing imports...")
    
    # Test database helper import
    try:
        from models.db_helper import get_dashboard_stats
        print("✅ Database helper imported successfully")
        
        # Test database connectivity
        stats = get_dashboard_stats()
        print(f"✅ Database connected - {stats['customers']['total']} customers found")
        
    except Exception as e:
        print(f"❌ Database import error: {e}")
        sys.exit(1)
    
    # Test FastAPI import
    try:
        import uvicorn
        from fastapi import FastAPI
        print("✅ FastAPI imported successfully")
    except Exception as e:
        print(f"❌ FastAPI import error: {e}")
        sys.exit(1)
    
    # Import main app
    print("🚀 Starting MarketBridge API Server...")
    from main import app
    
    print("📊 Database: SQLite with sample data")
    print("🤖 Agents: Basic system (enhancing next)")  
    print("🌐 API Docs: http://localhost:8000/docs")
    print("🏠 Dashboard: http://localhost:8000/dashboard")
    
    # Start server
    uvicorn.run(
        "main:app",  # Use import string to fix reload warning
        host="0.0.0.0", 
        port=8000, 
        reload=True,
        reload_dirs=[str(current_dir)]
    )
    
except KeyboardInterrupt:
    print("\n👋 Server stopped by user")
except Exception as e:
    print(f"❌ Server startup error: {e}")
    print("\n🔧 Troubleshooting:")
    print("1. Make sure you're in the backend directory")
    print("2. Check that database was initialized: python -m models.init_db stats")
    print("3. Verify all dependencies are installed")
    sys.exit(1)
