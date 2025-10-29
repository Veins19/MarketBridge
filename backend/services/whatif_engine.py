"""
Enhanced What-If Scenario Engine - AI-Powered Version
Integrates with your existing Gemini AI agents, FinBERT sentiment, and historical data
"""

import asyncio
import logging
import json
from typing import Dict, List, Any, Optional
from datetime import datetime
import uuid
from agents.ai_client import gemini_client
from models.database import insert_json_record, execute_query

logger = logging.getLogger(__name__)

class EnhancedWhatIfEngine:
    """Advanced What-If scenario engine with full AI integration"""
    
    def __init__(self):
        self.engine_id = f"whatif_{uuid.uuid4().hex[:8]}"
        
    async def generate_intelligent_scenarios(
        self, 
        base_params: Dict,
        agent_outputs: Optional[Dict] = None,
        use_full_ai: bool = True
    ) -> Dict[str, Any]:
        """Generate AI-enhanced scenarios using your complete agent system"""
        
        try:
            print(f"🎯 Generating What-If scenarios with AI integration...")
            
            # Extract parameters
            discount = base_params.get('discount', 10.0)
            duration = base_params.get('duration', 30)
            target_size = base_params.get('target_size', 1000)
            budget = base_params.get('budget', 15000)
            product = base_params.get('product', 'Default Product')
            
            # Enhanced strategy templates (improved from original)
            strategies = [
                {
                    "name": "Conservative AI-Optimized",
                    "risk_level": "Low",
                    "probability": 0.88,
                    "conversion_multiplier": 0.75,
                    "roi_multiplier": 2.4,
                    "ai_confidence": 0.92,
                    "description": "Low-risk approach with AI-optimized targeting"
                },
                {
                    "name": "Balanced AI-Enhanced", 
                    "risk_level": "Medium",
                    "probability": 0.76,
                    "conversion_multiplier": 1.1,
                    "roi_multiplier": 3.5,
                    "ai_confidence": 0.85,
                    "description": "Balanced strategy with sentiment-enhanced execution"
                },
                {
                    "name": "Aggressive AI-Powered",
                    "risk_level": "High", 
                    "probability": 0.62,
                    "conversion_multiplier": 1.5,
                    "roi_multiplier": 4.8,
                    "ai_confidence": 0.75,
                    "description": "High-potential strategy with full AI optimization"
                }
            ]
            
            # Calculate enhanced base metrics
            base_reach = target_size * (1 + (discount / 100) * 0.28)
            engagement_rate = 7 + (discount / 7) + (budget / 75000) - (duration / 140)
            
            # AI Enhancement Layer
            ai_enhancements = {
                "sentiment_boost": 0,
                "creative_multiplier": 1.0,
                "finance_adjustment": 1.0,
                "historical_factor": 1.0
            }
            
            # Integrate with your existing agent system
            if agent_outputs and use_full_ai:
                ai_enhancements = await self._extract_ai_intelligence(agent_outputs)
                engagement_rate *= (1 + ai_enhancements["sentiment_boost"])
                base_reach *= ai_enhancements["creative_multiplier"]
                
                print(f"🧠 AI Enhancement Applied:")
                print(f"   • Sentiment Boost: {ai_enhancements['sentiment_boost']:.1%}")
                print(f"   • Creative Multiplier: {ai_enhancements['creative_multiplier']:.2f}")
                print(f"   • Finance Adjustment: {ai_enhancements['finance_adjustment']:.2f}")
            
            scenarios = []
            
            for strategy in strategies:
                # Enhanced conversion calculation with AI
                conversion_rate = engagement_rate * strategy["conversion_multiplier"]
                
                # Multi-factor ROI calculation
                base_roi = ((base_reach * conversion_rate / 100) * strategy["roi_multiplier"]) / budget * 100
                final_roi = base_roi * ai_enhancements["finance_adjustment"] * ai_enhancements["historical_factor"]
                
                # Expected revenue calculation
                expected_conversions = int(base_reach * conversion_rate / 100)
                avg_order_value = budget / target_size * 12  # Estimated AOV
                expected_revenue = expected_conversions * avg_order_value
                
                # AI-enhanced insights
                ai_insights = await self._generate_ai_insights(strategy, final_roi, base_params, agent_outputs)
                
                # Risk assessment
                risk_factors = self._assess_scenario_risks(strategy, final_roi, ai_enhancements)
                
                scenario = {
                    "id": f"scenario_{uuid.uuid4().hex[:6]}",
                    "name": strategy["name"],
                    "description": strategy["description"],
                    "discount": discount,
                    "roi": round(final_roi, 1),
                    "probability": f"{int(strategy['probability']*100)}%",
                    "conversion_rate": round(conversion_rate, 2),
                    "risk_level": strategy["risk_level"],
                    "estimated_reach": int(base_reach),
                    "expected_conversions": expected_conversions,
                    "expected_revenue": round(expected_revenue, 2),
                    "cost_per_conversion": round(budget / max(1, expected_conversions), 2),
                    "ai_confidence": strategy["ai_confidence"],
                    "ai_insights": ai_insights,
                    "risk_factors": risk_factors,
                    "enhancements": {
                        "sentiment_enhanced": ai_enhancements["sentiment_boost"] > 0,
                        "creative_optimized": ai_enhancements["creative_multiplier"] > 1.0,
                        "finance_validated": agent_outputs is not None,
                        "historically_informed": ai_enhancements["historical_factor"] != 1.0
                    },
                    "recommended": final_roi >= 25 and strategy["probability"] >= 0.75,
                    "performance_tier": self._get_performance_tier(final_roi),
                    "execution_complexity": self._assess_execution_complexity(strategy, base_params)
                }
                
                scenarios.append(scenario)
            
            # Sort scenarios by ROI
            scenarios.sort(key=lambda x: x["roi"], reverse=True)
            
            # Generate executive summary
            executive_summary = await self._generate_executive_summary(scenarios, ai_enhancements)
            
            # Save scenario analysis to database
            await self._save_scenario_analysis(scenarios, base_params, ai_enhancements)
            
            result = {
                "scenarios": scenarios,
                "executive_summary": executive_summary,
                "analysis_meta": {
                    "engine": "Enhanced WhatIf with Full AI Integration",
                    "timestamp": datetime.now().isoformat(),
                    "product": product,
                    "base_engagement_rate": round(engagement_rate, 2),
                    "total_scenarios": len(scenarios),
                    "ai_enhanced": use_full_ai and bool(agent_outputs),
                    "best_scenario": scenarios[0]["name"] if scenarios else "None",
                    "recommended_scenarios": len([s for s in scenarios if s["recommended"]]),
                    "ai_enhancements_applied": ai_enhancements,
                    "average_roi": round(sum(s["roi"] for s in scenarios) / len(scenarios), 1) if scenarios else 0
                }
            }
            
            print(f"✅ Generated {len(scenarios)} AI-enhanced scenarios")
            return result
            
        except Exception as e:
            logger.error(f"What-If scenario generation failed: {e}")
            return await self._get_fallback_scenarios(base_params)
    
    async def _extract_ai_intelligence(self, agent_outputs: Dict) -> Dict[str, float]:
        """Extract intelligence from your complete agent system"""
        try:
            enhancements = {
                "sentiment_boost": 0,
                "creative_multiplier": 1.0,
                "finance_adjustment": 1.0,
                "historical_factor": 1.0
            }
            
            # FinBERT Sentiment Analysis Integration
            sentiment_data = agent_outputs.get('sentiment_metadata', {})
            if sentiment_data:
                sentiment_analysis = sentiment_data.get('sentiment_analysis', {})
                sentiment_score = sentiment_analysis.get('sentiment_score', 0.5)
                
                # Convert sentiment to performance boost
                if sentiment_score > 0.6:
                    enhancements["sentiment_boost"] = (sentiment_score - 0.5) * 0.5  # Up to 25% boost
                
                print(f"💰 FinBERT Sentiment Score: {sentiment_score:.3f}")
            
            # Creative Agent Intelligence
            creative_data = agent_outputs.get('Creative', {})
            if creative_data:
                confidence = creative_data.get('confidence_level', 0.7)
                channels = len(creative_data.get('recommended_channels', []))
                
                # Higher creative confidence and more channels = better reach
                enhancements["creative_multiplier"] = 0.85 + (confidence * 0.3) + (channels * 0.02)
                
                print(f"🎨 Creative Confidence: {confidence:.1%}, Channels: {channels}")
            
            # Finance Agent Intelligence
            finance_data = agent_outputs.get('Finance', {})
            if finance_data:
                projected_roi = finance_data.get('projected_roi', 100)
                success_prob = finance_data.get('success_probability', 0.7)
                
                # Finance agent ROI validation
                if projected_roi > 100:
                    enhancements["finance_adjustment"] = 1.15  # 15% boost for high ROI
                elif projected_roi > 50:
                    enhancements["finance_adjustment"] = 1.08  # 8% boost for good ROI
                elif projected_roi < 15:
                    enhancements["finance_adjustment"] = 0.92  # Reduce for low ROI
                
                print(f"💰 Finance ROI: {projected_roi}%, Success Prob: {success_prob:.1%}")
            
            # Historical Performance Factor
            historical_campaigns = agent_outputs.get('sentiment_metadata', {}).get('historical_campaigns_analyzed', 0)
            if historical_campaigns > 0:
                # Slight boost for historical data availability
                enhancements["historical_factor"] = 1.03
                
                print(f"📊 Historical Campaigns Analyzed: {historical_campaigns}")
            
            return enhancements
            
        except Exception as e:
            logger.error(f"AI intelligence extraction failed: {e}")
            return {
                "sentiment_boost": 0,
                "creative_multiplier": 1.0,
                "finance_adjustment": 1.0,
                "historical_factor": 1.0
            }
    
    async def _generate_ai_insights(
        self, 
        strategy: Dict, 
        roi: float, 
        params: Dict,
        agent_outputs: Optional[Dict] = None
    ) -> List[str]:
        """Generate AI-powered insights for each scenario using Gemini"""
        try:
            # Build context from agent outputs
            context_info = ""
            if agent_outputs:
                creative_data = agent_outputs.get('Creative', {})
                finance_data = agent_outputs.get('Finance', {})
                
                if creative_data:
                    context_info += f"Creative Strategy: {creative_data.get('confidence_level', 0.7):.1%} confidence. "
                if finance_data:
                    context_info += f"Finance Analysis: {finance_data.get('projected_roi', 0)}% ROI projected. "
            
            system_prompt = """You are a senior marketing strategist AI. Generate 3 concise, actionable insights for a campaign scenario. 
            Focus on practical business implications and optimization opportunities. Be specific and data-driven."""
            
            user_prompt = f"""
            Campaign Scenario Analysis:
            • Strategy: {strategy['name']} ({strategy['description']})
            • ROI Projection: {roi:.1f}%
            • Risk Level: {strategy['risk_level']}
            • Discount: {params.get('discount', 10)}%
            • Budget: ${params.get('budget', 15000):,}
            • Target Size: {params.get('target_size', 1000):,}
            • Duration: {params.get('duration', 30)} days
            
            Agent Intelligence: {context_info if context_info else "Basic analysis"}
            
            Provide exactly 3 brief, actionable insights for this scenario:
            """
            
            response = await gemini_client.generate_response(system_prompt, user_prompt)
            
            # Parse insights from response
            insights = []
            lines = response.split('\n')
            for line in lines:
                line = line.strip()
                if line and (line.startswith('•') or line.startswith('-') or line.startswith('1.') or line.startswith('2.') or line.startswith('3.')):
                    # Clean up the insight
                    clean_insight = line.lstrip('•-123.').strip()
                    if clean_insight:
                        insights.append(clean_insight)
            
            # Fallback to simple split if structured parsing fails
            if len(insights) < 2:
                insights = [line.strip() for line in response.split('.') if line.strip()][:3]
            
            return insights[:3]  # Ensure exactly 3 insights
            
        except Exception as e:
            logger.error(f"AI insight generation failed: {e}")
            # Fallback insights
            return [
                f"This {strategy['risk_level'].lower()}-risk strategy projects {roi:.1f}% ROI with {strategy['probability']} success probability",
                f"Budget efficiency: ${params.get('budget', 15000):,} investment targeting {params.get('target_size', 1000):,} customers",
                f"Recommended for campaigns prioritizing {strategy['risk_level'].lower()} risk tolerance and steady growth"
            ]
    
    def _assess_scenario_risks(self, strategy: Dict, roi: float, enhancements: Dict) -> List[str]:
        """Assess specific risks for each scenario"""
        risks = []
        
        if strategy["risk_level"] == "High":
            risks.append("High execution complexity requires experienced team")
        if roi > 200:
            risks.append("Exceptional ROI projection may be optimistic")
        if enhancements["sentiment_boost"] > 0.15:
            risks.append("Heavy reliance on positive market sentiment")
        if strategy["probability"] < 0.7:
            risks.append("Lower success probability requires contingency planning")
        
        return risks[:3]  # Max 3 risks
    
    def _get_performance_tier(self, roi: float) -> str:
        """Categorize performance tier"""
        if roi >= 150:
            return "Exceptional"
        elif roi >= 75:
            return "High"
        elif roi >= 25:
            return "Good"
        elif roi >= 10:
            return "Moderate"
        else:
            return "Low"
    
    def _assess_execution_complexity(self, strategy: Dict, params: Dict) -> str:
        """Assess execution complexity"""
        complexity_score = 0
        
        if strategy["risk_level"] == "High":
            complexity_score += 2
        if params.get('budget', 0) > 30000:
            complexity_score += 1
        if params.get('target_size', 0) > 5000:
            complexity_score += 1
        if params.get('duration', 30) > 60:
            complexity_score += 1
            
        if complexity_score >= 4:
            return "High"
        elif complexity_score >= 2:
            return "Medium"
        else:
            return "Low"
    
    async def _generate_executive_summary(self, scenarios: List[Dict], enhancements: Dict) -> str:
        """Generate executive summary using AI"""
        try:
            if not scenarios:
                return "No scenarios generated"
                
            best_roi = scenarios[0]["roi"]
            recommended_count = len([s for s in scenarios if s["recommended"]])
            avg_roi = sum(s["roi"] for s in scenarios) / len(scenarios)
            
            system_prompt = "You are an executive assistant. Generate a concise 2-sentence executive summary of campaign scenarios."
            
            user_prompt = f"""
            Scenario Analysis Summary:
            • Total Scenarios: {len(scenarios)}
            • Recommended Scenarios: {recommended_count}
            • Best ROI: {best_roi:.1f}%
            • Average ROI: {avg_roi:.1f}%
            • AI Enhanced: {enhancements['sentiment_boost'] > 0}
            
            Generate a concise executive summary:
            """
            
            summary = await gemini_client.generate_response(system_prompt, user_prompt)
            return summary.strip()
            
        except:
            return f"Analysis complete: {len(scenarios)} scenarios generated with {scenarios[0]['roi']:.1f}% top ROI and {len([s for s in scenarios if s['recommended']])} recommended strategies."
    
    async def _save_scenario_analysis(self, scenarios: List[Dict], params: Dict, enhancements: Dict):
        """Save scenario analysis to database for future reference"""
        try:
            analysis_data = {
                "analysis_id": f"whatif_{uuid.uuid4().hex[:8]}",
                "analysis_type": "whatif_scenario",
                "parameters": json.dumps(params),
                "scenarios_count": len(scenarios),
                "best_roi": scenarios[0]["roi"] if scenarios else 0,
                "ai_enhanced": enhancements.get("sentiment_boost", 0) > 0,
                "enhancements_applied": json.dumps(enhancements),
                "scenario_data": json.dumps(scenarios),
                "created_at": datetime.now().isoformat()
            }
            
            await insert_json_record('campaign_results', analysis_data)
            print(f"💾 Scenario analysis saved to database")
            
        except Exception as e:
            logger.error(f"Failed to save scenario analysis: {e}")
    
    async def _get_fallback_scenarios(self, params: Dict) -> Dict[str, Any]:
        """Fallback scenarios if AI generation fails"""
        budget = params.get('budget', 15000)
        discount = params.get('discount', 10)
        
        fallback_scenarios = [
            {
                "id": "fallback_conservative",
                "name": "Conservative Fallback",
                "roi": 22.0,
                "probability": "85%",
                "risk_level": "Low",
                "expected_revenue": budget * 1.5,
                "recommended": True,
                "ai_insights": ["Conservative approach with steady returns", "Low-risk execution suitable for all markets"],
                "performance_tier": "Good"
            },
            {
                "id": "fallback_balanced",  
                "name": "Balanced Fallback",
                "roi": 35.0,
                "probability": "70%",
                "risk_level": "Medium", 
                "expected_revenue": budget * 2.2,
                "recommended": True,
                "ai_insights": ["Balanced risk-reward profile", "Suitable for growth-focused campaigns"],
                "performance_tier": "Good"
            }
        ]
        
        return {
            "scenarios": fallback_scenarios,
            "executive_summary": f"Fallback analysis generated 2 scenarios with discount rate {discount}%",
            "analysis_meta": {
                "engine": "Fallback Mode",
                "timestamp": datetime.now().isoformat(),
                "ai_enhanced": False
            }
        }

# Global instance
whatif_engine = EnhancedWhatIfEngine()
