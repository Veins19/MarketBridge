"""
Database helper functions for MarketBridge - Fixed version.

Fixed parameter issues with get_campaigns function.
"""

import sqlite3
import json
from pathlib import Path
from typing import List, Dict, Optional, Any
from datetime import datetime


class DatabaseHelper:
    """Helper class for database operations"""
    
    def __init__(self):
        self.db_path = Path(__file__).parent.parent / "marketbridge.db"
    
    def get_connection(self) -> sqlite3.Connection:
        """Get database connection with proper settings"""
        conn = sqlite3.connect(str(self.db_path))
        conn.row_factory = sqlite3.Row  # Return rows as dictionaries
        return conn
    
    def execute_query(self, query: str, params: tuple = ()) -> List[Dict]:
        """Execute a SELECT query and return results as list of dictionaries"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
    
    def execute_update(self, query: str, params: tuple = ()) -> int:
        """Execute INSERT/UPDATE/DELETE and return affected rows"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            return cursor.rowcount
    
    # Customer operations
    def get_customers(self, segment: Optional[str] = None, limit: int = 100) -> List[Dict]:
        """Get customers, optionally filtered by segment"""
        query = "SELECT * FROM customers"
        params = ()
        
        if segment:
            query += " WHERE segment = ?"
            params = (segment,)
        
        query += " ORDER BY lifetime_value DESC LIMIT ?"
        params = params + (limit,)
        
        customers = self.execute_query(query, params)
        
        # Parse JSON fields
        for customer in customers:
            if customer['preferred_channels']:
                try:
                    customer['preferred_channels'] = json.loads(customer['preferred_channels'])
                except:
                    customer['preferred_channels'] = []
            if customer['product_preferences']:
                try:
                    customer['product_preferences'] = json.loads(customer['product_preferences'])
                except:
                    customer['product_preferences'] = []
        
        return customers
    
    def get_customer_by_id(self, customer_id: str) -> Optional[Dict]:
        """Get customer by customer_id"""
        customers = self.execute_query(
            "SELECT * FROM customers WHERE customer_id = ?", 
            (customer_id,)
        )
        return customers[0] if customers else None
    
    # Product operations
    def get_products(self, category: Optional[str] = None, active_only: bool = True) -> List[Dict]:
        """Get products, optionally filtered by category"""
        query = "SELECT * FROM products"
        params = ()
        
        conditions = []
        if category:
            conditions.append("category = ?")
            params = params + (category,)
        if active_only:
            conditions.append("is_active = 1")
        
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        
        query += " ORDER BY name"
        
        products = self.execute_query(query, params)
        
        # Parse JSON fields
        for product in products:
            if product['stock_regions']:
                try:
                    product['stock_regions'] = json.loads(product['stock_regions'])
                except:
                    product['stock_regions'] = {}
        
        return products
    
    def get_product_by_id(self, product_id: str) -> Optional[Dict]:
        """Get product by product_id"""
        products = self.execute_query(
            "SELECT * FROM products WHERE product_id = ?", 
            (product_id,)
        )
        if products:
            product = products[0]
            if product['stock_regions']:
                try:
                    product['stock_regions'] = json.loads(product['stock_regions'])
                except:
                    product['stock_regions'] = {}
            return product
        return None
    
    # Campaign operations - FIXED FUNCTION
    def get_campaigns(self, status: Optional[str] = None, **kwargs) -> List[Dict]:
        """Get campaigns, optionally filtered by status. Accepts any additional parameters."""
        # Extract limit from kwargs, default to 50
        limit = kwargs.get('limit', 50)
        
        query = """
            SELECT c.*, p.name as product_name, p.category as product_category
            FROM campaigns c 
            JOIN products p ON c.product_id = p.id
        """
        params = ()
        
        if status:
            query += " WHERE c.status = ?"
            params = (status,)
        
        query += " ORDER BY c.created_at DESC LIMIT ?"
        params = params + (limit,)
        
        campaigns = self.execute_query(query, params)
        
        # Parse JSON fields
        for campaign in campaigns:
            for field in ['target_segments', 'target_channels', 'target_regions']:
                if campaign[field]:
                    try:
                        campaign[field] = json.loads(campaign[field])
                    except:
                        campaign[field] = []
        
        return campaigns
    
    def get_campaign_by_id(self, campaign_id: str) -> Optional[Dict]:
        """Get campaign by campaign_id with product details"""
        campaigns = self.execute_query("""
            SELECT c.*, p.name as product_name, p.category as product_category,
                   p.base_price, p.cost_price, p.stock_quantity
            FROM campaigns c 
            JOIN products p ON c.product_id = p.id
            WHERE c.campaign_id = ?
        """, (campaign_id,))
        
        if campaigns:
            campaign = campaigns[0]
            # Parse JSON fields
            for field in ['target_segments', 'target_channels', 'target_regions']:
                if campaign[field]:
                    try:
                        campaign[field] = json.loads(campaign[field])
                    except:
                        campaign[field] = []
            return campaign
        return None
    
    def create_campaign(self, campaign_data: Dict) -> str:
        """Create a new campaign and return campaign_id"""
        import uuid
        campaign_id = f"CAMP_{str(uuid.uuid4())[:8].upper()}"
        
        query = """
            INSERT INTO campaigns (campaign_id, name, description, campaign_type, status,
                                 product_id, target_audience_size, discount_rate, budget,
                                 duration_days, target_segments, target_channels, target_regions,
                                 created_by)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        
        params = (
            campaign_id,
            campaign_data.get('name'),
            campaign_data.get('description'),
            campaign_data.get('campaign_type'),
            campaign_data.get('status', 'draft'),
            campaign_data.get('product_id'),
            campaign_data.get('target_audience_size', 10000),
            campaign_data.get('discount_rate', 10.0),
            campaign_data.get('budget'),
            campaign_data.get('duration_days', 30),
            json.dumps(campaign_data.get('target_segments', [])),
            json.dumps(campaign_data.get('target_channels', [])),
            json.dumps(campaign_data.get('target_regions', [])),
            campaign_data.get('created_by', 'system')
        )
        
        self.execute_update(query, params)
        return campaign_id
    
    # Campaign results operations
    def get_campaign_results(self, campaign_id: str) -> List[Dict]:
        """Get results for a specific campaign"""
        results = self.execute_query("""
            SELECT cr.*, c.name as campaign_name
            FROM campaign_results cr
            JOIN campaigns c ON cr.campaign_id = c.id
            WHERE c.campaign_id = ?
            ORDER BY cr.created_at DESC
        """, (campaign_id,))
        
        # Parse JSON fields
        for result in results:
            json_fields = ['creative_output', 'finance_output', 'inventory_output', 
                          'final_recommendation', 'agent_reasoning']
            for field in json_fields:
                if result[field]:
                    try:
                        result[field] = json.loads(result[field])
                    except:
                        result[field] = {}
        
        return results
    
    def save_campaign_result(self, campaign_id: str, result_data: Dict) -> int:
        """Save campaign analysis results"""
        # Get campaign's database ID
        campaign = self.execute_query(
            "SELECT id FROM campaigns WHERE campaign_id = ?", 
            (campaign_id,)
        )
        if not campaign:
            raise ValueError(f"Campaign {campaign_id} not found")
        
        campaign_db_id = campaign[0]['id']
        
        query = """
            INSERT INTO campaign_results (
                campaign_id, creative_output, finance_output, inventory_output,
                final_recommendation, projected_roi, projected_revenue, 
                projected_customers, risk_score, success_probability,
                agent_reasoning, negotiation_rounds
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        
        params = (
            campaign_db_id,
            json.dumps(result_data.get('creative_output', {})),
            json.dumps(result_data.get('finance_output', {})),
            json.dumps(result_data.get('inventory_output', {})),
            json.dumps(result_data.get('final_recommendation', {})),
            result_data.get('projected_roi'),
            result_data.get('projected_revenue'),
            result_data.get('projected_customers'),
            result_data.get('risk_score'),
            result_data.get('success_probability'),
            json.dumps(result_data.get('agent_reasoning', {})),
            result_data.get('negotiation_rounds', 0)
        )
        
        return self.execute_update(query, params)
    
    # What-if scenarios operations
    def get_scenarios(self, campaign_id: str) -> List[Dict]:
        """Get what-if scenarios for a campaign"""
        scenarios = self.execute_query("""
            SELECT ws.*, c.name as campaign_name
            FROM what_if_scenarios ws
            JOIN campaigns c ON ws.campaign_id = c.id
            WHERE c.campaign_id = ?
            ORDER BY ws.created_at DESC
        """, (campaign_id,))
        
        # Parse JSON fields
        for scenario in scenarios:
            json_fields = ['recommended_channels', 'budget_allocation']
            for field in json_fields:
                if scenario[field]:
                    try:
                        scenario[field] = json.loads(scenario[field])
                    except:
                        scenario[field] = {}
        
        return scenarios
    
    def save_scenario(self, campaign_id: str, scenario_data: Dict) -> str:
        """Save a what-if scenario"""
        import uuid
        scenario_id = f"SCEN_{str(uuid.uuid4())[:8].upper()}"
        
        # Get campaign's database ID
        campaign = self.execute_query(
            "SELECT id FROM campaigns WHERE campaign_id = ?", 
            (campaign_id,)
        )
        if not campaign:
            raise ValueError(f"Campaign {campaign_id} not found")
        
        campaign_db_id = campaign[0]['id']
        
        query = """
            INSERT INTO what_if_scenarios (
                scenario_id, campaign_id, scenario_name, scenario_description,
                input_discount_rate, input_target_size, input_budget, input_duration,
                projected_roi, projected_revenue, success_probability, risk_assessment,
                recommended_channels, targeting_strategy, budget_allocation
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        
        params = (
            scenario_id, campaign_db_id,
            scenario_data.get('scenario_name'),
            scenario_data.get('scenario_description'),
            scenario_data.get('input_discount_rate'),
            scenario_data.get('input_target_size'),
            scenario_data.get('input_budget'),
            scenario_data.get('input_duration'),
            scenario_data.get('projected_roi'),
            scenario_data.get('projected_revenue'),
            scenario_data.get('success_probability'),
            scenario_data.get('risk_assessment'),
            json.dumps(scenario_data.get('recommended_channels', [])),
            scenario_data.get('targeting_strategy'),
            json.dumps(scenario_data.get('budget_allocation', {}))
        )
        
        self.execute_update(query, params)
        return scenario_id
    
    # Analytics and stats
    def get_dashboard_stats(self) -> Dict:
        """Get key statistics for dashboard"""
        stats = {}
        
        # Customer stats
        stats['customers'] = {
            'total': self.execute_query("SELECT COUNT(*) as count FROM customers")[0]['count'],
            'high_value': self.execute_query("SELECT COUNT(*) as count FROM customers WHERE segment = 'high_value'")[0]['count'],
            'new': self.execute_query("SELECT COUNT(*) as count FROM customers WHERE segment = 'new_customer'")[0]['count']
        }
        
        # Product stats
        stats['products'] = {
            'total': self.execute_query("SELECT COUNT(*) as count FROM products WHERE is_active = 1")[0]['count'],
            'low_stock': self.execute_query("SELECT COUNT(*) as count FROM products WHERE stock_quantity < reorder_level")[0]['count']
        }
        
        # Campaign stats
        stats['campaigns'] = {
            'total': self.execute_query("SELECT COUNT(*) as count FROM campaigns")[0]['count'],
            'active': self.execute_query("SELECT COUNT(*) as count FROM campaigns WHERE status IN ('approved', 'active')")[0]['count'],
            'draft': self.execute_query("SELECT COUNT(*) as count FROM campaigns WHERE status = 'draft'")[0]['count']
        }
        
        # Performance stats
        avg_roi = self.execute_query("SELECT AVG(projected_roi) as avg_roi FROM campaign_results")[0]['avg_roi']
        stats['performance'] = {
            'average_roi': round(avg_roi, 1) if avg_roi else 0,
            'total_projected_revenue': self.execute_query("SELECT SUM(projected_revenue) as total FROM campaign_results")[0]['total'] or 0
        }
        
        return stats


# Global instance
db = DatabaseHelper()

# Convenience functions for easy import - FIXED VERSIONS
def get_customers(segment: Optional[str] = None, limit: int = 100) -> List[Dict]:
    return db.get_customers(segment, limit)

def get_products(category: Optional[str] = None) -> List[Dict]:
    return db.get_products(category)

def get_campaigns(status: Optional[str] = None, **kwargs) -> List[Dict]:
    return db.get_campaigns(status, **kwargs)

def get_campaign_by_id(campaign_id: str) -> Optional[Dict]:
    return db.get_campaign_by_id(campaign_id)

def create_campaign(campaign_data: Dict) -> str:
    return db.create_campaign(campaign_data)

def get_campaign_results(campaign_id: str) -> List[Dict]:
    return db.get_campaign_results(campaign_id)

def save_campaign_result(campaign_id: str, result_data: Dict) -> int:
    return db.save_campaign_result(campaign_id, result_data)

def get_scenarios(campaign_id: str) -> List[Dict]:
    return db.get_scenarios(campaign_id)

def save_scenario(campaign_id: str, scenario_data: Dict) -> str:
    return db.save_scenario(campaign_id, scenario_data)

def get_dashboard_stats() -> Dict:
    return db.get_dashboard_stats()
