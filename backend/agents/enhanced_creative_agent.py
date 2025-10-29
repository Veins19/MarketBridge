"""
Enhanced Creative Agent - Fixed Version
Handles creative strategy, messaging, and channel optimization with robust error handling
"""

import asyncio
import logging
import json
from typing import Dict, List, Any, Optional
from datetime import datetime
import uuid
from agents.ai_client import gemini_client

logger = logging.getLogger(__name__)

class EnhancedCreativeAgent:
    """Enhanced Creative Agent with complete method implementations"""
    
    def __init__(self):
        self.agent_id = f"creative_{uuid.uuid4().hex[:8]}"
        self.confidence_threshold = 0.7
        self.initialized = False
        
    async def initialize(self):
        """Initialize creative agent"""
        try:
            self.initialized = True
            logger.info("🎨 Enhanced Creative Agent initialized successfully")
            return True
        except Exception as e:
            logger.error(f"❌ Creative Agent initialization failed: {e}")
            return False
    
    async def analyze_creative_strategy(self, query: str, product: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        """Comprehensive creative analysis using Gemini AI"""
        if context is None:
            context = {}
        try:
            if not self.initialized:
                await self.initialize()
                
            # Generate creative strategy using Gemini AI
            system_prompt = (
                "You are a creative marketing strategist AI agent. Your role is to generate "
                "comprehensive creative campaign strategies that are innovative, actionable, and "
                "aligned with business objectives. Focus on target audience definition, channel selection, "
                "key messaging, and campaign tone."
            )
            
            user_prompt = (
                f"Product: {product}\n"
                f"Campaign Query: {query}\n"
                "Generate a comprehensive creative marketing strategy including:\n"
                "1. Target audience definition and rationale\n"
                "2. Recommended marketing channels and justification\n"
                "3. Key messaging themes and campaign tone\n"
                "4. Creative assets needed for execution\n"
                "Be specific, strategic, and actionable in your recommendations."
            )
            
            # Get AI-generated strategy
            creative_response = await gemini_client.generate_response(system_prompt, user_prompt)
            
            # Extract target audience using existing logic
            target_audience = self._extract_target_audience(query, context or {})
            
            # Generate channel strategy
            recommended_channels = self._select_optimal_channels(query, target_audience)
            
            # Generate channel rationale
            channel_rationale = self._generate_channel_rationale(recommended_channels, target_audience)
            
            # Create key messaging
            key_message = self._create_key_message(query, product, target_audience)
            
            # Estimate creative budget
            estimated_budget = self._estimate_creative_budget(20000.0, recommended_channels)
            
            # Use AI-generated strategy or fallback to existing method
            strategy = creative_response if creative_response else self._generate_creative_strategy(query, product, target_audience, recommended_channels)
            
            # Calculate confidence
            confidence = self._calculate_creative_confidence(query, recommended_channels, target_audience)
            
            return {
                "agent": "Enhanced Creative Agent",
                "timestamp": datetime.now().isoformat(),
                "analysis_id": f"creative_{uuid.uuid4().hex[:8]}",
                "strategy": strategy,
                "target_audience": target_audience,
                "recommended_channels": recommended_channels,
                "channel_rationale": channel_rationale,
                "key_message": key_message,
                "estimated_budget": estimated_budget,
                "messaging_themes": self._generate_messaging_themes(query, product),
                "creative_assets_needed": self._identify_creative_assets(recommended_channels),
                "campaign_tone": self._determine_campaign_tone(query),
                "success_metrics": self._define_success_metrics(recommended_channels),
                "confidence_level": confidence,
                "reasoning": f"Creative strategy developed for {product} targeting {target_audience}",
                "agent_status": "enhanced_analysis_complete"
            }
            
        except Exception as e:
            logger.error(f"❌ Creative analysis failed: {e}")
            return self._get_fallback_creative_analysis(query, product)
    
    def _extract_target_audience(self, query: str, context: Dict) -> str:
        """Extract and define target audience from query and context - FIXED METHOD"""
        try:
            query_lower = query.lower()
            
            # Audience detection based on keywords
            if any(word in query_lower for word in ["premium", "luxury", "high-end", "professional"]):
                return "High-income professionals and tech enthusiasts (ages 25-45, $75k+ income)"
            elif any(word in query_lower for word in ["budget", "affordable", "cheap", "deal"]):
                return "Price-conscious consumers and students (ages 18-35, budget-focused)"
            elif any(word in query_lower for word in ["holiday", "sale", "seasonal", "black friday"]):
                return "Holiday shoppers and deal-seekers (broad demographics, sale-driven)"
            elif any(word in query_lower for word in ["aggressive", "boost", "revenue", "market share"]):
                return "Business decision makers and power users (ages 25-50, high engagement)"
            elif "enthusiast" in query_lower:
                return "Product enthusiasts and early adopters (ages 20-40, tech-savvy)"
            else:
                # Default audience based on context
                customer_count = context.get("total_customers", 1000)
                if customer_count > 5000:
                    return "Broad consumer market with diverse demographics"
                else:
                    return "Targeted customer base focused on quality and value"
                    
        except Exception as e:
            logger.warning(f"Target audience extraction error: {e}")
            return "Target demographic focused on product value and quality"
    
    def _generate_channel_rationale(self, channels: List[str], audience: str) -> str:
        """Generate comprehensive rationale for channel selection - FIXED METHOD"""
        try:
            if not channels:
                return "Multi-channel approach selected for comprehensive market reach"
            
            rationale_parts = []
            
            for channel in channels[:4]:  # Top 4 channels for detailed rationale
                if channel == "email":
                    rationale_parts.append("Email marketing for direct customer engagement, personalization, and high ROI conversion")
                elif channel == "social":
                    rationale_parts.append("Social media for brand awareness, viral potential, and community building")
                elif channel == "search":
                    rationale_parts.append("Search engine marketing for high-intent customer acquisition and immediate conversion")
                elif channel == "display":
                    rationale_parts.append("Display advertising for broad brand visibility and retargeting capabilities")
                elif channel == "content":
                    rationale_parts.append("Content marketing for thought leadership, SEO benefits, and long-term engagement")
                elif channel == "video":
                    rationale_parts.append("Video content for product demonstration and emotional engagement")
                elif channel == "influencer":
                    rationale_parts.append("Influencer partnerships for authentic endorsements and niche audience reach")
                elif channel == "affiliate":
                    rationale_parts.append("Affiliate marketing for performance-based customer acquisition")
            
            # Add audience-specific rationale
            audience_context = ""
            if "professional" in audience.lower():
                audience_context = " Channels optimized for professional demographics with business-focused messaging."
            elif "budget" in audience.lower() or "deal" in audience.lower():
                audience_context = " Channel mix prioritizes cost-effective reach and conversion optimization."
            elif "enthusiast" in audience.lower():
                audience_context = " Strategy targets engaged communities and product-focused audiences."
            
            return "; ".join(rationale_parts) + audience_context
            
        except Exception as e:
            logger.warning(f"Channel rationale generation error: {e}")
            return "Strategic multi-channel approach optimized for target audience engagement and conversion"
    
    def _estimate_creative_budget(self, total_budget: float, channels: List[str]) -> Dict[str, Any]:
        """Estimate creative production budget allocation - FIXED METHOD"""
        try:
            # Creative production typically 15-25% of total budget
            creative_percentage = 0.20  # 20%
            total_creative_budget = float(total_budget) * creative_percentage
            
            if not channels or len(channels) == 0:
                return {
                    "total_creative_budget": round(total_creative_budget, 2),
                    "per_channel_average": round(total_creative_budget / 3, 2),  # Assume 3 channels
                    "budget_allocation": "Standard creative production budget"
                }
            
            # Channel-specific budget multipliers
            channel_multipliers = {
                "video": 1.8,     # Video production is expensive
                "display": 1.2,   # Graphics and banners
                "social": 1.1,    # Social content creation
                "content": 1.3,   # Blog posts, articles
                "email": 0.8,     # Lower creative needs
                "search": 0.7,    # Text-based ads
                "influencer": 1.4, # Content collaboration
                "affiliate": 0.6   # Minimal creative needs
            }
            
            # Calculate weighted budget allocation
            total_weight = sum(channel_multipliers.get(channel, 1.0) for channel in channels)
            budget_breakdown = {}
            
            for channel in channels:
                multiplier = channel_multipliers.get(channel, 1.0)
                channel_budget = (total_creative_budget * multiplier) / total_weight
                budget_breakdown[f"{channel}_creative"] = round(channel_budget, 2)
            
            budget_breakdown["total_creative_budget"] = round(total_creative_budget, 2)
            budget_breakdown["budget_efficiency"] = round(total_creative_budget / len(channels), 2)
            
            return budget_breakdown
            
        except Exception as e:
            logger.warning(f"Creative budget estimation error: {e}")
            return {
                "total_creative_budget": round(float(total_budget) * 0.15, 2),
                "budget_allocation": "Conservative creative budget estimate"
            }
    
    def _select_optimal_channels(self, query: str, audience: str) -> List[str]:
        """Select optimal marketing channels based on query and audience"""
        try:
            query_lower = query.lower()
            base_channels = ["email", "social", "search"]
            
            # Add channels based on query intent
            if any(word in query_lower for word in ["aggressive", "boost", "revenue"]):
                base_channels.extend(["display", "video"])
            if "holiday" in query_lower or "sale" in query_lower:
                base_channels.extend(["display", "affiliate"])
            if "premium" in query_lower:
                base_channels.extend(["content", "influencer"])
            if "enthusiast" in query_lower:
                base_channels.extend(["content", "video"])
            
            # Remove duplicates and limit to top 5
            return list(set(base_channels))[:5]
            
        except Exception:
            return ["email", "social", "search", "display"]
    
    def _create_key_message(self, query: str, product: str, audience: str) -> str:
        """Create key marketing message"""
        try:
            if "aggressive" in query.lower() and "revenue" in query.lower():
                return f"Transform your experience with {product} - Limited time offer for maximum value"
            elif "premium" in query.lower():
                return f"Elevate your lifestyle with premium {product} - Crafted for excellence"
            elif "holiday" in query.lower():
                return f"Perfect holiday gift: {product} - Special seasonal pricing available"
            else:
                return f"Discover the difference with {product} - Quality you can trust"
        except Exception:
            return f"Experience the best with {product}"
    
    def _generate_creative_strategy(self, query: str, product: str, audience: str, channels: List[str]) -> str:
        """Generate comprehensive creative strategy"""
        try:
            strategy_focus = "premium positioning" if "premium" in query.lower() else "value-driven messaging"
            channel_approach = f"multi-channel approach across {', '.join(channels[:3])}"
            
            return f"Comprehensive creative strategy for {product} featuring {strategy_focus} with {channel_approach}. " \
                   f"Targeting {audience.split('(')[0].strip()} through integrated campaign messaging that emphasizes " \
                   f"product benefits and drives conversion across all touchpoints."
        except Exception:
            return f"Creative marketing strategy developed for {product} with integrated multi-channel approach"
    
    def _generate_messaging_themes(self, query: str, product: str) -> List[str]:
        """Generate messaging themes"""
        try:
            themes = ["Quality and reliability", "Customer satisfaction"]
            
            if "aggressive" in query.lower() or "boost" in query.lower():
                themes.extend(["Performance and results", "Competitive advantage"])
            if "holiday" in query.lower():
                themes.extend(["Perfect gift solution", "Limited time value"])
            if "premium" in query.lower():
                themes.extend(["Premium quality", "Exclusive experience"])
                
            return themes[:4]
        except Exception:
            return ["Product quality", "Customer value", "Trusted brand", "Satisfaction guarantee"]
    
    def _identify_creative_assets(self, channels: List[str]) -> List[str]:
        """Identify required creative assets"""
        try:
            assets = []
            for channel in channels:
                if channel == "social":
                    assets.extend(["Social media graphics", "Post templates"])
                elif channel == "display":
                    assets.extend(["Banner ads", "Display graphics"])
                elif channel == "video":
                    assets.extend(["Product videos", "Demo content"])
                elif channel == "email":
                    assets.extend(["Email templates", "Newsletter designs"])
                elif channel == "content":
                    assets.extend(["Blog graphics", "Infographics"])
            
            return list(set(assets))[:6]  # Top 6 assets
        except Exception:
            return ["Marketing graphics", "Product images", "Ad copy", "Email templates"]
    
    def _determine_campaign_tone(self, query: str) -> str:
        """Determine appropriate campaign tone"""
        try:
            if "aggressive" in query.lower():
                return "Bold and assertive"
            elif "premium" in query.lower():
                return "Sophisticated and aspirational"
            elif "holiday" in query.lower():
                return "Festive and welcoming"
            else:
                return "Professional and trustworthy"
        except Exception:
            return "Professional and engaging"
    
    def _define_success_metrics(self, channels: List[str]) -> List[str]:
        """Define success metrics for campaign"""
        try:
            base_metrics = ["Click-through rate", "Conversion rate", "Return on ad spend"]
            
            if "social" in channels:
                base_metrics.append("Engagement rate")
            if "email" in channels:
                base_metrics.append("Email open rate")
            if "video" in channels:
                base_metrics.append("Video completion rate")
                
            return base_metrics[:5]
        except Exception:
            return ["Conversion rate", "Click-through rate", "Return on investment"]
    
    def _calculate_creative_confidence(self, query: str, channels: List[str], audience: str) -> float:
        """Calculate confidence level for creative strategy"""
        try:
            base_confidence = 0.7
            
            # Boost confidence for clear targeting
            if any(keyword in query.lower() for keyword in ["premium", "holiday", "aggressive"]):
                base_confidence += 0.1
            
            # Boost confidence for optimal channel count
            if 3 <= len(channels) <= 5:
                base_confidence += 0.1
            
            # Boost confidence for specific audience
            if "ages" in audience and "income" in audience:
                base_confidence += 0.05
            
            return min(0.95, base_confidence)  # Cap at 95%
            
        except Exception:
            return 0.75  # Default confidence
    
    def _get_fallback_creative_analysis(self, query: str, product: str) -> Dict[str, Any]:
        """Fallback creative analysis when main analysis fails"""
        return {
            "agent": "Enhanced Creative Agent (Fallback)",
            "strategy": f"Strategic creative campaign for {product} focused on {query}",
            "target_audience": "Target demographic based on product positioning",
            "recommended_channels": ["email", "social", "search", "display"],
            "channel_rationale": "Multi-channel approach for comprehensive market coverage",
            "key_message": f"Experience excellence with {product}",
            "estimated_budget": {"total_creative_budget": 3000.0},
            "messaging_themes": ["Quality", "Value", "Trust", "Innovation"],
            "creative_assets_needed": ["Graphics", "Copy", "Templates"],
            "campaign_tone": "Professional and engaging",
            "success_metrics": ["CTR", "Conversion Rate", "ROAS"],
            "confidence_level": 0.7,
            "reasoning": "Fallback creative strategy with proven marketing principles",
            "agent_status": "fallback_analysis_complete"
        }
    
    async def negotiate_with_agents(self, proposal: Dict, other_agents_data: Dict) -> Dict[str, Any]:
        """Negotiate creative strategy with other agents"""
        try:
            # Get finance constraints
            finance_data = other_agents_data.get('Finance', {})
            approved_budget = finance_data.get('approved_budget', 20000)
            
            # Adjust creative budget if needed
            current_budget = proposal.get('estimated_budget', {}).get('total_creative_budget', 3000)
            max_creative_budget = float(approved_budget) * 0.25  # Max 25% for creative
            
            if current_budget > max_creative_budget:
                adjusted_budget = self._estimate_creative_budget(float(approved_budget), 
                                                              proposal.get('recommended_channels', []))
                proposal['estimated_budget'] = adjusted_budget
                proposal['budget_adjusted'] = True
            
            # Adapt channels based on inventory
            inventory_data = other_agents_data.get('Inventory', {})
            if inventory_data.get('stock_status') == 'limited':
                # Focus on targeted channels for limited inventory
                proposal['recommended_channels'] = proposal.get('recommended_channels', [])[:3]
                proposal['strategy'] += " - Focused targeting due to inventory constraints"
            
            proposal['negotiation_complete'] = True
            return proposal
            
        except Exception as e:
            logger.error(f"Creative negotiation error: {e}")
            proposal['negotiation_error'] = str(e)
            return proposal
