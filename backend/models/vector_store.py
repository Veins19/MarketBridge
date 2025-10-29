import chromadb
from chromadb.config import Settings
from chromadb.utils import embedding_functions
import logging
from typing import List, Dict, Any, Optional, TypeVar, Union, cast
from chromadb import Collection
from chromadb.api.types import Documents, QueryResult, Embeddable, EmbeddingFunction
import json
from datetime import datetime
import os

logger = logging.getLogger(__name__)

class MarketBridgeVectorStore:
    """ChromaDB Vector Store for MarketBridge campaign and customer data"""
    
    def __init__(self):
        self.client = None
        self.campaigns_collection: Optional[Collection] = None
        self.customers_collection: Optional[Collection] = None
        self.products_collection: Optional[Collection] = None
        self.embedding_function = None
        
    async def initialize(self) -> bool:
        """Initialize ChromaDB client and collections"""
        try:
            # Initialize ChromaDB client (persistent storage)
            persist_directory = "./data/chromadb"
            os.makedirs(persist_directory, exist_ok=True)
            
            self.client = chromadb.PersistentClient(path=persist_directory)
            
            # Initialize embedding function (sentence transformers)
            self.embedding_function = cast(
                EmbeddingFunction[Embeddable],
                embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
            )
            
            # Create collections
            self.campaigns_collection = self.client.get_or_create_collection(
                name="campaigns",
                embedding_function=self.embedding_function,
                metadata={"hnsw:space": "cosine"}
            )
            
            self.customers_collection = self.client.get_or_create_collection(
                name="customers", 
                embedding_function=self.embedding_function,
                metadata={"hnsw:space": "cosine"}
            )
            
            self.products_collection = self.client.get_or_create_collection(
                name="products",
                embedding_function=self.embedding_function,
                metadata={"hnsw:space": "cosine"}
            )
            
            logger.info("✅ ChromaDB Vector Store initialized successfully")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to initialize ChromaDB: {str(e)}")
            return False
    
    async def add_campaign_data(self, campaign_id: str, campaign_data: Dict[str, Any]) -> None:
        """Add campaign data to vector store for future retrieval"""
        if not self.campaigns_collection:
            logger.error("❌ Campaign collection not initialized")
            return
        try:
            # Create searchable text from campaign data
            campaign_text = self._create_campaign_text(campaign_data)
            
            # Add to ChromaDB
            self.campaigns_collection.add(
                documents=[campaign_text],
                metadatas=[{
                    "campaign_id": campaign_id,
                    "timestamp": datetime.now().isoformat(),
                    "query": campaign_data.get("query", ""),
                    "product": campaign_data.get("product", ""),
                    "decision": campaign_data.get("Executive_Decision", ""),
                    "roi": str(campaign_data.get("Finance", {}).get("projected_roi", 0))
                }],
                ids=[f"campaign_{campaign_id}"]
            )
            
            logger.info(f"✅ Added campaign {campaign_id} to vector store")
            
        except Exception as e:
            logger.error(f"❌ Failed to add campaign to vector store: {str(e)}")
    
    async def search_similar_campaigns(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Search for similar campaigns based on query"""
        if not self.campaigns_collection:
            logger.error("❌ Campaign collection not initialized")
            return []
        try:
            results: QueryResult = self.campaigns_collection.query(
                query_texts=[query],
                n_results=limit
            )
            
            similar_campaigns: List[Dict[str, Any]] = []
            documents = results.get('documents', [])
            if documents and len(documents) > 0:
                metadatas = results.get('metadatas', [[]])
                distances = results.get('distances', [[]])
                for i, doc in enumerate(documents[0]):
                    similar_campaigns.append({
                        "content": doc,
                        "metadata": metadatas[0][i] if metadatas and len(metadatas) > 0 else {},
                        "similarity": 1 - distances[0][i] if distances and len(distances) > 0 else 0.0  # Convert distance to similarity
                    })
            
            logger.info(f"✅ Found {len(similar_campaigns)} similar campaigns")
            return similar_campaigns
            
        except Exception as e:
            logger.error(f"❌ Failed to search campaigns: {str(e)}")
            return []
    
    def _create_campaign_text(self, campaign_data: Dict[str, Any]) -> str:
        """Create searchable text representation of campaign data"""
        text_parts = []
        
        # Basic info
        text_parts.append(f"Query: {campaign_data.get('query', '')}")
        text_parts.append(f"Product: {campaign_data.get('product', '')}")
        
        # Creative strategy
        creative = campaign_data.get('Creative', {})
        if creative:
            text_parts.append(f"Strategy: {creative.get('strategy', '')}")
            text_parts.append(f"Channels: {', '.join(creative.get('recommended_channels', []))}")
        
        # Finance analysis
        finance = campaign_data.get('Finance', {})
        if finance:
            text_parts.append(f"ROI: {finance.get('projected_roi', 0)}%")
            text_parts.append(f"Budget: ${finance.get('approved_budget', 0)}")
            text_parts.append(f"Risk: {finance.get('risk_assessment', '')}")
        
        # Executive decision
        text_parts.append(f"Decision: {campaign_data.get('Executive_Decision', '')}")
        
        return " | ".join(text_parts)

# Global vector store instance
vector_store = MarketBridgeVectorStore()
