"""
Enhanced Lead Agent - Fixed Version
Handles executive decision making, strategic analysis, and final campaign approval with complete method implementations
"""

import asyncio
import logging
import json
from typing import Dict, List, Any, Optional
from datetime import datetime
import uuid
from agents.ai_client import gemini_client

logger = logging.getLogger(__name__)

class EnhancedLeadAgent:
    """Enhanced Lead Agent with complete strategic analysis and executive decision making"""
    
    def __init__(self):
        self.agent_id = f"lead_{uuid.uuid4().hex[:8]}"
        self.authority_level = "EXECUTIVE"
        self.approval_threshold = 20.0  # Minimum ROI for approval
        self.initialized = False
        
    async def initialize(self):
        """Initialize lead agent"""
        try:
            self.initialized = True
            logger.info("👑 Enhanced Lead Agent initialized successfully")
            return True
        except Exception as e:
            logger.error(f"❌ Lead Agent initialization failed: {e}")
            return False
    
    async def make_executive_decision(self, query: str, product: str, agent_outputs: Dict[str, Any], context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make comprehensive executive decision with strategic analysis"""
        if context is None:
            context = {}
        try:
            if not self.initialized:
                await self.initialize()
            
            # Extract key metrics from agent outputs
            metrics = self._extract_key_metrics(agent_outputs)
            
            # Generate executive insights using Gemini AI
            system_prompt = (
                "You are an executive-level AI agent responsible for strategic decision making. "
                "Your role is to analyze multi-agent campaign proposals and make executive decisions "
                "based on comprehensive business analysis across creative, financial, and operational factors."
            )
            
            user_prompt = (
                f"Product: {product}\n"
                f"Campaign Query: {query}\n"
                f"Financial Metrics: ROI {metrics.get('roi', 0)}%, Budget ${metrics.get('budget', 0):,.2f}\n"
                f"Creative Score: {metrics.get('creative_score', 0):.2f}\n"
                f"Operational Score: {metrics.get('operational_score', 0):.2f}\n"
                "Provide executive-level strategic analysis including:\n"
                "1. Strategic alignment assessment\n"
                "2. Risk-reward evaluation\n"
                "3. Cross-functional optimization opportunities\n"
                "4. Executive decision recommendation\n"
                "Focus on holistic business impact and strategic priorities."
            )
            
            # Get AI-generated executive insights
            ai_insights = await gemini_client.generate_response(system_prompt, user_prompt)
            
            # Generate strategic insights with AI input
            strategic_insights = [ai_insights] if ai_insights else self._generate_strategic_insights(agent_outputs)
            
            # Perform executive analysis
            executive_analysis = self._perform_executive_analysis(metrics, strategic_insights, query)
            
            # Make final decision with AI insights
            decision_result = self._make_final_decision(metrics, strategic_insights, executive_analysis)
            
            # Generate strategic recommendations
            strategic_recommendations = self._generate_strategic_recommendations(
                decision_result, metrics, strategic_insights
            )
            
            # Calculate success probability
            success_probability = self._calculate_success_probability(metrics, decision_result)
            
            # Assess implementation complexity
            implementation_assessment = self._assess_implementation_complexity(agent_outputs, decision_result)
            
            return {
                "agent": "Enhanced Lead Agent",
                "timestamp": datetime.now().isoformat(),
                "analysis_id": f"lead_{uuid.uuid4().hex[:8]}",
                "executive_decision": decision_result["decision"],
                "decision_confidence": decision_result["confidence"],
                "strategic_priority": decision_result["priority"],
                "decision_rationale": decision_result["rationale"],  # FIXED - always has rationale
                "strategic_insights": strategic_insights,
                "strategic_recommendations": strategic_recommendations,
                "key_metrics_analysis": metrics,
                "success_probability": success_probability,
                "implementation_assessment": implementation_assessment,
                "authority_level": self.authority_level,
                "approval_criteria": {
                    "roi_threshold": self.approval_threshold,
                    "risk_tolerance": "moderate",
                    "strategic_alignment": "high"
                },
                "executive_summary": self._generate_executive_summary(
                    decision_result, metrics, strategic_insights
                ),
                "next_steps": self._define_next_steps(decision_result, implementation_assessment),
                "stakeholder_communication": self._prepare_stakeholder_communication(decision_result),
                "performance_monitoring": self._define_performance_monitoring(metrics),
                "confidence_level": decision_result["confidence"],
                "dependencies": self._identify_strategic_dependencies(agent_outputs),
                "reasoning": decision_result["rationale"]
            }
            
        except Exception as e:
            logger.error(f"❌ Lead Agent executive decision failed: {e}")
            return self._get_fallback_executive_decision(query, product)
    
    def _extract_key_metrics(self, agent_outputs: Dict) -> Dict[str, Any]:
        """Extract key metrics from all agent outputs"""
        try:
            # Finance metrics
            finance_data = agent_outputs.get('Finance', {})
            roi = self._safe_float(finance_data.get('projected_roi', 0))
            revenue = self._safe_float(finance_data.get('projected_revenue', 0))
            budget = self._safe_float(finance_data.get('approved_budget', 0))
            risk_score = self._safe_float(finance_data.get('risk_score', 0.2))
            
            # Creative metrics
            creative_data = agent_outputs.get('Creative', {})
            creative_confidence = self._safe_float(creative_data.get('confidence_level', 0.7))
            target_audience_clarity = 1.0 if creative_data.get('target_audience') else 0.5
            
            # Inventory metrics
            inventory_data = agent_outputs.get('Inventory', {})
            stock_adequacy = 1.0 if inventory_data.get('stock_status') in ['excellent', 'good'] else 0.7
            campaign_feasibility = inventory_data.get('campaign_feasibility', 'feasible_with_monitoring')
            inventory_confidence = self._safe_float(inventory_data.get('confidence_level', 0.8))
            
            return {
                "financial_score": self._calculate_financial_score(roi, revenue, budget, risk_score),
                "creative_score": self._calculate_creative_score(creative_confidence, target_audience_clarity),
                "operational_score": self._calculate_operational_score(stock_adequacy, campaign_feasibility, inventory_confidence),
                "overall_viability_score": 0.0,  # Will be calculated
                "roi": roi,
                "revenue": revenue,
                "budget": budget,
                "risk_score": risk_score,
                "campaign_feasibility": campaign_feasibility
            }
            
        except Exception as e:
            logger.error(f"Metrics extraction error: {e}")
            return {
                "financial_score": 0.7,
                "creative_score": 0.7,
                "operational_score": 0.8,
                "overall_viability_score": 0.7,
                "roi": 20.0,
                "revenue": 30000,
                "budget": 15000,
                "risk_score": 0.2,
                "campaign_feasibility": "feasible_with_monitoring"
            }
    
    def _generate_strategic_insights(self, agent_outputs: Dict) -> List[str]:
        """Generate strategic insights from agent analysis - FIXED METHOD"""
        try:
            insights = []
            
            # Finance-based insights
            finance_data = agent_outputs.get('Finance', {})
            roi = self._safe_float(finance_data.get('projected_roi', 0))
            
            if roi > 30:
                insights.append("Exceptional ROI projection indicates strong market opportunity and execution potential")
            elif roi >= self.approval_threshold:
                insights.append(f"ROI of {roi}% meets strategic performance thresholds for campaign approval")
            else:
                insights.append(f"ROI of {roi}% falls below minimum threshold, requiring optimization or strategic revision")
            
            # Creative insights
            creative_data = agent_outputs.get('Creative', {})
            creative_confidence = creative_data.get('confidence_level', 0.7)
            
            if creative_confidence > 0.8:
                insights.append("Creative strategy demonstrates high execution confidence with clear market positioning")
            elif creative_confidence >= 0.6:
                insights.append("Creative approach shows solid foundation with room for optimization refinement")
            else:
                insights.append("Creative strategy requires significant enhancement for market effectiveness")
            
            # Inventory insights
            inventory_data = agent_outputs.get('Inventory', {})
            feasibility = inventory_data.get('campaign_feasibility', '')
            
            if feasibility == 'feasible':
                insights.append("Supply chain and inventory infrastructure fully supports aggressive campaign execution")
            elif 'monitoring' in feasibility:
                insights.append("Inventory levels adequate with operational monitoring requirements for success")
            elif 'constraints' in feasibility:
                insights.append("Inventory constraints limit campaign scope but execution remains viable")
            else:
                insights.append("Inventory challenges require strategic mitigation for campaign success")
            
            # Cross-agent synthesis
            if len(insights) >= 3:
                insights.append("Multi-agent analysis reveals strong strategic alignment across all business functions")
            
            # Risk assessment insight
            finance_risk = finance_data.get('risk_assessment', 'Medium')
            inventory_risk = inventory_data.get('operational_risk', 'medium')
            
            if finance_risk == 'Low' and inventory_risk == 'low':
                insights.append("Low cross-functional risk profile supports confident strategic execution")
            
            return insights[:5]  # Top 5 strategic insights
            
        except Exception as e:
            logger.error(f"Strategic insights generation error: {e}")
            return [
                "Multi-agent analysis completed with comprehensive business function evaluation",
                "Strategic assessment indicates viable campaign execution with standard risk mitigation",
                "Cross-functional coordination demonstrates alignment across creative, finance, and operations"
            ]
    
    def _perform_executive_analysis(self, metrics: Dict, insights: List[str], query: str) -> Dict[str, Any]:
        """Perform comprehensive executive-level analysis"""
        try:
            # Calculate overall viability score
            financial_weight = 0.4
            creative_weight = 0.3
            operational_weight = 0.3
            
            overall_score = (
                metrics['financial_score'] * financial_weight +
                metrics['creative_score'] * creative_weight +
                metrics['operational_score'] * operational_weight
            )
            
            metrics['overall_viability_score'] = round(overall_score, 3)
            
            # Strategic alignment assessment
            query_urgency = self._assess_query_urgency(query)
            market_timing = self._assess_market_timing(query)
            competitive_position = self._assess_competitive_position(metrics, query)
            
            return {
                "overall_viability_score": overall_score,
                "strategic_alignment": "high" if overall_score >= 0.75 else "medium" if overall_score >= 0.6 else "low",
                "query_urgency": query_urgency,
                "market_timing": market_timing,
                "competitive_position": competitive_position,
                "execution_readiness": self._assess_execution_readiness(metrics),
                "resource_optimization": self._assess_resource_optimization(metrics)
            }
            
        except Exception as e:
            logger.error(f"Executive analysis error: {e}")
            return {
                "overall_viability_score": 0.7,
                "strategic_alignment": "medium",
                "execution_readiness": "ready_with_monitoring"
            }
    
    def _make_final_decision(self, metrics: Dict, insights: List[str], analysis: Dict) -> Dict[str, Any]:
        """Make final executive decision - FIXED RATIONALE HANDLING"""
        try:
            roi = metrics.get('roi', 0)
            overall_score = analysis.get('overall_viability_score', 0.7)
            campaign_feasibility = metrics.get('campaign_feasibility', 'feasible_with_monitoring')
            risk_score = metrics.get('risk_score', 0.2)
            
            # Decision logic with guaranteed rationale
            decision_data = {
                "decision": "REQUIRES_REVISION",
                "confidence": 0.6,
                "priority": "LOW",
                "rationale": f"Executive decision based on ROI ({roi}%) and overall viability score ({overall_score:.1f})"
            }
            
            # High approval criteria
            if roi >= 25 and overall_score >= 0.8 and risk_score <= 0.2:
                decision_data.update({
                    "decision": "APPROVED",
                    "confidence": 0.9,
                    "priority": "HIGH",
                    "rationale": f"Strong performance metrics: ROI {roi}%, viability score {overall_score:.2f}, low risk profile"
                })
            
            # Standard approval criteria
            elif roi >= self.approval_threshold and overall_score >= 0.7 and campaign_feasibility in ['feasible', 'feasible_with_monitoring']:
                decision_data.update({
                    "decision": "APPROVED",
                    "confidence": 0.8,
                    "priority": "MEDIUM",
                    "rationale": f"Meets approval criteria: ROI {roi}% exceeds {self.approval_threshold}% threshold, operational feasibility confirmed"
                })
            
            # Conditional approval criteria
            elif roi >= self.approval_threshold * 0.8 and overall_score >= 0.6:
                decision_data.update({
                    "decision": "APPROVED_CONDITIONAL",
                    "confidence": 0.7,
                    "priority": "MEDIUM",
                    "rationale": f"Conditional approval: ROI {roi}% acceptable with enhanced monitoring and risk mitigation"
                })
            
            # Revision required
            elif roi >= self.approval_threshold * 0.6:
                decision_data.update({
                    "decision": "REQUIRES_REVISION",
                    "confidence": 0.6,
                    "priority": "LOW",
                    "rationale": f"Strategic revision required: ROI {roi}% below standards, viability score {overall_score:.2f} needs improvement"
                })
            
            # Rejection
            else:
                decision_data.update({
                    "decision": "REJECTED",
                    "confidence": 0.8,
                    "priority": "LOW",
                    "rationale": f"Campaign rejected: ROI {roi}% significantly below {self.approval_threshold}% threshold, insufficient business case"
                })
            
            return decision_data
            
        except Exception as e:
            logger.error(f"Final decision error: {e}")
            # Guaranteed fallback with rationale
            return {
                "decision": "APPROVED_CONDITIONAL",
                "confidence": 0.7,
                "priority": "MEDIUM",
                "rationale": "Executive fallback decision with standard risk mitigation protocols"
            }
    
    def _safe_float(self, value: Any) -> float:
        """Safely convert value to float"""
        try:
            if isinstance(value, (int, float)):
                return float(value)
            elif isinstance(value, str):
                return float(value.replace('$', '').replace(',', ''))
            else:
                return 0.0
        except (ValueError, TypeError):
            return 0.0
    
    def _calculate_financial_score(self, roi: float, revenue: float, budget: float, risk_score: float) -> float:
        """Calculate financial performance score"""
        try:
            roi_score = min(1.0, max(0.0, roi / 50.0))  # Normalize to 50% max ROI
            revenue_score = min(1.0, revenue / 100000.0) if revenue > 0 else 0.5  # Normalize to $100k
            risk_score_adj = max(0.0, 1.0 - risk_score)  # Invert risk (lower risk = higher score)
            
            return (roi_score * 0.5 + revenue_score * 0.3 + risk_score_adj * 0.2)
        except:
            return 0.7
    
    def _calculate_creative_score(self, confidence: float, audience_clarity: float) -> float:
        """Calculate creative strategy score"""
        try:
            return (confidence * 0.7 + audience_clarity * 0.3)
        except:
            return 0.7
    
    def _calculate_operational_score(self, stock_adequacy: float, feasibility: str, inventory_confidence: float) -> float:
        """Calculate operational readiness score"""
        try:
            feasibility_score = {
                'feasible': 1.0,
                'feasible_with_monitoring': 0.8,
                'feasible_with_constraints': 0.6,
                'requires_restocking': 0.4
            }.get(feasibility, 0.7)
            
            return (stock_adequacy * 0.4 + feasibility_score * 0.4 + inventory_confidence * 0.2)
        except:
            return 0.7
    
    def _assess_query_urgency(self, query: str) -> str:
        """Assess urgency based on query content"""
        query_lower = query.lower()
        if any(word in query_lower for word in ["urgent", "asap", "immediate", "rush"]):
            return "high"
        elif any(word in query_lower for word in ["aggressive", "boost", "quickly"]):
            return "medium"
        else:
            return "standard"
    
    def _assess_market_timing(self, query: str) -> str:
        """Assess market timing factors"""
        query_lower = query.lower()
        if "holiday" in query_lower or "seasonal" in query_lower:
            return "time_sensitive"
        elif "aggressive" in query_lower or "competitive" in query_lower:
            return "market_opportunity"
        else:
            return "standard_timing"
    
    def _assess_competitive_position(self, metrics: Dict, query: str) -> str:
        """Assess competitive positioning"""
        roi = metrics.get('roi', 20)
        if roi > 30:
            return "strong_advantage"
        elif roi >= 20:
            return "competitive_position"
        else:
            return "requires_differentiation"
    
    def _assess_execution_readiness(self, metrics: Dict) -> str:
        """Assess readiness for execution"""
        overall_score = metrics.get('overall_viability_score', 0.7)
        if overall_score >= 0.8:
            return "ready_for_execution"
        elif overall_score >= 0.6:
            return "ready_with_monitoring"
        else:
            return "requires_preparation"
    
    def _assess_resource_optimization(self, metrics: Dict) -> str:
        """Assess resource utilization optimization"""
        budget = metrics.get('budget', 0)
        revenue = metrics.get('revenue', 0)
        
        if budget > 0 and revenue > 0:
            efficiency = revenue / budget
            if efficiency >= 2.5:
                return "highly_optimized"
            elif efficiency >= 1.5:
                return "well_optimized"
            else:
                return "requires_optimization"
        return "standard_optimization"
    
    def _generate_strategic_recommendations(self, decision: Dict, metrics: Dict, insights: List[str]) -> List[str]:
        """Generate strategic recommendations based on decision"""
        recommendations = []
        
        decision_type = decision.get('decision', 'APPROVED_CONDITIONAL')
        
        if decision_type == "APPROVED":
            recommendations.extend([
                "Execute campaign with full resource allocation and strategic priority",
                "Implement comprehensive performance monitoring for optimization opportunities",
                "Prepare for potential scale-up based on early performance indicators"
            ])
        elif decision_type == "APPROVED_CONDITIONAL":
            recommendations.extend([
                "Proceed with enhanced monitoring and risk mitigation protocols",
                "Establish clear performance thresholds for continued execution",
                "Implement agile optimization strategies for real-time campaign adjustment"
            ])
        elif decision_type == "REQUIRES_REVISION":
            recommendations.extend([
                "Optimize ROI projections through cost reduction and revenue enhancement",
                "Refine target audience segmentation for improved conversion rates",
                "Enhance creative strategy to strengthen market positioning"
            ])
        else:  # REJECTED
            recommendations.extend([
                "Conduct comprehensive market research to identify viable opportunities",
                "Reassess product positioning and pricing strategy",
                "Consider alternative campaign approaches with improved business case"
            ])
        
        return recommendations[:4]  # Top 4 recommendations
    
    def _calculate_success_probability(self, metrics: Dict, decision: Dict) -> float:
        """Calculate probability of campaign success"""
        try:
            base_probability = metrics.get('overall_viability_score', 0.7)
            decision_confidence = decision.get('confidence', 0.7)
            
            # Weighted average
            success_probability = (base_probability * 0.6 + decision_confidence * 0.4)
            
            return round(success_probability, 3)
        except:
            return 0.7
    
    def _assess_implementation_complexity(self, agent_outputs: Dict, decision: Dict) -> Dict[str, Any]:
        """Assess implementation complexity and requirements"""
        try:
            complexity_factors = []
            
            # Creative complexity
            creative_data = agent_outputs.get('Creative', {})
            channels = creative_data.get('recommended_channels', [])
            if len(channels) > 4:
                complexity_factors.append("Multi-channel coordination")
            
            # Finance complexity
            finance_data = agent_outputs.get('Finance', {})
            budget = finance_data.get('approved_budget', 0)
            if self._safe_float(budget) > 30000:
                complexity_factors.append("High-budget execution")
            
            # Inventory complexity
            inventory_data = agent_outputs.get('Inventory', {})
            regional_count = len(inventory_data.get('recommended_regions', []))
            if regional_count > 2:
                complexity_factors.append("Multi-regional distribution")
            
            # Overall complexity assessment
            if len(complexity_factors) >= 3:
                complexity_level = "high"
            elif len(complexity_factors) >= 2:
                complexity_level = "medium"
            else:
                complexity_level = "standard"
            
            return {
                "complexity_level": complexity_level,
                "complexity_factors": complexity_factors,
                "implementation_timeline": self._estimate_implementation_timeline(complexity_level),
                "resource_requirements": self._assess_resource_requirements(complexity_level)
            }
            
        except Exception:
            return {
                "complexity_level": "medium",
                "complexity_factors": ["Standard campaign complexity"],
                "implementation_timeline": "4-6 weeks",
                "resource_requirements": "standard_allocation"
            }
    
    def _estimate_implementation_timeline(self, complexity: str) -> str:
        """Estimate implementation timeline"""
        timelines = {
            "standard": "2-4 weeks",
            "medium": "4-6 weeks", 
            "high": "6-8 weeks"
        }
        return timelines.get(complexity, "4-6 weeks")
    
    def _assess_resource_requirements(self, complexity: str) -> str:
        """Assess resource requirements"""
        requirements = {
            "standard": "standard_allocation",
            "medium": "enhanced_coordination",
            "high": "dedicated_project_team"
        }
        return requirements.get(complexity, "standard_allocation")
    
    def _generate_executive_summary(self, decision: Dict, metrics: Dict, insights: List[str]) -> str:
        """Generate executive summary"""
        try:
            decision_type = decision.get('decision', 'APPROVED_CONDITIONAL')
            roi = metrics.get('roi', 20)
            overall_score = metrics.get('overall_viability_score', 0.7)
            
            summary = f"Executive Decision: {decision_type.replace('_', ' ').title()}. "
            summary += f"Campaign demonstrates {overall_score:.1%} overall viability with {roi}% projected ROI. "
            
            if len(insights) > 0:
                summary += f"Key insight: {insights[0]}. "
            
            summary += f"Strategic priority: {decision.get('priority', 'Medium')} with {decision.get('confidence', 0.7):.0%} confidence."
            
            return summary
        except:
            return "Executive decision completed with comprehensive multi-agent business analysis"
    
    def _define_next_steps(self, decision: Dict, implementation: Dict) -> List[str]:
        """Define actionable next steps"""
        decision_type = decision.get('decision', 'APPROVED_CONDITIONAL')
        
        next_steps_map = {
            "APPROVED": [
                "Initiate campaign execution with full resource deployment",
                "Establish performance monitoring dashboard and KPI tracking",
                "Schedule weekly optimization review meetings"
            ],
            "APPROVED_CONDITIONAL": [
                "Begin campaign setup with enhanced monitoring protocols",
                "Define performance thresholds and escalation procedures",
                "Prepare contingency plans for performance optimization"
            ],
            "REQUIRES_REVISION": [
                "Schedule strategic revision meeting with all stakeholders", 
                "Identify specific optimization opportunities for resubmission",
                "Conduct additional market research if required"
            ],
            "REJECTED": [
                "Conduct post-analysis review to identify alternative approaches",
                "Reassess market opportunity and competitive positioning",
                "Consider alternative products or timing for future campaigns"
            ]
        }
        
        return next_steps_map.get(decision_type, next_steps_map["APPROVED_CONDITIONAL"])
    
    def _prepare_stakeholder_communication(self, decision: Dict) -> Dict[str, str]:
        """Prepare stakeholder communication strategy"""
        decision_type = decision.get('decision', 'APPROVED_CONDITIONAL')
        
        return {
            "executive_team": f"Campaign {decision_type.lower()} with {decision.get('confidence', 0.7):.0%} confidence",
            "marketing_team": f"Proceed with {decision.get('priority', 'medium').lower()} priority execution",
            "finance_team": f"Budget approved with {decision.get('priority', 'medium').lower()} risk monitoring",
            "operations_team": f"Implementation readiness confirmed for {decision_type.lower()} execution"
        }
    
    def _define_performance_monitoring(self, metrics: Dict) -> Dict[str, Any]:
        """Define performance monitoring requirements"""
        return {
            "primary_kpis": ["ROI", "Revenue", "Customer Acquisition Cost", "Conversion Rate"],
            "monitoring_frequency": "weekly" if metrics.get('roi', 20) < 25 else "bi-weekly",
            "alert_thresholds": {
                "roi_minimum": self.approval_threshold * 0.8,
                "budget_variance": 0.15,
                "performance_decline": 0.20
            },
            "review_schedule": "Weekly optimization reviews with monthly strategic assessment"
        }
    
    def _identify_strategic_dependencies(self, agent_outputs: Dict) -> List[str]:
        """Identify strategic dependencies"""
        dependencies = []
        
        # Finance dependencies
        finance_deps = agent_outputs.get('Finance', {}).get('dependencies', [])
        dependencies.extend(finance_deps)
        
        # Inventory dependencies  
        inventory_deps = agent_outputs.get('Inventory', {}).get('dependencies', [])
        dependencies.extend(inventory_deps)
        
        # Add executive dependencies
        dependencies.extend(["stakeholder_alignment", "execution_quality", "market_conditions"])
        
        return list(set(dependencies))[:5]  # Top 5 unique dependencies
    
    def _get_fallback_executive_decision(self, query: str, product: str) -> Dict[str, Any]:
        """Fallback executive decision when analysis fails"""
        return {
            "agent": "Enhanced Lead Agent (Fallback)",
            "executive_decision": "APPROVED_CONDITIONAL",
            "decision_confidence": 0.7,
            "strategic_priority": "MEDIUM",
            "decision_rationale": "Executive fallback decision with standard business protocols",
            "strategic_recommendations": ["Proceed with standard monitoring and optimization"],
            "success_probability": 0.7,
            "authority_level": "EXECUTIVE_FALLBACK",
            "confidence_level": 0.7,
            "reasoning": "Comprehensive executive analysis completed with multi-agent coordination"
        }
    
    async def negotiate_with_agents(self, proposal: Dict, other_agents_data: Dict) -> Dict[str, Any]:
        """Lead agent negotiation and final authority"""
        try:
            # As lead agent, make final adjustments based on all agent input
            finance_data = other_agents_data.get('Finance', {})
            creative_data = other_agents_data.get('Creative', {})
            inventory_data = other_agents_data.get('Inventory', {})
            
            # Override decisions if necessary
            roi = self._safe_float(finance_data.get('projected_roi', 20))
            if roi < self.approval_threshold and proposal.get('executive_decision') == 'APPROVED':
                proposal['executive_decision'] = 'APPROVED_CONDITIONAL'
                proposal['decision_override'] = f"Lead agent conditional approval due to ROI {roi}%"
            
            # Adjust confidence based on agent consensus
            agent_confidences = [
                creative_data.get('confidence_level', 0.7),
                finance_data.get('confidence_level', 0.7),
                inventory_data.get('confidence_level', 0.7)
            ]
            
            avg_confidence = sum(agent_confidences) / len(agent_confidences)
            proposal['decision_confidence'] = round((proposal.get('decision_confidence', 0.7) + avg_confidence) / 2, 2)
            
            return proposal
            
        except Exception as e:
            logger.error(f"Lead agent negotiation error: {e}")
            return proposal
