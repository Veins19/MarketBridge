"""
Enhanced Finance Agent - Fixed Version
Handles financial analysis, ROI calculations, and budget optimization with proper type handling
"""

import asyncio
import logging
import json
from typing import Dict, List, Any, Optional
from datetime import datetime
import uuid
from decimal import Decimal
from agents.ai_client import gemini_client

logger = logging.getLogger(__name__)

class EnhancedFinanceAgent:
    """Enhanced Finance Agent with fixed type handling and robust calculations"""
    
    def __init__(self):
        self.agent_id = f"finance_{uuid.uuid4().hex[:8]}"
        self.roi_threshold = 20.0  # Minimum acceptable ROI percentage
        self.initialized = False
        
    async def initialize(self):
        """Initialize finance agent"""
        try:
            self.initialized = True
            logger.info("💰 Enhanced Finance Agent initialized successfully")
            return True
        except Exception as e:
            logger.error(f"❌ Finance Agent initialization failed: {e}")
            return False
    
    async def analyze_financial_viability(self, query: str, product: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Comprehensive financial analysis with fixed type handling"""
        if context is None:
            context = {}
        try:
            print(f"🔍 Finance Agent Debug: Starting analysis")
            print(f"🔍 Finance Agent Debug: query='{query}', product='{product}'")
            print(f"🔍 Finance Agent Debug: context keys={list(context.keys()) if context else 'None'}")
            
            if not self.initialized:
                print(f"🔍 Finance Agent Debug: Initializing agent...")
                await self.initialize()
            
            # Get product and customer context
            product_context = context.get('product', {}) if context else {}
            customer_context = context.get('customers', {}) if context else {}
            
            print(f"🔍 Finance Agent Debug: product_context keys={list(product_context.keys())}")
            print(f"🔍 Finance Agent Debug: customer_context keys={list(customer_context.keys())}")
            
            # Extract financial parameters with type safety
            base_price = self._safe_float(product_context.get('base_price', 299.99))
            cost_price = self._safe_float(product_context.get('cost_price', 120.00))
            margin_per_unit = base_price - cost_price
            
            print(f"🔍 Finance Agent Debug: base_price={base_price}, cost_price={cost_price}, margin={margin_per_unit}")
            
            total_customers = self._safe_int(customer_context.get('total_customers', 1000))
            
            print(f"🔍 Finance Agent Debug: total_customers={total_customers}")
            
            # Estimate campaign parameters
            target_audience_size = self._estimate_target_audience_size(query, total_customers)
            conversion_rate = self._estimate_conversion_rate(query, product)
            projected_customers = int(target_audience_size * conversion_rate)
            
            print(f"🔍 Finance Agent Debug: target_audience={target_audience_size}, conversion_rate={conversion_rate}, projected_customers={projected_customers}")
            
            # Budget calculations - FIXED TYPE HANDLING
            print(f"🔍 Finance Agent Debug: Calculating budget requirements...")
            budget_analysis = self._calculate_budget_requirements(
                projected_customers, margin_per_unit, query
            )
            
            print(f"🔍 Finance Agent Debug: budget_analysis completed: {budget_analysis.get('optimal_budget', 'ERROR')}")
            
            # ROI calculations - FIXED DECIMAL/FLOAT HANDLING
            print(f"🔍 Finance Agent Debug: Calculating ROI metrics...")
            roi_metrics = self._calculate_roi_metrics(
                projected_customers, base_price, budget_analysis['optimal_budget'], cost_price
            )
            
            print(f"🔍 Finance Agent Debug: ROI calculation completed: {roi_metrics.get('projected_roi', 'ERROR')}%")
            
            # Generate financial insights using Gemini AI
            system_prompt = (
                "You are a financial analyst AI agent specialized in marketing campaign analysis. "
                "Your role is to provide strategic financial insights and recommendations based on "
                "campaign metrics and market conditions."
            )
            
            user_prompt = (
                f"Product: {product}\n"
                f"Campaign Query: {query}\n"
                f"ROI: {roi_metrics.get('projected_roi')}%\n"
                f"Projected Revenue: ${roi_metrics.get('projected_revenue'):,.2f}\n"
                f"Budget: ${budget_analysis.get('optimal_budget'):,.2f}\n"
                "Provide strategic financial insights and recommendations focusing on:\n"
                "1. ROI optimization strategies\n"
                "2. Risk assessment and mitigation\n"
                "3. Budget allocation recommendations\n"
                "4. Performance monitoring metrics\n"
            )
            
            # Get AI-generated insights
            finance_insights = await gemini_client.generate_response(system_prompt, user_prompt)
            
            # Risk assessment
            risk_analysis = self._assess_financial_risk(roi_metrics, budget_analysis, query)
            
            # Channel budget allocation
            channel_budgets = self._allocate_channel_budgets(budget_analysis['optimal_budget'], query)
            
            # Approval decision
            approval_status = self._make_approval_decision(roi_metrics['projected_roi'], risk_analysis['risk_score'])
            
            print(f"🔍 Finance Agent Debug: Analysis completed successfully!")
            
            return {
                "agent": "Enhanced Finance Agent",
                "timestamp": datetime.now().isoformat(),
                "analysis_id": f"fin_{uuid.uuid4().hex[:8]}",
                **roi_metrics,
                "projected_customers": projected_customers,
                "conversion_rate": round(conversion_rate, 3),
                "target_audience_size": target_audience_size,
                "margin_per_unit": round(margin_per_unit, 2),
                "break_even_customers": self._calculate_break_even(budget_analysis['optimal_budget'], margin_per_unit),
                "break_even_timeline": self._estimate_break_even_timeline(roi_metrics['projected_roi']),
                **budget_analysis,
                "budget_utilization_plan": self._create_budget_utilization_plan(budget_analysis['optimal_budget']),
                "cost_per_acquisition_target": self._calculate_cpa_target(budget_analysis['optimal_budget'], projected_customers),
                **risk_analysis,
                "success_probability": self._calculate_success_probability(roi_metrics, risk_analysis),
                "recommended_risk_budget": budget_analysis['optimal_budget'] * 4,
                "channel_budgets": channel_budgets,
                "channel_cost_analysis": self._analyze_channel_costs(channel_budgets),
                "budget_efficiency_score": self._calculate_budget_efficiency(roi_metrics, budget_analysis),
                "recommended_reallocation": self._suggest_budget_reallocation(channel_budgets),
                "approval_status": approval_status,
                "recommended_adjustments": self._suggest_budget_adjustments(roi_metrics, approval_status),
                "financing_options": self._suggest_financing_options(budget_analysis['optimal_budget']),
                "roi_optimization_tips": self._generate_roi_optimization_tips(),
                "confidence_level": self._calculate_finance_confidence(roi_metrics, risk_analysis),
                "risk_tolerance": "moderate",
                "budget_flexibility": 0.15,
                "dependencies": ["market_conditions", "execution_quality"],
                "reasoning": self._generate_financial_reasoning(roi_metrics, risk_analysis, approval_status)
            }
            
        except Exception as e:
            print(f"🔍 Finance Agent Debug: Exception caught: {str(e)}")
            import traceback
            print(f"🔍 Finance Agent Debug: Full traceback: {traceback.format_exc()}")
            logger.error(f"❌ Financial analysis failed: {e}")
            return self._get_fallback_financial_analysis(query, product)

    
    def _safe_float(self, value: Any) -> float:
        """Safely convert any value to float - FIXED TYPE HANDLING"""
        try:
            if isinstance(value, (int, float)):
                return float(value)
            elif isinstance(value, Decimal):
                return float(value)
            elif isinstance(value, str):
                # Remove currency symbols and convert
                clean_value = value.replace('$', '').replace(',', '').strip()
                return float(clean_value)
            else:
                return 0.0
        except (ValueError, TypeError):
            return 0.0
    
    def _safe_int(self, value: Any) -> int:
        """Safely convert any value to int"""
        try:
            return int(self._safe_float(value))
        except:
            return 0
    
    def _calculate_roi_metrics(self, customers: int, price: float, budget: float, cost: float) -> Dict[str, Any]:
        """Calculate ROI metrics with proper type conversion - FIXED DECIMAL HANDLING"""
        try:
            # Ensure all values are floats to avoid Decimal errors
            customers_float = self._safe_float(customers)
            price = self._safe_float(price)
            budget = self._safe_float(budget)
            cost = self._safe_float(cost)
            
            # Calculate revenue and profit
            projected_revenue = customers_float * price
            total_cost = (customers * cost) + budget
            projected_profit = projected_revenue - total_cost
            
            # Calculate ROI percentage
            roi_percentage = (projected_profit / budget * 100) if budget > 0 else 0
            
            return {
                "projected_roi": round(roi_percentage, 1),
                "projected_revenue": round(projected_revenue, 2),
                "projected_profit": round(projected_profit, 2)
            }
            
        except Exception as e:
            logger.error(f"ROI calculation error: {e}")
            # Fallback calculations
            return {
                "projected_roi": 22.0,  # Conservative estimate
                "projected_revenue": self._safe_float(budget) * 2.2,
                "projected_profit": self._safe_float(budget) * 0.22
            }
    
    def _calculate_budget_requirements(self, customers: int, margin: float, query: str) -> Dict[str, Any]:
        """Calculate budget requirements with type safety"""
        try:
            customers_float = self._safe_float(customers)
            margin = self._safe_float(margin)
            
            # Base budget calculation
            base_budget = customers_float * 50  # $50 per customer acquisition
            
            # Query-based adjustments
            multiplier = 1.0
            if "aggressive" in query.lower():
                multiplier = 1.5
            elif "premium" in query.lower():
                multiplier = 1.3
            elif "budget" in query.lower():
                multiplier = 0.8
            
            optimal_budget = base_budget * multiplier
            
            return {
                "minimum_budget": round(optimal_budget * 0.7, 2),
                "optimal_budget": round(optimal_budget, 2),
                "maximum_budget": round(optimal_budget * 1.5, 2),
                "approved_budget": round(optimal_budget, 2),
                "budget_breakdown": {
                    "media_spend": round(optimal_budget * 0.65, 2),
                    "creative_production": round(optimal_budget * 0.15, 2),
                    "operations": round(optimal_budget * 0.10, 2),
                    "contingency": round(optimal_budget * 0.10, 2)
                }   
            }
            
        except Exception as e:
            logger.error(f"Budget calculation error: {e}")
            return {
                "minimum_budget": 15000.0,
                "optimal_budget": 20000.0,
                "maximum_budget": 30000.0,
                "approved_budget": 20000.0,
                "budget_breakdown": {
                    "media_spend": 13000.0,
                    "creative_production": 3000.0,
                    "operations": 2000.0,
                    "contingency": 2000.0
                }
            }
    
    def _estimate_target_audience_size(self, query: str, total_customers: int) -> int:
        """Estimate target audience size based on query"""
        try:
            base_percentage = 0.3  # 30% of customer base
            
            if "aggressive" in query.lower():
                base_percentage = 0.5
            elif "premium" in query.lower():
                base_percentage = 0.2
            elif "broad" in query.lower():
                base_percentage = 0.7
            
            return max(100, int(total_customers * base_percentage))
        except:
            return 500  # Fallback
    
    def _estimate_conversion_rate(self, query: str, product: str) -> float:
        """Estimate conversion rate based on campaign type"""
        try:
            base_rate = 0.035  # 3.5% base conversion
            
            if "aggressive" in query.lower() and "sale" in query.lower():
                return 0.055  # Higher conversion for aggressive sales
            elif "premium" in query.lower():
                return 0.025  # Lower conversion for premium
            elif "holiday" in query.lower():
                return 0.045  # Higher for holiday campaigns
            else:
                return base_rate
        except:
            return 0.035
    
    def _assess_financial_risk(self, roi_metrics: Dict, budget_analysis: Dict, query: str) -> Dict[str, Any]:
        """Assess financial risk with comprehensive factors"""
        try:
            risk_score = 0.0
            risk_factors = []
            
            # ROI-based risk
            roi = roi_metrics.get('projected_roi', 0)
            if roi < 15:
                risk_score += 0.3
                risk_factors.append("Low projected ROI below industry standards")
            elif roi > 50:
                risk_score += 0.2
                risk_factors.append("Unusually high ROI projection may be unrealistic")
            
            # Budget-based risk
            budget = budget_analysis.get('optimal_budget', 0)
            if budget > 50000:
                risk_score += 0.2
                risk_factors.append("High budget increases financial exposure")
            
            # Query-based risk
            if "aggressive" in query.lower():
                risk_score += 0.1
                risk_factors.append("Aggressive campaigns carry higher execution risk")
            
            # Risk assessment
            if risk_score <= 0.2:
                risk_level = "Low"
            elif risk_score <= 0.4:
                risk_level = "Medium"
            else:
                risk_level = "High"
            
            return {
                "risk_assessment": risk_level,
                "risk_score": round(risk_score, 2),
                "risk_factors": risk_factors[:3],  # Top 3 risk factors
                "mitigation_strategies": self._generate_mitigation_strategies(risk_level)
            }
            
        except Exception:
            return {
                "risk_assessment": "Medium",
                "risk_score": 0.25,
                "risk_factors": ["Standard campaign risk factors"],
                "mitigation_strategies": ["Monitor performance metrics closely"]
            }
    
    def _generate_mitigation_strategies(self, risk_level: str) -> List[str]:
        """Generate risk mitigation strategies"""
        base_strategies = [
            "Implement A/B testing for ad creatives and landing pages",
            "Implement real-time performance monitoring and budget reallocation"
        ]
        
        if risk_level == "High":
            base_strategies.extend([
                "Phase budget release based on early performance indicators",
                "Establish clear performance thresholds for campaign continuation"
            ])
        elif risk_level == "Medium":
            base_strategies.extend([
                "Maintain 10% contingency budget for optimization opportunities",
                "Set up automated bid adjustments based on performance thresholds"
            ])
        else:
            base_strategies.append("Regular weekly performance reviews and optimizations")
        
        return base_strategies
    
    def _allocate_channel_budgets(self, total_budget: float, query: str) -> Dict[str, float]:
        """Allocate budget across marketing channels"""
        try:
            total_budget = self._safe_float(total_budget)
            media_budget = total_budget * 0.65  # 65% for media spend
            
            # Base allocation
            allocations = {
                "email": 0.15,
                "social": 0.25,
                "search": 0.30,
                "display": 0.20,
                "content": 0.10
            }
            
            # Adjust based on query
            if "aggressive" in query.lower():
                allocations["social"] += 0.05
                allocations["display"] += 0.05
                allocations["content"] -= 0.10
            elif "premium" in query.lower():
                allocations["content"] += 0.10
                allocations["search"] += 0.05
                allocations["display"] -= 0.15
            
            # Calculate actual budgets
            channel_budgets = {}
            for channel, percentage in allocations.items():
                channel_budgets[channel] = round(media_budget * percentage, 2)
            
            return channel_budgets
            
        except Exception:
            budget = self._safe_float(total_budget) * 0.65
            return {
                "email": round(budget * 0.2, 2),
                "social": round(budget * 0.3, 2),
                "search": round(budget * 0.3, 2),
                "display": round(budget * 0.2, 2)
            }
    
    def _analyze_channel_costs(self, channel_budgets: Dict[str, float]) -> Dict[str, Dict]:
        """Analyze cost efficiency for each channel"""
        try:
            # Typical cost per conversion by channel
            channel_cpc = {
                "email": 10, "social": 60, "search": 31.25,
                "display": 53.33, "content": 40
            }
            
            analysis = {}
            for channel, budget in channel_budgets.items():
                cpc = channel_cpc.get(channel, 45)
                estimated_conversions = int(budget / cpc)
                efficiency_score = 100 / cpc  # Higher score = more efficient
                
                analysis[channel] = {
                    "estimated_conversions": estimated_conversions,
                    "cost_per_conversion": cpc,
                    "efficiency_score": round(efficiency_score, 1)
                }
            
            return analysis
            
        except Exception:
            return {"email": {"estimated_conversions": 50, "cost_per_conversion": 20, "efficiency_score": 5.0}}
    
    def _calculate_break_even(self, budget: float, margin_per_unit: float) -> int:
        """Calculate break-even point in units"""
        try:
            margin = self._safe_float(margin_per_unit)
            budget = self._safe_float(budget)
            return int(budget / margin) if margin > 0 else 999
        except:
            return 100
    
    def _estimate_break_even_timeline(self, roi: float) -> str:
        """Estimate timeline to break even"""
        try:
            if roi >= 30:
                return "2-3 months"
            elif roi >= 20:
                return "3-4 months"
            elif roi >= 10:
                return "4-6 months"
            else:
                return "6+ months or may not break even"
        except:
            return "3-4 months"
    
    def _create_budget_utilization_plan(self, budget: float) -> Dict[str, Any]:
        """Create budget utilization timeline"""
        try:
            budget = self._safe_float(budget)
            return {
                "week_1": round(budget * 0.4, 2),
                "week_2_3": round(budget * 0.35, 2),
                "week_4_plus": round(budget * 0.25, 2),
                "utilization_strategy": "Front-loaded spending for maximum early impact"
            }
        except:
            return {"week_1": 8000, "week_2_3": 7000, "week_4_plus": 5000}
    
    def _calculate_cpa_target(self, budget: float, customers: int) -> float:
        """Calculate target cost per acquisition"""
        try:
            return round(self._safe_float(budget) / max(1, self._safe_int(customers)), 2)
        except:
            return 150.0
    
    def _calculate_success_probability(self, roi_metrics: Dict, risk_analysis: Dict) -> float:
        """Calculate probability of campaign success"""
        try:
            base_probability = 0.7
            roi = roi_metrics.get('projected_roi', 20)
            risk_score = risk_analysis.get('risk_score', 0.2)
            
            # Adjust based on ROI
            if roi > 25:
                base_probability += 0.15
            elif roi < 15:
                base_probability -= 0.15
            
            # Adjust based on risk
            base_probability -= risk_score
            
            return max(0.1, min(0.95, base_probability))
        except:
            return 0.75
    
    def _calculate_budget_efficiency(self, roi_metrics: Dict, budget_analysis: Dict) -> float:
        """Calculate budget efficiency score"""
        try:
            roi = roi_metrics.get('projected_roi', 20)
            return min(1.0, roi / 50.0)  # Efficiency based on ROI
        except:
            return 0.4
    
    def _suggest_budget_reallocation(self, channel_budgets: Dict[str, float]) -> Dict[str, str]:
        """Suggest budget reallocation opportunities"""
        try:
            suggestions = {}
            # Simple suggestions based on typical performance
            if channel_budgets.get('email', 0) > 0:
                suggestions['email'] = "Increase by 10% (high conversion rate)"
            if channel_budgets.get('social', 0) > 0:
                suggestions['social'] = "Optimize creative for better engagement"
            return suggestions
        except:
            return {"email": "Consider increasing allocation", "social": "Monitor performance closely"}
    
    def _make_approval_decision(self, roi: float, risk_score: float) -> str:
        """Make budget approval decision"""
        try:
            if roi >= self.roi_threshold and risk_score <= 0.3:
                return "approved"
            elif roi >= self.roi_threshold * 0.75:
                return "approved_conditional"
            else:
                return "rejected_insufficient_roi"
        except:
            return "approved_conditional"
    
    def _suggest_budget_adjustments(self, roi_metrics: Dict, approval_status: str) -> List[str]:
        """Suggest budget adjustments based on analysis"""
        if approval_status == "rejected_insufficient_roi":
            return [
                "Reduce target audience size to improve conversion rates",
                "Increase focus on higher-performing channels",
                "Consider phased campaign approach to reduce initial investment"
            ]
        elif approval_status == "approved_conditional":
            return [
                "Implement strict performance monitoring",
                "Prepare budget reallocation strategies"
            ]
        else:
            return []
    
    def _suggest_financing_options(self, budget: float) -> List[str]:
        """Suggest financing options for the campaign"""
        return [
            "Internal marketing budget allocation",
            "Performance-based budget with milestone releases",
            "Cross-departmental budget collaboration",
            "Revenue-based campaign financing",
            "Phased budget release based on early performance indicators"
        ]
    
    def _generate_roi_optimization_tips(self) -> List[str]:
        """Generate ROI optimization recommendations"""
        return [
            "Focus initial spend on highest-converting channels",
            "Implement dynamic budget reallocation based on real-time performance",
            "Use customer lifetime value to optimize acquisition costs",
            "Prioritize high-value customer segments for maximum ROI impact",
            "Consider installment payment options to reduce purchase friction"
        ]
    
    def _calculate_finance_confidence(self, roi_metrics: Dict, risk_analysis: Dict) -> float:
        """Calculate confidence in financial analysis"""
        try:
            base_confidence = 0.8
            risk_score = risk_analysis.get('risk_score', 0.2)
            
            # Adjust confidence based on risk
            confidence = base_confidence - (risk_score * 0.5)
            
            return max(0.5, min(0.95, confidence))
        except:
            return 0.75
    
    def _generate_financial_reasoning(self, roi_metrics: Dict, risk_analysis: Dict, approval_status: str) -> str:
        """Generate comprehensive financial reasoning"""
        try:
            roi = roi_metrics.get('projected_roi', 0)
            revenue = roi_metrics.get('projected_revenue', 0)
            risk_level = risk_analysis.get('risk_assessment', 'Medium')
            
            reasoning = f"Financial Analysis Reasoning:\n"
            reasoning += f"• ROI Projection: {roi}% (threshold: {self.roi_threshold}%)\n"
            reasoning += f"• Revenue Forecast: ${revenue:,.2f} from projected customer acquisitions\n"
            reasoning += f"• Risk Assessment: {risk_level} risk based on market and execution factors\n"
            reasoning += f"• Recommendation: {approval_status.replace('_', ' ').title()} - "
            
            if approval_status == "approved":
                reasoning += "Strong financial metrics support campaign execution"
            elif approval_status == "approved_conditional":
                reasoning += "Acceptable metrics with monitoring requirements"
            else:
                reasoning += "Financial metrics challenge campaign viability"
                
            return reasoning
            
        except Exception:
            return "Comprehensive financial analysis completed with risk-adjusted projections"
    
    def _get_fallback_financial_analysis(self, query: str, product: str) -> Dict[str, Any]:
        """Fallback financial analysis when main analysis fails"""
        return {
            "agent": "Enhanced Finance Agent (Fallback)",
            "projected_roi": 22.0,
            "projected_revenue": 45000.0,
            "projected_customers": 180,
            "approved_budget": 20000.0,
            "risk_assessment": "Medium",
            "success_probability": 0.75,
            "approval_status": "approved_conditional",
            "reasoning": "Fallback financial analysis - conservative estimates applied due to calculation error",
            "confidence_level": 0.6
        }
    
    async def negotiate_with_agents(self, proposal: Dict, other_agents_data: Dict) -> Dict[str, Any]:
        """Negotiate budget with other agents"""
        try:
            # Adjust budget based on inventory constraints
            inventory_data = other_agents_data.get('Inventory', {})
            if inventory_data.get('stock_status') == 'limited':
                # Reduce budget for limited inventory
                current_budget = proposal.get('approved_budget', 20000)
                proposal['approved_budget'] = self._safe_float(current_budget) * 0.8
                proposal['budget_adjustment_reason'] = "Reduced due to inventory limitations"
            
            # Adjust based on creative requirements
            creative_data = other_agents_data.get('Creative', {})
            creative_budget = creative_data.get('estimated_budget', {}).get('total_creative_budget', 0)
            if creative_budget > proposal.get('approved_budget', 20000) * 0.25:
                proposal['creative_budget_warning'] = "Creative budget exceeds 25% threshold"
            
            proposal['negotiation_round'] = proposal.get('negotiation_round', 0) + 1
            proposal['last_adjustment'] = datetime.now().isoformat()
            
            return proposal
            
        except Exception as e:
            logger.error(f"Finance negotiation error: {e}")
            return proposal
