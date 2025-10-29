"""
Database initialization script for MarketBridge - Python 3.13 compatible.

This script:
1. Creates all database tables from our SQLAlchemy models
2. Populates tables with realistic sample data for development/demo
3. Provides utilities to reset the database when needed
"""

import asyncio
import sqlite3
import os
from datetime import datetime, timedelta
from pathlib import Path


def create_sqlite_database():
    """Create SQLite database and tables directly using SQL"""
    
    # Database path
    db_path = Path(__file__).parent.parent / "marketbridge.db"
    
    # Remove existing database
    if db_path.exists():
        os.remove(db_path)
        print("🗑️  Removed existing database")
    
    # Connect to SQLite
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    
    try:
        print("🚀 Creating database tables...")
        
        # Create customers table
        cursor.execute("""
            CREATE TABLE customers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_id VARCHAR(50) UNIQUE NOT NULL,
                name VARCHAR(100) NOT NULL,
                email VARCHAR(100) UNIQUE,
                segment VARCHAR(20) DEFAULT 'new_customer',
                lifetime_value REAL DEFAULT 0.0,
                average_order_value REAL DEFAULT 0.0,
                total_orders INTEGER DEFAULT 0,
                last_purchase_date DATETIME,
                preferred_channels TEXT,
                product_preferences TEXT,
                age_group VARCHAR(20),
                location VARCHAR(100),
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Create products table
        cursor.execute("""
            CREATE TABLE products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id VARCHAR(50) UNIQUE NOT NULL,
                name VARCHAR(200) NOT NULL,
                category VARCHAR(100) NOT NULL,
                description TEXT,
                base_price REAL NOT NULL,
                cost_price REAL NOT NULL,
                current_discount REAL DEFAULT 0.0,
                stock_quantity INTEGER DEFAULT 0,
                stock_regions TEXT,
                reorder_level INTEGER DEFAULT 10,
                is_active BOOLEAN DEFAULT 1,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Create campaigns table
        cursor.execute("""
            CREATE TABLE campaigns (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                campaign_id VARCHAR(50) UNIQUE NOT NULL,
                name VARCHAR(200) NOT NULL,
                description TEXT,
                campaign_type VARCHAR(50),
                status VARCHAR(20) DEFAULT 'draft',
                product_id INTEGER NOT NULL,
                target_audience_size INTEGER DEFAULT 10000,
                discount_rate REAL DEFAULT 10.0,
                budget REAL NOT NULL,
                duration_days INTEGER DEFAULT 30,
                target_segments TEXT,
                target_channels TEXT,
                target_regions TEXT,
                start_date DATETIME,
                end_date DATETIME,
                created_by VARCHAR(100),
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (product_id) REFERENCES products (id)
            )
        """)
        
        # Create campaign_results table
        cursor.execute("""
            CREATE TABLE campaign_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                campaign_id INTEGER NOT NULL,
                creative_output TEXT,
                finance_output TEXT,
                inventory_output TEXT,
                final_recommendation TEXT,
                projected_roi REAL,
                projected_revenue REAL,
                projected_customers INTEGER,
                risk_score VARCHAR(20),
                success_probability REAL,
                agent_reasoning TEXT,
                negotiation_rounds INTEGER DEFAULT 0,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (campaign_id) REFERENCES campaigns (id)
            )
        """)
        
        # Create what_if_scenarios table
        cursor.execute("""
            CREATE TABLE what_if_scenarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                scenario_id VARCHAR(50) UNIQUE NOT NULL,
                campaign_id INTEGER NOT NULL,
                scenario_name VARCHAR(100) NOT NULL,
                scenario_description TEXT,
                input_discount_rate REAL,
                input_target_size INTEGER,
                input_budget REAL,
                input_duration INTEGER,
                projected_roi REAL,
                projected_revenue REAL,
                success_probability REAL,
                risk_assessment VARCHAR(20),
                recommended_channels TEXT,
                targeting_strategy TEXT,
                budget_allocation TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (campaign_id) REFERENCES campaigns (id)
            )
        """)
        
        print("✅ Database tables created successfully!")
        
        # Insert sample data
        populate_sample_data(cursor)
        
        conn.commit()
        print("✅ Database initialization completed!")
        
        # Show stats
        get_database_stats(cursor)
        
    except Exception as e:
        print(f"❌ Error creating database: {e}")
        conn.rollback()
        raise
    finally:
        conn.close()


def populate_sample_data(cursor):
    """Populate database with sample data"""
    print("🌱 Populating sample data...")
    
    # Insert sample customers
    customers_data = [
        ('CUST_001', 'John Smith', 'john@example.com', 'high_value', 2500.0, 150.0, 17, 
         '["email", "social"]', '["electronics", "gadgets"]', '25-35', 'Mumbai'),
        ('CUST_002', 'Sarah Johnson', 'sarah@example.com', 'medium_value', 800.0, 80.0, 10,
         '["email", "sms"]', '["fashion", "accessories"]', '18-25', 'Delhi'),
        ('CUST_003', 'Mike Chen', 'mike@example.com', 'new_customer', 0.0, 0.0, 0,
         '["social", "web"]', '["electronics"]', '26-35', 'Bangalore'),
        ('CUST_004', 'Emily Davis', 'emily@example.com', 'high_value', 3200.0, 200.0, 16,
         '["email", "social", "sms"]', '["fitness", "wellness"]', '30-40', 'Chennai'),
        ('CUST_005', 'Alex Kumar', 'alex@example.com', 'medium_value', 1200.0, 100.0, 12,
         '["social", "search"]', '["electronics", "fitness"]', '22-30', 'Hyderabad')
    ]
    
    cursor.executemany("""
        INSERT INTO customers (customer_id, name, email, segment, lifetime_value, 
                             average_order_value, total_orders, preferred_channels, 
                             product_preferences, age_group, location)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, customers_data)
    
    # Insert sample products
    products_data = [
        ('PROD_001', 'Wireless Bluetooth Headphones', 'Electronics', 
         'Premium noise-cancelling wireless headphones', 299.99, 120.0, 0.0, 150,
         '{"north": 60, "south": 50, "west": 40}', 20),
        ('PROD_002', 'Smart Fitness Watch', 'Wearables',
         'Advanced fitness tracking smartwatch', 199.99, 80.0, 0.0, 200,
         '{"north": 80, "south": 70, "west": 50}', 25),
        ('PROD_003', 'Wireless Earbuds Pro', 'Electronics',
         'Professional-grade wireless earbuds with active noise cancellation', 149.99, 60.0, 0.0, 300,
         '{"north": 120, "south": 100, "west": 80}', 30)
    ]
    
    cursor.executemany("""
        INSERT INTO products (product_id, name, category, description, base_price, 
                            cost_price, current_discount, stock_quantity, stock_regions, reorder_level)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, products_data)
    
    # Insert sample campaigns
    campaigns_data = [
        ('CAMP_001', 'Black Friday Electronics Sale', 
         'Major discount campaign for premium electronics during Black Friday',
         'seasonal_sale', 'planning', 1, 15000, 25.0, 75000.0, 7,
         '["high_value", "medium_value"]', '["email", "social", "search_ads"]', 
         '["north", "south", "west"]', 'marketing_team'),
        ('CAMP_002', 'New Year Fitness Campaign',
         'Promote fitness watches for New Year resolution season',
         'product_launch', 'draft', 2, 8000, 15.0, 40000.0, 14,
         '["new_customer", "returning"]', '["social", "influencer", "content"]',
         '["north", "south"]', 'product_team'),
        ('CAMP_003', 'Customer Retention Program',
         'Re-engage customers who haven\'t purchased in 6 months',
         'customer_retention', 'approved', 1, 5000, 20.0, 25000.0, 21,
         '["churned", "medium_value"]', '["email", "sms", "direct_mail"]',
         '["north", "west"]', 'retention_team')
    ]
    
    cursor.executemany("""
        INSERT INTO campaigns (campaign_id, name, description, campaign_type, status, 
                             product_id, target_audience_size, discount_rate, budget, duration_days,
                             target_segments, target_channels, target_regions, created_by)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, campaigns_data)
    
    # Insert sample campaign results
    results_data = [
        (1, # campaign_id for Black Friday sale
         '{"strategy": "Bold Black Friday messaging", "key_message": "Premium sound, premium savings"}',
         '{"roi_projection": 28.5, "revenue_estimate": 448750.0, "approval_status": "Approved"}',
         '{"stock_availability": "Sufficient", "projected_units_sold": 1875}',
         '{"go_no_go": "GO", "confidence_level": 0.85}',
         28.5, 448750.0, 1875, 'Medium', 0.85,
         '{"creative_reasoning": "Black Friday creates urgency", "finance_reasoning": "ROI above threshold"}',
         2),
        (2, # campaign_id for New Year fitness
         '{"strategy": "New Year transformation", "key_message": "Track your transformation"}',
         '{"roi_projection": 22.3, "revenue_estimate": 179280.0, "approval_status": "Approved"}',
         '{"stock_availability": "Excellent", "projected_units_sold": 896}',
         '{"go_no_go": "GO", "confidence_level": 0.78}',
         22.3, 179280.0, 896, 'Medium', 0.78,
         '{"creative_reasoning": "Perfect New Year timing", "finance_reasoning": "Meets ROI threshold"}',
         3)
    ]
    
    cursor.executemany("""
        INSERT INTO campaign_results (campaign_id, creative_output, finance_output, inventory_output,
                                    final_recommendation, projected_roi, projected_revenue, projected_customers,
                                    risk_score, success_probability, agent_reasoning, negotiation_rounds)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, results_data)
    
    # Insert sample what-if scenarios
    scenarios_data = [
        ('SCEN_001', 1, 'Conservative Strategy', 'Lower risk with reduced discount',
         15.0, 10000, 50000.0, 7, 24.2, 303000.0, 0.92, 'Low',
         '["email", "search_ads"]', 'Focus on existing customers',
         '{"email": 0.3, "search_ads": 0.4, "social": 0.2, "contingency": 0.1}'),
        ('SCEN_002', 1, 'Aggressive Strategy', 'High-impact with maximum discount',
         35.0, 25000, 100000.0, 7, 31.8, 636500.0, 0.72, 'High',
         '["social", "influencer", "display_ads"]', 'Broad market penetration',
         '{"social": 0.35, "influencer": 0.25, "display": 0.2, "search": 0.15}'),
        ('SCEN_003', 2, 'Balanced Strategy', 'Moderate approach balancing reach and profit',
         15.0, 8000, 40000.0, 14, 22.3, 179280.0, 0.78, 'Medium',
         '["social", "content", "partnerships"]', 'Mixed audience with A/B testing',
         '{"social": 0.4, "content": 0.3, "partnerships": 0.2, "optimization": 0.1}')
    ]
    
    cursor.executemany("""
        INSERT INTO what_if_scenarios (scenario_id, campaign_id, scenario_name, scenario_description,
                                     input_discount_rate, input_target_size, input_budget, input_duration,
                                     projected_roi, projected_revenue, success_probability, risk_assessment,
                                     recommended_channels, targeting_strategy, budget_allocation)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, scenarios_data)
    
    print("✅ Sample data populated successfully!")


def get_database_stats(cursor):
    """Print current database statistics"""
    cursor.execute("SELECT COUNT(*) FROM customers")
    customer_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM products")
    product_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM campaigns")
    campaign_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM campaign_results")
    result_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM what_if_scenarios")
    scenario_count = cursor.fetchone()[0]
    
    print("\n📈 Database Statistics:")
    print(f"   👥 Customers: {customer_count}")
    print(f"   📦 Products: {product_count}")
    print(f"   🎯 Campaigns: {campaign_count}")
    print(f"   🤖 Campaign Results: {result_count}")
    print(f"   🎲 What-If Scenarios: {scenario_count}")


def reset_database():
    """Reset database completely"""
    db_path = Path(__file__).parent.parent / "marketbridge.db"
    if db_path.exists():
        os.remove(db_path)
        print("🗑️  Database reset!")
    create_sqlite_database()


def main():
    """Main CLI function"""
    import sys
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "init":
            create_sqlite_database()
        elif command == "reset":
            reset_database()
        elif command == "stats":
            db_path = Path(__file__).parent.parent / "marketbridge.db"
            if db_path.exists():
                conn = sqlite3.connect(str(db_path))
                get_database_stats(conn.cursor())
                conn.close()
            else:
                print("❌ Database doesn't exist. Run 'init' first.")
        else:
            print("Available commands: init, reset, stats")
    else:
        create_sqlite_database()


if __name__ == "__main__":
    main()
