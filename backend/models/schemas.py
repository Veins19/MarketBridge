"""
SQLAlchemy ORM models for MarketBridge.

Tables:
- customers: Customer profiles and segmentation data
- products: Product catalog with pricing and inventory info
- campaigns: Campaign records and performance data
- campaign_results: Results from agent collaborations
- what_if_scenarios: Saved scenario simulations
"""

from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import Integer, String, Float, Text, DateTime, Boolean, JSON, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql.functions import func
from datetime import datetime
from enum import Enum
import uuid
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class CustomerSegment(str, Enum):
    """Customer segmentation categories"""
    HIGH_VALUE = "high_value"
    MEDIUM_VALUE = "medium_value" 
    LOW_VALUE = "low_value"
    NEW_CUSTOMER = "new_customer"
    RETURNING = "returning"
    CHURNED = "churned"


class CampaignStatus(str, Enum):
    """Campaign status options"""
    DRAFT = "draft"
    PLANNING = "planning"
    APPROVED = "approved" 
    ACTIVE = "active"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class Customer(Base):
    """Customer profiles and behavioral data"""
    __tablename__ = "customers"
    
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(String(50), unique=True, index=True, nullable=False)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True)
    segment = Column(SQLEnum(CustomerSegment), default=CustomerSegment.NEW_CUSTOMER)
    
    # Financial data
    lifetime_value = Column(Float, default=0.0)
    average_order_value = Column(Float, default=0.0)
    total_orders = Column(Integer, default=0)
    
    # Behavioral data
    last_purchase_date = Column(DateTime)
    preferred_channels = Column(JSON, default=list)  # ["email", "social", "sms"]
    product_preferences = Column(JSON, default=list)  # ["electronics", "fashion"]
    
    # Demographics (optional)
    age_group = Column(String(20))  # "18-25", "26-35", etc.
    location = Column(String(100))
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    campaigns = relationship("Campaign", back_populates="target_customers")


class Product(Base):
    """Product catalog with inventory and pricing"""
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(String(50), unique=True, index=True, nullable=False)
    name = Column(String(200), nullable=False)
    category = Column(String(100), nullable=False)
    description = Column(Text)
    
    # Pricing
    base_price = Column(Float, nullable=False)
    cost_price = Column(Float, nullable=False)  # For margin calculations
    current_discount = Column(Float, default=0.0)  # Current discount %
    
    # Inventory
    stock_quantity = Column(Integer, default=0)
    stock_regions = Column(JSON, default=dict)  # {"north": 100, "south": 50}
    reorder_level = Column(Integer, default=10)
    
    # Metadata
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    campaigns = relationship("Campaign", back_populates="product")


class Campaign(Base):
    """Marketing campaigns and their configurations"""
    __tablename__ = "campaigns"
    
    id = Column(Integer, primary_key=True, index=True)
    campaign_id = Column(String(50), unique=True, index=True, default=lambda: str(uuid.uuid4())[:8])
    
    # Basic info
    name = Column(String(200), nullable=False)
    description = Column(Text)
    campaign_type = Column(String(50))  # "product_launch", "seasonal_sale", etc.
    status = Column(SQLEnum(CampaignStatus), default=CampaignStatus.DRAFT)
    
    # Foreign keys
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    
    # Campaign parameters
    target_audience_size = Column(Integer, default=10000)
    discount_rate = Column(Float, default=10.0)  # Percentage
    budget = Column(Float, nullable=False)
    duration_days = Column(Integer, default=30)
    
    # Targeting
    target_segments = Column(JSON, default=list)  # Customer segments to target
    target_channels = Column(JSON, default=list)  # Marketing channels
    target_regions = Column(JSON, default=list)  # Geographic targeting
    
    # Timeline
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    
    # Metadata
    created_by = Column(String(100))  # User who created campaign
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    product = relationship("Product", back_populates="campaigns")
    target_customers = relationship("Customer", back_populates="campaigns")
    results = relationship("CampaignResult", back_populates="campaign")
    scenarios = relationship("WhatIfScenario", back_populates="campaign")


