import json
from typing import Dict, Any, List
import math

class FinanceAgent:
    """Enhanced Finance Agent with budget analysis and ROI projections"""
    
    def __init__(self):
        self.agent_name = "Finance"
        self.min_roi_threshold = 0.20  # 20% minimum ROI
        self.risk_tolerance = 0.15     # 15% buffer for risk
        self.negotiation_history = []
        
    def analyze(self, context, creative_proposal: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze financial feasibility of creative proposal"""
        print(f"💰 {self.agent_name} Agent: Analyzing financial feasibility...")
        
        budget_needed = creative_proposal.get("estimated_budget_needed", 30000)
        available_budget = context.budget
        target_segment = creative_proposal.get("target_segment", {})
        
        # Calculate ROI projections
        roi_analysis = self._calculate_roi_projection(
            budget_needed, target_segment, creative_proposal
        )
        
        # Assess budget feasibility
        budget_analysis = self._assess_budget_feasibility(
            budget_needed, available_budget
        )
        
        # Risk assessment
        risk_assessment = self._assess_financial_risk(
            budget_needed, available_budget, roi_analysis
        )
        
        # Make approval decision
        approval_decision = self._make_approval_decision(
            budget_analysis, roi_analysis, risk_assessment
        )
        
        result = {
            "approval": approval_decision["status"],
            "budget_needed": budget_needed,
            "available_budget": available_budget,
            "budget_utilization": (budget_needed / available_budget) * 100,
            "projected_roi": roi_analysis["roi_percentage"],
            "projected_revenue": roi_analysis["projected_revenue"],
            "profit_margin": roi_analysis["profit_margin"],
            "risk_level": risk_assessment["risk_level"],
            "confidence_score": approval_decision["confidence"],
            "recommendations": approval_decision["recommendations"],
            "summary": self._generate_summary(approval_decision, budget_analysis, roi_analysis)
        }
        
        print(f"✓ Budget Status: {approval_decision['status'].upper()}")
        print(f"✓ Projected ROI: {roi_analysis['roi_percentage']:.1f}%")
        print(f"✓ Risk Level: {risk_assessment['risk_level'].upper()}")
        
        return result
    
    def negotiate(self, creative_proposal: Dict[str, Any], context, round_number: int) -> Dict[str, Any]:
        """Negotiate budget constraints with creative agent"""
        print(f"🤝 {self.agent_name} Agent: Negotiating budget (Round {round_number})...")
        
        budget_needed = creative_proposal.get("estimated_budget_needed", 30000)
        max_acceptable_budget = context.budget * 0.85  # Reserve 15% buffer
        
        if budget_needed > max_acceptable_budget:
            # Propose budget reduction
            suggested_budget = max_acceptable_budget
            reduction_percentage = ((budget_needed - suggested_budget) / budget_needed) * 100
            
            feedback = {
                "constraint_type": "budget_constraint",
                "max_budget": suggested_budget,
                "required_reduction": budget_needed - suggested_budget,
                "reduction_percentage": reduction_percentage,
                "suggestions": [
                    "Focus on 2-3 high-ROI channels instead of broad approach",
                    "Reduce campaign duration to optimize spend",
                    "Leverage organic content and partnerships",
                    "Phase campaign launch to spread costs"
                ]
            }
            
            print(f"✓ Requesting {reduction_percentage:.1f}% budget reduction")
            return feedback
        
        return {"constraint_type": "budget_approved", "message": "Budget within acceptable limits"}
    
    def final_validation(self, final_strategy: Dict[str, Any], context) -> Dict[str, Any]:
        """Final validation of the negotiated strategy"""
        print(f"✓ {self.agent_name} Agent: Final budget validation...")
        
        final_budget = final_strategy.get("estimated_budget_needed", context.budget * 0.5)
        
        # Recalculate with final numbers
        final_roi = self._calculate_final_roi(final_budget, context)
        
        if final_roi["roi_percentage"] >= self.min_roi_threshold * 100:
            return {
                "approval": "approved",
                "final_budget": final_budget,
                "projected_roi": final_roi["roi_percentage"],
                "projected_revenue": final_roi["projected_revenue"],
                "summary": f"Budget approved: ${final_budget:,.2f} with {final_roi['roi_percentage']:.1f}% projected ROI"
            }
        else:
            return {
                "approval": "conditional",
                "final_budget": final_budget,
                "projected_roi": final_roi["roi_percentage"],
                "additional_budget_needed": final_budget * 0.15,
                "summary": f"Conditional approval: ROI below threshold ({final_roi['roi_percentage']:.1f}% < {self.min_roi_threshold*100}%)"
            }
    
    def _calculate_roi_projection(self, budget: float, target_segment: Dict, 
                                creative_proposal: Dict) -> Dict[str, Any]:
        """Calculate projected ROI based on target segment and budget"""
        
        segment_size = target_segment.get("size", 10000)
        avg_spend = target_segment.get("avg_spend", 800)
        conversion_rate = target_segment.get("conversion_rate", 0.10)
        
        # Campaign reach estimation (based on budget and channels)
        channels = creative_proposal.get("channels", ["Social Media"])
        channel_multiplier = len(channels) * 0.2 + 0.6  # More channels = better reach
        
        # Estimate reach as percentage of segment (budget dependent)
        reach_percentage = min((budget / 50000) * channel_multiplier, 0.3)  # Cap at 30%
        estimated_reach = int(segment_size * reach_percentage)
        
        # Calculate conversions and revenue
        estimated_conversions = int(estimated_reach * conversion_rate)
        projected_revenue = estimated_conversions * avg_spend
        
        # Calculate profit (assume 30% margin on products)
        cost_of_goods = projected_revenue * 0.7
        gross_profit = projected_revenue - cost_of_goods
        net_profit = gross_profit - budget
        
        roi_percentage = (net_profit / budget) * 100 if budget > 0 else 0
        profit_margin = (net_profit / projected_revenue) * 100 if projected_revenue > 0 else 0
        
        return {
            "estimated_reach": estimated_reach,
            "estimated_conversions": estimated_conversions,
            "projected_revenue": projected_revenue,
            "gross_profit": gross_profit,
            "net_profit": net_profit,
            "roi_percentage": roi_percentage,
            "profit_margin": profit_margin
        }
    
    def _assess_budget_feasibility(self, budget_needed: float, available_budget: float) -> Dict[str, Any]:
        """Assess if the budget is feasible"""
        utilization = (budget_needed / available_budget) * 100
        
        if utilization <= 70:
            feasibility = "excellent"
            risk = "low"
        elif utilization <= 85:
            feasibility = "good"
            risk = "moderate"
        elif utilization <= 100:
            feasibility = "acceptable"
            risk = "high"
        else:
            feasibility = "over_budget"
            risk = "very_high"
        
        return {
            "feasibility": feasibility,
            "utilization_percentage": utilization,
            "remaining_budget": max(0, available_budget - budget_needed),
            "risk": risk
        }
    
    def _assess_financial_risk(self, budget_needed: float, available_budget: float, 
                              roi_analysis: Dict) -> Dict[str, Any]:
        """Assess overall financial risk"""
        
        risk_factors = []
        risk_score = 0
        
        # Budget utilization risk
        utilization = (budget_needed / available_budget) * 100
        if utilization > 90:
            risk_factors.append("High budget utilization")
            risk_score += 3
        elif utilization > 75:
            risk_score += 2
        elif utilization > 60:
            risk_score += 1
        
        # ROI risk
        projected_roi = roi_analysis["roi_percentage"]
        if projected_roi < self.min_roi_threshold * 100:
            risk_factors.append("ROI below threshold")
            risk_score += 4
        elif projected_roi < 30:
            risk_score += 2
        elif projected_roi < 50:
            risk_score += 1
        
        # Revenue risk
        if roi_analysis["projected_revenue"] < budget_needed * 1.5:
            risk_factors.append("Low revenue projection")
            risk_score += 2
        
        # Determine risk level
        if risk_score <= 2:
            risk_level = "low"
        elif risk_score <= 4:
            risk_level = "moderate"
        elif risk_score <= 6:
            risk_level = "high"
        else:
            risk_level = "very_high"
        
        return {
            "risk_level": risk_level,
            "risk_score": risk_score,
            "risk_factors": risk_factors,
            "risk_mitigation": self._suggest_risk_mitigation(risk_factors)
        }
    
    def _suggest_risk_mitigation(self, risk_factors: List[str]) -> List[str]:
        """Suggest risk mitigation strategies"""
        mitigations = []
        
        if "High budget utilization" in risk_factors:
            mitigations.extend([
                "Reserve 15% of budget for contingencies",
                "Phase campaign launch to control spending"
            ])
        
        if "ROI below threshold" in risk_factors:
            mitigations.extend([
                "Focus on highest-converting channels first",
                "Implement A/B testing to optimize performance",
                "Consider reducing campaign scope"
            ])
        
        if "Low revenue projection" in risk_factors:
            mitigations.extend([
                "Target higher-value customer segments",
                "Include upselling and cross-selling strategies"
            ])
        
        return mitigations
    
    def _make_approval_decision(self, budget_analysis: Dict, roi_analysis: Dict, 
                               risk_assessment: Dict) -> Dict[str, Any]:
        """Make final approval decision based on all factors"""
        
        # Decision matrix
        score = 0
        recommendations = []
        
        # Budget feasibility scoring
        feasibility = budget_analysis["feasibility"]
        if feasibility == "excellent":
            score += 3
        elif feasibility == "good":
            score += 2
        elif feasibility == "acceptable":
            score += 1
        else:
            score -= 2
            recommendations.append("Reduce budget requirements")
        
        # ROI scoring
        roi = roi_analysis["roi_percentage"]
        if roi >= 50:
            score += 3
        elif roi >= 30:
            score += 2
        elif roi >= self.min_roi_threshold * 100:
            score += 1
        else:
            score -= 2
            recommendations.append("Improve ROI projections")
        
        # Risk scoring
        risk_level = risk_assessment["risk_level"]
        if risk_level == "low":
            score += 2
        elif risk_level == "moderate":
            score += 1
        elif risk_level == "high":
            score -= 1
        else:
            score -= 3
            recommendations.extend(risk_assessment["risk_mitigation"])
        
        # Final decision
        if score >= 4:
            status = "approved"
            confidence = 0.85 + (score - 4) * 0.03
        elif score >= 2:
            status = "conditional"
            confidence = 0.65 + (score - 2) * 0.1
            recommendations.append("Address moderate concerns before launch")
        else:
            status = "rejected"
            confidence = 0.3
            recommendations.insert(0, "Major revisions required")
        
        return {
            "status": status,
            "confidence": min(confidence, 0.95),
            "score": score,
            "recommendations": recommendations[:3]  # Top 3 recommendations
        }
    
    def _generate_summary(self, approval: Dict, budget: Dict, roi: Dict) -> str:
        """Generate human-readable summary"""
        status = approval["status"]
        confidence = approval["confidence"] * 100
        
        if status == "approved":
            return f"APPROVED ({confidence:.0f}% confidence): Budget ${budget['utilization_percentage']:.0f}% utilized, {roi['roi_percentage']:.1f}% ROI projected"
        elif status == "conditional":
            return f"CONDITIONAL ({confidence:.0f}% confidence): Requires {', '.join(approval['recommendations'][:2])}"
        else:
            return f"REJECTED ({confidence:.0f}% confidence): {', '.join(approval['recommendations'][:2])}"
    
    def _calculate_final_roi(self, final_budget: float, context) -> Dict[str, Any]:
        """Calculate final ROI with adjusted budget"""
        # Simplified final ROI calculation
        estimated_conversions = final_budget / 200  # Assume $200 per conversion
        avg_order_value = 800  # Default AOV
        projected_revenue = estimated_conversions * avg_order_value
        net_profit = projected_revenue * 0.3 - final_budget  # 30% margin
        roi_percentage = (net_profit / final_budget) * 100 if final_budget > 0 else 0
        
        return {
            "projected_revenue": projected_revenue,
            "net_profit": net_profit,
            "roi_percentage": roi_percentage
        }

# Legacy function for backward compatibility
def finance_agent(plan, budget):
    """Legacy function wrapper"""
    agent = FinanceAgent()
    
    # Extract budget info from creative plan if it's a dict
    if isinstance(plan, dict):
        budget_needed = plan.get("estimated_budget_needed", 30000)
    else:
        budget_needed = 30000  # Default
    
    if budget >= budget_needed:
        return f"Finance Agent: APPROVED — Budget sufficient (${budget:,.2f} available, ${budget_needed:,.2f} needed)"
    else:
        shortfall = budget_needed - budget
        return f"Finance Agent: CONDITIONAL — Budget shortfall of ${shortfall:,.2f} (${budget:,.2f} available, ${budget_needed:,.2f} needed)"