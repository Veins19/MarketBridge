import asyncio
from typing import List, Dict, Any, Optional, Union
import logging
from datetime import datetime, timedelta
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from transformers import pipeline
from transformers.pipelines.text_classification import TextClassificationPipeline
import numpy as np
from models.database import execute_query, execute_one

logger = logging.getLogger(__name__)

class SentimentTrendAnalyzer:
    """Simple FinBERT-powered sentiment analysis for MarketBridge"""
    
    def __init__(self):
        self.vader_analyzer = SentimentIntensityAnalyzer()
        self._finbert_pipeline = None
        self.initialized = False
        
    def get_pipeline(self) -> Optional[TextClassificationPipeline]:
        """Get the FinBERT pipeline"""
        return self._finbert_pipeline
        
    def set_pipeline(self, value: Optional[TextClassificationPipeline]) -> None:
        """Set the FinBERT pipeline"""
        self._finbert_pipeline = value
        
    async def initialize(self):
        """Initialize FinBERT sentiment analyzer"""
        try:
            # Load FinBERT for business sentiment
            from transformers import pipeline, TextClassificationPipeline
            logger.info("💰 Loading FinBERT for business sentiment analysis...")
            
            self.finbert_pipeline: TextClassificationPipeline = pipeline(
                task="text-classification", 
                model="ProsusAI/finbert",
                device=-1  # CPU
            )
            
            # Test FinBERT
            test_result = self.finbert_pipeline("This campaign will generate excellent ROI")[0]
            logger.info(f"✅ FinBERT test: {test_result['label']} ({test_result['score']:.3f})")
            
            self.initialized = True
            logger.info("✅ FinBERT Sentiment Analyzer initialized successfully")
            return True
            
        except Exception as e:
            logger.error(f"❌ FinBERT initialization failed: {str(e)}")
            # Fallback to VADER only
            self.initialized = True
            return False
    
    async def analyze_campaign_sentiment(self, campaign_query: str, product: str) -> Dict[str, Any]:
        """Analyze sentiment for campaign planning"""
        try:
            # Analyze query sentiment
            query_sentiment = self._analyze_text_sentiment(campaign_query)
            
            # Get historical trends
            historical_sentiment = await self._get_historical_sentiment(product)
            
            # Generate recommendations
            recommendations = self._generate_sentiment_recommendations(query_sentiment, historical_sentiment)
            
            # Calculate overall score
            overall_score = self._calculate_overall_sentiment_score(query_sentiment, historical_sentiment)
            
            return {
                "query_sentiment": query_sentiment,
                "historical_trends": historical_sentiment,
                "recommendations": recommendations,
                "sentiment_score": overall_score,
                "analysis_timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"❌ Sentiment analysis failed: {str(e)}")
            return {
                "query_sentiment": {"sentiment_label": "neutral", "confidence": 0.5},
                "historical_trends": {"trend_direction": "neutral"},
                "recommendations": ["Use balanced messaging approach"],
                "sentiment_score": 0.0,
                "analysis_timestamp": datetime.now().isoformat()
            }
    
    def _analyze_text_sentiment(self, text: str) -> Dict[str, Any]:
        """Analyze text sentiment using FinBERT + VADER fallback"""
        try:
            # Try FinBERT first
            if self.finbert_pipeline:
                try:
                    finbert_result = self.finbert_pipeline(text)[0]
                    
                    # Convert to standard format
                    label = finbert_result['label'].lower()
                    confidence = finbert_result['score']
                    
                    if label == 'positive':
                        compound = confidence
                        positive, neutral, negative = confidence, 1-confidence, 0
                    elif label == 'negative':
                        compound = -confidence
                        positive, neutral, negative = 0, 1-confidence, confidence
                    else:  # neutral
                        compound = 0
                        positive, neutral, negative = 0, confidence, 0
                    
                    return {
                        "compound": round(compound, 3),
                        "positive": round(positive, 3),
                        "neutral": round(neutral, 3),
                        "negative": round(negative, 3),
                        "sentiment_label": label,
                        "confidence": round(confidence, 3),
                        "analysis_method": "FinBERT",
                        "business_optimized": True
                    }
                    
                except Exception as e:
                    logger.warning(f"FinBERT failed, using VADER: {str(e)}")
            
            # VADER fallback
            vader_scores = self.vader_analyzer.polarity_scores(text)
            
            return {
                "compound": vader_scores['compound'],
                "positive": vader_scores['pos'],
                "neutral": vader_scores['neu'],
                "negative": vader_scores['neg'],
                "sentiment_label": self._get_sentiment_label(vader_scores['compound']),
                "confidence": abs(vader_scores['compound']),
                "analysis_method": "VADER",
                "business_optimized": False
            }
            
        except Exception as e:
            logger.error(f"Sentiment analysis error: {str(e)}")
            return {"sentiment_label": "neutral", "confidence": 0.5, "analysis_method": "fallback"}
    
    def _get_sentiment_label(self, compound_score: float) -> str:
        """Convert compound score to label"""
        if compound_score >= 0.05:
            return "positive"
        elif compound_score <= -0.05:
            return "negative"
        else:
            return "neutral"
    
    async def _get_historical_sentiment(self, product: str) -> Dict[str, Any]:
        """Get simple historical sentiment trends"""
        try:
            query = """
            SELECT 
                COUNT(*) as total_campaigns,
                AVG(CASE WHEN projected_roi > 20 THEN 1 ELSE -1 END) as sentiment_trend
            FROM campaign_results 
            WHERE created_at > NOW() - INTERVAL '90 days'
            """
            
            result = await execute_one(query)
            
            if result and result['total_campaigns'] > 0:
                trend = float(result['sentiment_trend'] or 0)
                return {
                    "sentiment_trend": round(trend, 3),
                    "campaign_count": int(result['total_campaigns']),
                    "trend_direction": "improving" if trend > 0 else "declining" if trend < 0 else "stable"
                }
            else:
                return {
                    "sentiment_trend": 0.0,
                    "campaign_count": 0,
                    "trend_direction": "neutral"
                }
                
        except Exception as e:
            logger.error(f"Historical sentiment error: {str(e)}")
            return {"sentiment_trend": 0.0, "trend_direction": "neutral", "campaign_count": 0}
    
    def _generate_sentiment_recommendations(self, query_sentiment: Dict, historical_sentiment: Dict) -> List[str]:
        """Generate simple recommendations"""
        recommendations = []
        
        # Query sentiment
        label = query_sentiment.get("sentiment_label", "neutral")
        if label == "positive":
            recommendations.append("Query sentiment is positive - use optimistic messaging")
        elif label == "negative":
            recommendations.append("Query sentiment is negative - focus on problem-solving benefits")
        
        # Historical trend
        trend = historical_sentiment.get("trend_direction", "neutral")
        if trend == "improving":
            recommendations.append("Historical performance is improving - scale with confidence")
        elif trend == "declining":
            recommendations.append("Recent performance declining - consider strategy adjustment")
        
        # Analysis method
        if query_sentiment.get("business_optimized"):
            recommendations.append("FinBERT business analysis applied for enhanced accuracy")
        
        return recommendations[:3]
    
    def _calculate_overall_sentiment_score(self, query_sentiment: Dict, historical_sentiment: Dict) -> float:
        """Calculate simple overall score"""
        try:
            query_score = query_sentiment.get("compound", 0.0)
            historical_score = historical_sentiment.get("sentiment_trend", 0.0) * 0.5  # Scale down historical
            
            # 70% query, 30% historical
            overall = (query_score * 0.7) + (historical_score * 0.3)
            return round(overall, 3)
            
        except Exception:
            return 0.0

# Global instance
sentiment_analyzer = SentimentTrendAnalyzer()