class CampaignResult(Base):
    """Results from agent analysis and campaign execution"""
    __tablename__ = "campaign_results"
    
    id = Column(Integer, primary_key=True, index=True)
    campaign_id = Column(Integer, ForeignKey("campaigns.id"), nullable=False)
    
    # Agent outputs
    creative_output = Column(JSON)  # Creative agent's strategy
    finance_output = Column(JSON)   # Finance agent's analysis  
    inventory_output = Column(JSON) # Inventory agent's assessment
    final_recommendation = Column(JSON)  # Orchestrated final plan
    
    # Projected metrics
    projected_roi = Column(Float)
    projected_revenue = Column(Float)
    projected_customers = Column(Integer)
    risk_score = Column(String(20))  # "Low", "Medium", "High"
    success_probability = Column(Float)  # 0.0 to 1.0
    
    # Agent reasoning (for explainability)
    agent_reasoning = Column(JSON)  # Detailed reasoning from each agent
    negotiation_rounds = Column(Integer, default=0)
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    campaign = relationship("Campaign", back_populates="results")


class WhatIfScenario(Base):
    """Saved What-If simulation scenarios"""
    __tablename__ = "what_if_scenarios"
    
    id = Column(Integer, primary_key=True, index=True)
    scenario_id = Column(String(50), unique=True, index=True, default=lambda: str(uuid.uuid4())[:8])
    campaign_id = Column(Integer, ForeignKey("campaigns.id"), nullable=False)
    
    # Scenario parameters
    scenario_name = Column(String(100), nullable=False)  # "Conservative", "Balanced", "Aggressive"
    scenario_description = Column(Text)
    
    # Input parameters
    input_discount_rate = Column(Float)
    input_target_size = Column(Integer)
    input_budget = Column(Float)
    input_duration = Column(Integer)
    
    # Simulation results
    projected_roi = Column(Float)
    projected_revenue = Column(Float) 
    success_probability = Column(Float)
    risk_assessment = Column(String(20))
    
    # Strategy details
    recommended_channels = Column(JSON, default=list)
    targeting_strategy = Column(Text)
    budget_allocation = Column(JSON, default=dict)
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    campaign = relationship("Campaign", back_populates="scenarios")


# Sample data creation helper
class SampleDataGenerator:
    """Helper class to create sample data for development"""
    
    @staticmethod
    def create_sample_customers():
        """Generate sample customer data"""
        return [
            {
                "customer_id": "CUST_001",
                "name": "John Smith", 
                "email": "john@example.com",
                "segment": CustomerSegment.HIGH_VALUE,
                "lifetime_value": 2500.0,
                "average_order_value": 150.0,
                "total_orders": 17,
                "preferred_channels": ["email", "social"],
                "product_preferences": ["electronics", "gadgets"],
                "age_group": "25-35",
                "location": "Mumbai"
            },
            {
                "customer_id": "CUST_002", 
                "name": "Sarah Johnson",
                "email": "sarah@example.com",
                "segment": CustomerSegment.MEDIUM_VALUE,
                "lifetime_value": 800.0,
                "average_order_value": 80.0,
                "total_orders": 10,
                "preferred_channels": ["email", "sms"],
                "product_preferences": ["fashion", "accessories"],
                "age_group": "18-25",
                "location": "Delhi"
            },
            {
                "customer_id": "CUST_003",
                "name": "Mike Chen", 
                "email": "mike@example.com",
                "segment": CustomerSegment.NEW_CUSTOMER,
                "lifetime_value": 0.0,
                "average_order_value": 0.0,
                "total_orders": 0,
                "preferred_channels": ["social", "web"],
                "product_preferences": ["electronics"],
                "age_group": "26-35", 
                "location": "Bangalore"
            }
        ]
    
    @staticmethod
    def create_sample_products():
        """Generate sample product data"""
        return [
            {
                "product_id": "PROD_001",
                "name": "Wireless Bluetooth Headphones",
                "category": "Electronics",
                "description": "Premium noise-cancelling wireless headphones",
                "base_price": 299.99,
                "cost_price": 120.0,
                "stock_quantity": 150,
                "stock_regions": {"north": 60, "south": 50, "west": 40},
                "reorder_level": 20
            },
            {
                "product_id": "PROD_002", 
                "name": "Smart Fitness Watch",
                "category": "Wearables",
                "description": "Advanced fitness tracking smartwatch",
                "base_price": 199.99,
                "cost_price": 80.0,
                "stock_quantity": 200,
                "stock_regions": {"north": 80, "south": 70, "west": 50},
                "reorder_level": 25
            }
        ]
