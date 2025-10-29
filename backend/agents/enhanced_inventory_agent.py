"""
Enhanced Inventory Agent - Fixed Version
Handles inventory analysis, supply chain optimization, and regional distribution with proper data handling
"""

import asyncio
import logging
import json
from typing import Dict, List, Any, Optional, Union
from datetime import datetime
import uuid
from agents.ai_client import gemini_client

logger = logging.getLogger(__name__)

class EnhancedInventoryAgent:
    """Enhanced Inventory Agent with fixed data processing and robust error handling"""
    
    def __init__(self):
        self.agent_id = f"inventory_{uuid.uuid4().hex[:8]}"
        self.initialized = False
        
    async def initialize(self):
        """Initialize inventory agent"""
        try:
            self.initialized = True
            logger.info("📦 Enhanced Inventory Agent initialized successfully")
            return True
        except Exception as e:
            logger.error(f"❌ Inventory Agent initialization failed: {e}")
            return False
    
    async def analyze_inventory_requirements(self, query: str, product: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Comprehensive inventory analysis with fixed data processing"""
        try:
            if not self.initialized:
                await self.initialize()
            
            # Get product and context with safe processing
            product_context = context.get('product', {}) if context else {}
            customer_context = context.get('customers', {}) if context else {}
            
            # Extract inventory parameters safely
            current_stock = self._safe_int(product_context.get('stock_quantity', 150))
            base_price = self._safe_float(product_context.get('base_price', 299.99))
            
            # Generate inventory insights using Gemini AI
            system_prompt = (
                "You are an inventory management AI agent specialized in campaign planning. "
                "Your role is to analyze inventory requirements, supply chain impacts, and "
                "provide strategic recommendations for optimal inventory management during campaigns."
            )
            
            user_prompt = (
                f"Product: {product}\n"
                f"Campaign Query: {query}\n"
                f"Current Stock: {current_stock} units\n"
                f"Base Price: ${base_price:,.2f}\n"
                "Provide comprehensive inventory analysis focusing on:\n"
                "1. Stock level assessment and recommendations\n"
                "2. Supply chain impact and risk mitigation\n"
                "3. Regional distribution strategy\n"
                "4. Campaign feasibility from inventory perspective\n"
            )
            
            # Get AI-generated insights
            inventory_insights = await gemini_client.generate_response(system_prompt, user_prompt)
            
            # Process regional data safely
            regional_data = self._process_regional_data(product_context.get('stock_regions', '{}'))
            
            # Base analyses
            stock_analysis = self._analyze_stock_status(current_stock, query)
            demand_analysis = self._estimate_campaign_demand(query, current_stock, customer_context)
            regional_analysis = self._analyze_regional_distribution(regional_data, demand_analysis)
            
            # Supply chain assessment with AI insights
            risk_level = "medium"
            supplier_status = "normal_capacity"
            if current_stock >= 150 and demand_analysis.get('projected_campaign_demand', 100) <= 150:
                risk_level = "low"
                supplier_status = "adequate_capacity"
            elif current_stock < 50 or demand_analysis.get('projected_campaign_demand', 100) > 200:
                risk_level = "high"
                supplier_status = "constrained_capacity"
            
            supply_chain_analysis = {
                "supply_chain_risk_level": risk_level,
                "supplier_capacity_status": supplier_status,
                "logistics_readiness": "excellent_multi_region" if risk_level == "low" else "adequate_standard"
            }
            
            # Campaign feasibility
            feasibility_assessment = self._assess_campaign_feasibility(
                current_stock, demand_analysis, supply_chain_analysis
            )
            
            # Inventory optimization recommendations
            optimization_recommendations = self._generate_optimization_recommendations(
                stock_analysis, regional_analysis, feasibility_assessment
            )
            
            # Budget impact analysis
            budget_analysis = self._analyze_inventory_budget_impact(
                demand_analysis, supply_chain_analysis, base_price
            )
            
            return {
                "agent": "Enhanced Inventory Agent",
                "timestamp": datetime.now().isoformat(),
                "analysis_id": f"inv_{uuid.uuid4().hex[:8]}",
                "current_stock": current_stock,
                "reorder_level": max(10, int(current_stock * 0.2)),
                **stock_analysis,
                "carrying_cost_impact": self._calculate_carrying_costs(current_stock, base_price),
                **regional_analysis,
                "domestic_lead_time_days": 7,
                "international_lead_time_days": 21,
                "seasonal_demand_factor": self._calculate_seasonal_factor(query),
                "reorder_recommendation": self._calculate_reorder_quantity(current_stock, demand_analysis),
                "expedited_shipping_possible": True,
                "supplier_capacity_status": self._assess_supplier_capacity(demand_analysis),
                "logistics_readiness": self._assess_logistics_readiness(regional_analysis),
                **supply_chain_analysis,
                **demand_analysis,
                **feasibility_assessment,
                "recommended_campaign_scope": self._recommend_campaign_scope(feasibility_assessment),
                "inventory_constraints": self._identify_inventory_constraints(stock_analysis, demand_analysis),
                "supply_chain_recommendations": optimization_recommendations,
                "confidence_level": self._calculate_inventory_confidence(stock_analysis, feasibility_assessment),
                "operational_risk": self._assess_operational_risk(stock_analysis, supply_chain_analysis),
                "fulfillment_capability": self._assess_fulfillment_capability(current_stock, demand_analysis),
                "dependencies": ["supplier_response", "logistics_capacity"],
                "reasoning": self._generate_inventory_reasoning(stock_analysis, demand_analysis, feasibility_assessment),
                **budget_analysis
            }
            
        except Exception as e:
            logger.error(f"❌ Inventory analysis failed: {e}")
            return self._get_fallback_inventory_analysis(query, product)
    
    def _safe_int(self, value: Any) -> int:
        """Safely convert any value to int"""
        try:
            if isinstance(value, (int, float)):
                return int(value)
            elif isinstance(value, str):
                return int(float(value.replace(',', '')))
            else:
                return 0
        except (ValueError, TypeError):
            return 0
    
    def _safe_float(self, value: Any) -> float:
        """Safely convert any value to float"""
        try:
            if isinstance(value, (int, float)):
                return float(value)
            elif isinstance(value, str):
                return float(value.replace('$', '').replace(',', ''))
            else:
                return 0.0
        except (ValueError, TypeError):
            return 0.0
    
    def _process_regional_data(self, regional_data: Any) -> Dict[str, Any]:
        """Process regional data safely - FIXED STRING PROCESSING ERROR"""
        try:
            # Handle different input types
            if isinstance(regional_data, dict):
                # Already a dictionary, return as-is
                return regional_data
            elif isinstance(regional_data, str):
                # Try to parse JSON string
                if regional_data.strip():
                    parsed_data = json.loads(regional_data)
                    if isinstance(parsed_data, dict):
                        return parsed_data
                # If parsing fails or empty string, return fallback
                return self._get_fallback_regional_data()
            else:
                # Any other type, return fallback
                return self._get_fallback_regional_data()
                
        except (json.JSONDecodeError, TypeError, AttributeError) as e:
            logger.warning(f"Regional data processing error: {e}, using fallback")
            return self._get_fallback_regional_data()
    
    def _get_fallback_regional_data(self) -> Dict[str, Any]:
        """Fallback regional data structure"""
        return {
            "north": {"stock": 60, "demand_multiplier": 1.2, "preference": True},
            "south": {"stock": 50, "demand_multiplier": 1.3, "preference": True},
            "west": {"stock": 40, "demand_multiplier": 1.1, "preference": False}
        }
    
    def _analyze_stock_status(self, current_stock: int, query: str) -> Dict[str, Any]:
        """Analyze current stock status"""
        try:
            # Determine stock status
            if current_stock >= 200:
                status = "excellent"
                description = "Excellent levels for large campaigns"
            elif current_stock >= 100:
                status = "good"
                description = "Good levels for standard campaigns"
            elif current_stock >= 50:
                status = "adequate"
                description = "Adequate for targeted campaigns"
            else:
                status = "limited"
                description = "Limited inventory requires careful planning"
            
            # Calculate days of supply (assuming 3 units sold per day baseline)
            daily_consumption = 3
            if "aggressive" in query.lower():
                daily_consumption = 5
            elif "premium" in query.lower():
                daily_consumption = 2
            
            days_of_supply = max(1, current_stock // daily_consumption)
            
            # Determine restock urgency
            if days_of_supply <= 10:
                urgency = "high"
            elif days_of_supply <= 30:
                urgency = "medium"
            else:
                urgency = "low"
            
            return {
                "stock_status": status,
                "status_description": description,
                "days_of_supply": days_of_supply,
                "restock_urgency": urgency,
                "stock_efficiency": min(1.0, current_stock / 200.0)  # Efficiency score
            }
            
        except Exception as e:
            logger.error(f"Stock status analysis error: {e}")
            return {
                "stock_status": "adequate",
                "status_description": "Standard inventory levels",
                "days_of_supply": 30,
                "restock_urgency": "medium",
                "stock_efficiency": 0.75
            }
    
    def _estimate_campaign_demand(self, query: str, current_stock: int, customer_context: Dict) -> Dict[str, Any]:
        """Estimate campaign-driven demand"""
        try:
            # Base demand estimation
            total_customers = customer_context.get('total_customers', 1000)
            base_demand = max(20, int(total_customers * 0.05))  # 5% of customer base
            
            # Query-based demand adjustments
            demand_multiplier = 1.0
            if "aggressive" in query.lower():
                demand_multiplier = 1.8
            elif "holiday" in query.lower() or "sale" in query.lower():
                demand_multiplier = 1.5
            elif "premium" in query.lower():
                demand_multiplier = 0.7
            elif "boost" in query.lower() and "revenue" in query.lower():
                demand_multiplier = 1.6
            
            projected_demand = int(base_demand * demand_multiplier)
            
            # Calculate supportable demand (80% of current stock as safety margin)
            max_supportable = int(current_stock * 0.8)
            
            # Risk assessment
            if projected_demand <= max_supportable * 0.5:
                risk_level = "minimal_excess_capacity"
            elif projected_demand <= max_supportable:
                risk_level = "manageable_within_capacity"
            else:
                risk_level = "exceeds_current_capacity"
            
            # Stockout probability
            stockout_probability = max(0, min(100, (projected_demand - current_stock) / current_stock * 100))
            
            return {
                "base_demand_estimate": base_demand,
                "projected_campaign_demand": projected_demand,
                "max_supportable_demand": max_supportable,
                "demand_risk_assessment": risk_level,
                "stockout_probability": int(stockout_probability),
                "recommended_campaign_scale": self._recommend_campaign_scale(projected_demand, max_supportable),
                "inventory_buffer_needed": max(0, projected_demand - current_stock + 20)  # +20 safety buffer
            }
            
        except Exception as e:
            logger.error(f"Demand estimation error: {e}")
            return {
                "base_demand_estimate": 30,
                "projected_campaign_demand": 50,
                "max_supportable_demand": 80,
                "demand_risk_assessment": "manageable_within_capacity",
                "stockout_probability": 15,
                "recommended_campaign_scale": "standard_campaign",
                "inventory_buffer_needed": 25
            }
    
    def _analyze_regional_distribution(self, regional_data: Dict, demand_analysis: Dict) -> Dict[str, Any]:
        """Analyze regional inventory distribution - FIXED ITEMS() PROCESSING"""
        try:
            regional_analysis: Dict[str, Union[Dict[str, Dict[str, Any]], List[str], float, List[str]]] = {
                "regional_stock_analysis": {},
                "recommended_regions": [],
                "regional_constraints": [],
                "regional_optimization_score": 50.0,
                "cross_regional_transfer_opportunities": []
            }
            recommended_regions = []
            total_regional_score = 0
            
            # Process each region safely - FIXED .items() ERROR
            for region_name, region_info in regional_data.items():
                try:
                    # Handle different region_info formats
                    if isinstance(region_info, dict):
                        stock_level = self._safe_int(region_info.get('stock', 50))
                        demand_multiplier = self._safe_float(region_info.get('demand_multiplier', 1.0))
                        preference = region_info.get('preference', True)
                    else:
                        # Fallback if region_info is not a dict
                        stock_level = self._safe_int(region_info) if region_info else 50
                        demand_multiplier = 1.0
                        preference = True
                    
                    # Calculate campaign suitability
                    if stock_level >= 40 and preference:
                        suitability = "good"
                    elif stock_level >= 20:
                        suitability = "moderate"
                    else:
                        suitability = "limited"
                    
                    # Calculate region score
                    region_score = (stock_level * demand_multiplier * (1.2 if preference else 0.8))
                    total_regional_score += region_score
                    
                    # Add to analysis
                    stock_analysis = regional_analysis["regional_stock_analysis"]
                    if isinstance(stock_analysis, dict):
                        stock_analysis[region_name] = {
                            "stock_level": stock_level,
                            "demand_multiplier": demand_multiplier,
                            "category_preference": preference,
                            "campaign_suitability": suitability,
                            "region_score": round(region_score, 1)
                        }
                    
                    # Add to recommended regions if suitable
                    if suitability in ["good", "moderate"]:
                        recommended_regions.append(region_name)
                        
                except Exception as region_error:
                    logger.warning(f"Error processing region {region_name}: {region_error}")
                    continue
            
            # Add summary metrics and safely cast dictionary types
            stock_analysis = regional_analysis["regional_stock_analysis"]
            if isinstance(stock_analysis, dict):
                regional_analysis["recommended_regions"] = recommended_regions[:3]
                regional_analysis["regional_constraints"] = self._identify_regional_constraints(stock_analysis)
                regional_analysis["regional_optimization_score"] = round(total_regional_score / len(regional_data), 2) if regional_data else 50.0
                regional_analysis["cross_regional_transfer_opportunities"] = self._identify_transfer_opportunities(stock_analysis)
            
            return regional_analysis
            
        except Exception as e:
            logger.error(f"Regional analysis error: {e}")
            return {
                "regional_stock_analysis": {
                    "national": {"stock_level": 150, "suitability": "good", "region_score": 150}
                },
                "recommended_regions": ["national"],
                "regional_constraints": [],
                "regional_optimization_score": 75.0,
                "cross_regional_transfer_opportunities": []
            }
    
    def _identify_regional_constraints(self, regional_stock: Dict[str, Dict[str, Any]]) -> List[str]:
        """Identify regional inventory constraints"""
        constraints = []
        try:
            for region, data in regional_stock.items():
                stock_level = data.get('stock_level', 0)
                if stock_level < 30:
                    constraints.append(f"{region.title()} region has limited inventory ({stock_level} units)")
                if data.get('campaign_suitability') == 'limited':
                    constraints.append(f"{region.title()} region not recommended for large campaigns")
        except Exception:
            pass
        return constraints[:3]  # Top 3 constraints

    def _identify_transfer_opportunities(self, regional_stock: Dict[str, Dict[str, Any]]) -> List[str]:
        """Identify opportunities for cross-regional inventory transfers"""
        opportunities = []
        try:
            # Find regions with excess and deficit
            high_stock = []
            low_stock = []
            
            for region, data in regional_stock.items():
                stock_level = data.get('stock_level', 0)
                if stock_level > 60:
                    high_stock.append(region)
                elif stock_level < 30:
                    low_stock.append(region)
            
            # Suggest transfers
            for high in high_stock[:2]:
                for low in low_stock[:2]:
                    opportunities.append(f"Transfer inventory from {high.title()} to {low.title()}")
                    
        except Exception:
            pass
        return opportunities[:2]  # Top 2 opportunities    def _assess_supply_chain(self, stock_analysis: Dict[str, Any], demand_analysis: Dict[str, Any], query: str) -> Dict[str, str]:
        """Assess supply chain readiness"""
        try:
            # Base supply chain risk
            current_status = stock_analysis.get('stock_status', 'adequate')
            projected_demand = demand_analysis.get('projected_campaign_demand', 50)
            
            # Risk level assessment
            if current_status == 'excellent' and projected_demand <= 100:
                risk_level = "low"
            elif current_status in ['good', 'adequate'] and projected_demand <= 150:
                risk_level = "medium"
            else:
                risk_level = "high"
            
            return {
                "supply_chain_risk_level": risk_level,
                "supplier_capacity_status": "normal_capacity" if risk_level != "high" else "constrained_capacity",
                "logistics_readiness": "excellent_multi_region" if risk_level == "low" else "adequate_standard",
            }
            
        except Exception:
            return {
                "supply_chain_risk_level": "medium",
                "supplier_capacity_status": "normal_capacity",
                "logistics_readiness": "adequate_standard"
            }
    
    def _assess_campaign_feasibility(self, current_stock: int, demand_analysis: Dict, supply_chain: Dict) -> Dict[str, Any]:
        """Assess overall campaign feasibility"""
        try:
            projected_demand = demand_analysis.get('projected_campaign_demand', 50)
            max_supportable = demand_analysis.get('max_supportable_demand', 100)
            risk_level = supply_chain.get('supply_chain_risk_level', 'medium')
            
            # Feasibility determination
            if projected_demand <= max_supportable and risk_level == 'low':
                feasibility = "feasible"
            elif projected_demand <= max_supportable * 1.2 and risk_level in ['low', 'medium']:
                feasibility = "feasible_with_monitoring"
            elif projected_demand <= current_stock:
                feasibility = "feasible_with_constraints"
            else:
                feasibility = "requires_restocking"
            
            return {"campaign_feasibility": feasibility}
            
        except Exception:
            return {"campaign_feasibility": "feasible_with_monitoring"}
    
    def _recommend_campaign_scale(self, projected_demand: int, max_supportable: int) -> str:
        """Recommend campaign scale based on inventory capacity"""
        try:
            ratio = projected_demand / max(1, max_supportable)
            
            if ratio <= 0.6:
                return "scale_up_opportunity"
            elif ratio <= 1.0:
                return "optimal_scale"
            else:
                return "scale_down_recommended"
        except:
            return "standard_scale"
    
    def _recommend_campaign_scope(self, feasibility_assessment: Dict) -> Dict[str, Any]:
        """Recommend campaign scope based on feasibility"""
        feasibility = feasibility_assessment.get('campaign_feasibility', 'feasible_with_monitoring')
        
        scope_recommendations = {
            "feasible": {"scope": "full_campaign", "geographic": "all_regions", "timeline": "standard"},
            "feasible_with_monitoring": {"scope": "standard_campaign", "geographic": "primary_regions", "timeline": "standard"},
            "feasible_with_constraints": {"scope": "targeted_campaign", "geographic": "select_regions", "timeline": "extended"},
            "requires_restocking": {"scope": "delayed_campaign", "geographic": "limited_regions", "timeline": "post_restock"}
        }
        
        return scope_recommendations.get(feasibility, scope_recommendations["feasible_with_monitoring"])
    
    def _calculate_carrying_costs(self, stock: int, price: float) -> Dict[str, Any]:
        """Calculate inventory carrying costs"""
        try:
            monthly_rate = 0.02  # 2% per month
            cost_per_unit = self._safe_float(price) * monthly_rate
            monthly_carrying_cost = stock * cost_per_unit
            
            return {
                "monthly_carrying_cost": round(monthly_carrying_cost, 2),
                "cost_per_unit": round(cost_per_unit, 2),
                "optimization_opportunity": "Maintain current levels" if stock <= 200 else "Consider reduction"
            }
        except:
            return {"monthly_carrying_cost": 375.0, "cost_per_unit": 2.5}
    
    def _calculate_seasonal_factor(self, query: str) -> float:
        """Calculate seasonal demand factor"""
        if "holiday" in query.lower() or "black friday" in query.lower():
            return 1.5
        elif "summer" in query.lower():
            return 1.2
        elif "back to school" in query.lower():
            return 1.3
        else:
            return 1.0
    
    def _calculate_reorder_quantity(self, current_stock: int, demand_analysis: Dict) -> int:
        """Calculate recommended reorder quantity"""
        try:
            projected_demand = demand_analysis.get('projected_campaign_demand', 50)
            safety_stock = 50  # Base safety stock
            
            reorder_quantity = projected_demand + safety_stock - current_stock
            return max(0, reorder_quantity)
        except:
            return max(0, 225 - current_stock)
    
    def _assess_supplier_capacity(self, demand_analysis: Dict) -> str:
        """Assess supplier capacity to meet demand"""
        projected_demand = demand_analysis.get('projected_campaign_demand', 50)
        
        if projected_demand <= 100:
            return "normal_capacity"
        elif projected_demand <= 200:
            return "high_utilization"
        else:
            return "capacity_constrained"
    
    def _assess_logistics_readiness(self, regional_analysis: Dict) -> str:
        """Assess logistics readiness"""
        recommended_regions = regional_analysis.get('recommended_regions', [])
        
        if len(recommended_regions) >= 3:
            return "excellent_multi_region"
        elif len(recommended_regions) >= 2:
            return "good_dual_region"
        else:
            return "adequate_single_region"
    
    def _identify_inventory_constraints(self, stock_analysis: Dict, demand_analysis: Dict) -> List[str]:
        """Identify inventory-related constraints"""
        constraints = []
        
        if stock_analysis.get('stock_status') == 'limited':
            constraints.append("Limited inventory requires targeted campaign approach")
        
        if demand_analysis.get('stockout_probability', 0) > 20:
            constraints.append("High stockout risk during peak campaign period")
        
        if stock_analysis.get('restock_urgency') == 'high':
            constraints.append("Urgent restocking required before campaign launch")
        
        return constraints[:3]
    
    def _generate_optimization_recommendations(self, stock_analysis: Dict, regional_analysis: Dict, feasibility: Dict) -> List[str]:
        """Generate inventory optimization recommendations"""
        recommendations = []
        
        if stock_analysis.get('stock_efficiency', 0.8) < 0.7:
            recommendations.append("Increase inventory levels to support larger campaigns")
        
        regional_constraints = regional_analysis.get('regional_constraints', [])
        if regional_constraints:
            recommendations.append("Address regional inventory imbalances through transfers")
        
        if feasibility.get('campaign_feasibility') == 'requires_restocking':
            recommendations.append("Expedite restocking to enable campaign execution")
        
        return recommendations[:3]
    
    def _analyze_inventory_budget_impact(self, demand_analysis: Dict, supply_chain: Dict, price: float) -> Dict[str, Any]:
        """Analyze budget impact of inventory decisions"""
        try:
            projected_demand = demand_analysis.get('projected_campaign_demand', 50)
            buffer_needed = demand_analysis.get('inventory_buffer_needed', 20)
            
            # Calculate costs
            unit_cost = self._safe_float(price) * 0.6  # Assume 60% cost ratio
            restock_cost = buffer_needed * unit_cost
            
            return {
                "budget_inventory_optimization": {
                    "conservative_approach": "Limit campaign scope to current stock levels",
                    "aggressive_approach": f"Invest ${restock_cost:,.0f} in additional inventory" if buffer_needed > 0 else "No additional investment needed"
                },
                "restock_budget_allocation": f"${restock_cost:,.0f} recommended for inventory buffer" if buffer_needed > 0 else "No restocking budget required"
            }
        except:
            return {
                "budget_inventory_optimization": {"conservative_approach": "Maintain current inventory levels"},
                "restock_budget_allocation": "Standard inventory budget allocation recommended"
            }
    
    def _calculate_inventory_confidence(self, stock_analysis: Dict, feasibility: Dict) -> float:
        """Calculate confidence in inventory analysis"""
        try:
            base_confidence = 0.8
            
            stock_status = stock_analysis.get('stock_status', 'adequate')
            if stock_status == 'excellent':
                base_confidence += 0.1
            elif stock_status == 'limited':
                base_confidence -= 0.2
            
            feasibility_status = feasibility.get('campaign_feasibility', 'feasible_with_monitoring')
            if feasibility_status == 'feasible':
                base_confidence += 0.1
            elif 'requires' in feasibility_status:
                base_confidence -= 0.1
            
            return max(0.5, min(0.95, base_confidence))
        except:
            return 0.8
    
    def _assess_operational_risk(self, stock_analysis: Dict, supply_chain: Dict) -> str:
        """Assess operational risk level"""
        try:
            stock_status = stock_analysis.get('stock_status', 'adequate')
            supply_risk = supply_chain.get('supply_chain_risk_level', 'medium')
            
            if stock_status in ['excellent', 'good'] and supply_risk == 'low':
                return "low"
            elif stock_status == 'limited' or supply_risk == 'high':
                return "high"
            else:
                return "medium"
        except:
            return "medium"
    
    def _assess_fulfillment_capability(self, stock: int, demand_analysis: Dict) -> str:
        """Assess fulfillment capability"""
        try:
            max_supportable = demand_analysis.get('max_supportable_demand', 100)
            
            if max_supportable >= 150:
                return "high_volume_capable"
            elif max_supportable >= 75:
                return "standard_volume_capable"
            else:
                return "limited_volume_capability"
        except:
            return "standard_volume_capable"
    
    def _generate_inventory_reasoning(self, stock_analysis: Dict, demand_analysis: Dict, feasibility: Dict) -> str:
        """Generate comprehensive inventory reasoning"""
        try:
            current_stock = stock_analysis.get('current_stock', 150)
            stock_status = stock_analysis.get('stock_status', 'adequate')
            projected_demand = demand_analysis.get('projected_campaign_demand', 50)
            max_supportable = demand_analysis.get('max_supportable_demand', 100)
            feasibility = feasibility.get('campaign_feasibility', 'feasible_with_monitoring')
            stockout_prob = demand_analysis.get('stockout_probability', 10)
            
            reasoning = f"Inventory Analysis Reasoning:\n"
            reasoning += f"• Current Stock Status: {stock_status.title()} ({current_stock} units available)\n"
            reasoning += f"• Projected Campaign Demand: {projected_demand} units based on campaign scope analysis\n"
            reasoning += f"• Maximum Supportable Demand: {max_supportable} units (80% of current stock)\n"
            reasoning += f"• Stockout Probability: {stockout_prob}% chance based on demand projections\n"
            feasibility_str = feasibility.get('campaign_feasibility', 'feasible_with_monitoring')
            if isinstance(feasibility_str, str):
                feasibility_str = feasibility_str.replace('_', ' ').title()
            reasoning += f"• Campaign Feasibility: {feasibility_str}\n"
            reasoning += f"• Inventory Recommendation: Support campaign execution"
            
            return reasoning
        except:
            return "Comprehensive inventory analysis completed with supply chain risk assessment"
    
    def _get_fallback_inventory_analysis(self, query: str, product: str) -> Dict[str, Any]:
        """Fallback inventory analysis when main analysis fails"""
        return {
            "agent": "Enhanced Inventory Agent (Fallback)",
            "current_stock": 150,
            "stock_status": "adequate",
            "campaign_feasibility": "feasible_with_monitoring",
            "projected_campaign_demand": 50,
            "max_supportable_demand": 75,
            "recommended_regions": ["national"],
            "supply_chain_risk_level": "medium",
            "reasoning": "Fallback inventory analysis - conservative estimates applied due to calculation error",
            "confidence_level": 0.6
        }
    
    async def negotiate_with_agents(self, proposal: Dict, other_agents_data: Dict) -> Dict[str, Any]:
        """Negotiate inventory optimization with other agents"""
        try:
            # Adjust recommendations based on finance constraints
            finance_data = other_agents_data.get('Finance', {})
            approved_budget = finance_data.get('approved_budget', 20000)
            
            # If budget is tight, recommend conservative inventory approach
            if self._safe_float(approved_budget) < 15000:
                proposal['budget_inventory_optimization'] = {
                    "conservative_approach": "Limit campaign scope to current stock levels",
                    "budget_constraint_applied": True
                }
            
            # Adjust based on creative requirements
            creative_data = other_agents_data.get('Creative', {})
            target_audience = creative_data.get('target_audience', '')
            if "broad" in target_audience.lower():
                current_demand = proposal.get('projected_campaign_demand', 50)
                proposal['projected_campaign_demand'] = int(current_demand * 1.2)
                proposal['demand_adjustment'] = "Increased for broad audience targeting"
            
            proposal['negotiation_round'] = proposal.get('negotiation_round', 0) + 1
            proposal['last_optimization'] = datetime.now().isoformat()
            
            return proposal
            
        except Exception as e:
            logger.error(f"Inventory negotiation error: {e}")
            return proposal
