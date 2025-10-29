"""
MarketBridge Enhanced Multi-Agent System
"""

# Import individual agent classes
from .enhanced_creative_agent import EnhancedCreativeAgent
from .enhanced_finance_agent import EnhancedFinanceAgent
from .enhanced_inventory_agent import EnhancedInventoryAgent
from .enhanced_agent_manager import EnhancedAgentManager

# Import the manager instance
from .enhanced_agent_manager import enhanced_agent_manager

# Export everything
__all__ = [
    'EnhancedCreativeAgent',
    'EnhancedFinanceAgent', 
    'EnhancedInventoryAgent',
    'EnhancedAgentManager',
    'enhanced_agent_manager'
]

__version__ = "2.0.0"
__description__ = "Enhanced Multi-Agent Marketing Campaign Planning System"
