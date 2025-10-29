"""
Services module for MarketBridge
Contains business logic services including What-If scenario engine
"""

from .whatif_engine import whatif_engine

__all__ = ['whatif_engine']
